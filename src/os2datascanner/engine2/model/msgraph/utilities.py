from dataclasses import dataclass
from contextlib import contextmanager
import logging
import requests

from os2datascanner.engine2.utilities.backoff import WebRetrier
from os2datascanner.engine2 import settings as engine2_settings

from ..core import Source


logger = logging.getLogger(__name__)


def make_token(client_id, tenant_id, client_secret):
    response = WebRetrier().run(
            requests.post,
            f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
            {
                "client_id": client_id,
                "scope": "https://graph.microsoft.com/.default",
                "client_secret": client_secret,
                "grant_type": "client_credentials"
            })
    response.raise_for_status()
    logger.info("Collected new token")
    return response.json()["access_token"]


class MSGraphSource(Source):
    yields_independent_sources = True

    def __init__(self, client_id, tenant_id, client_secret):
        super().__init__()
        self._client_id = client_id
        self._tenant_id = tenant_id
        self._client_secret = client_secret

    def censor(self):
        return type(self)(self._client_id, self._tenant_id, None)

    def make_token(self):
        return make_token(
                self._client_id, self._tenant_id, self._client_secret)

    def _generate_state(self, sm):
        with requests.Session() as session:
            yield MSGraphSource.GraphCaller(self.make_token, session)

    def _list_users(self, sm):
        yield from sm.open(self).paginated_get("users")

    class GraphCaller:
        def __init__(self, token_creator, session=None):
            self._token_creator = token_creator
            self._token = token_creator()

            self._session = session or requests

        def _make_headers(self):
            return {
                "authorization": "Bearer {0}".format(self._token),
            }

        def get_raw(self, tail, timeout=None):
            return WebRetrier().run(
                    self._session.get,
                    "https://graph.microsoft.com/v1.0/{0}".format(tail),
                    headers=self._make_headers(),
                    timeout=timeout)

        def get(self, tail, *, json=True, _retry=False):
            timeout = engine2_settings.model["msgraph"]["timeout"]
            response = self.get_raw(tail, timeout=timeout)
            try:
                response.raise_for_status()
                if json:
                    return response.json()
                else:
                    return response.content
            except requests.exceptions.HTTPError as ex:
                # If _retry, it means we have a status code 401 but are trying a second time.
                # It should've succeeded the first time, so we raise an exc to avoid a potential
                # endless loop
                if ex.response.status_code != 401 or _retry:
                    raise ex

                self._token = self._token_creator()
                return self.get(tail, json=json, _retry=True)

        def paginated_get(self, endpoint: str):
            """ Performs a GET request on specified MSGraph endpoint and
            uses generators to go through pages if response is paginated"""
            result = self.get(endpoint)
            yield from result.get('value')

            while '@odata.nextLink' in result:
                result = self.follow_next_link(result["@odata.nextLink"])
                yield from result.get('value')

        def head_raw(self, tail):
            return WebRetrier().run(
                    self._session.head,
                    "https://graph.microsoft.com/v1.0/{0}".format(tail),
                    headers=self._make_headers())

        def head(self, tail, _retry=False):
            response = self.head_raw(tail)
            try:
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError as ex:
                if ex.response.status_code != 401 or _retry:
                    raise ex

            self._token = self._token_creator()
            return self.head(tail, _retry=True)

        def follow_next_link(self, next_page, _retry=False):
            response = WebRetrier().run(
                    self._session.get, next_page, headers=self._make_headers())
            try:
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as ex:
                if ex.response.status_code != 401 or _retry:
                    raise ex
            self._token = self._token_creator()
            return self.follow_next_link(next_page, _retry=True)

    def to_json_object(self):
        return dict(
            **super().to_json_object(),
            client_id=self._client_id,
            tenant_id=self._tenant_id,
            client_secret=self._client_secret,
        )


@contextmanager
def ignore_responses(*status_codes):
    try:
        yield
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code in status_codes:
            pass
        else:
            raise


class MailFSBuilder:
    """Utility class to construct folder system for MS Graph mailscanner"""

    def __init__(self, source, sm, pn):
        self._source = source
        self._sm = sm
        self._pn = pn
        self._folder_map = {}
        self.build_mail_fs_map()

    def build_mail_fs_map(self):
        """Constructs a dict of mail folders with fid as keys"""
        pn = self._pn
        sm = self._sm
        src = self._source
        ps = engine2_settings.model["msgraph"]["page_size"]

        recursion_stack = []

        result = sm.open(src).get(
            (f"users/{pn}/mailFolders?$select=id,"
             f"parentFolderId,displayName,childFolderCount&$top={ps}"))

        recursion_stack = self._process_result(result, recursion_stack)
        if len(recursion_stack) > 0:
            self._recurse_child_folders(recursion_stack)

    def _process_result(self, result, recursion_stack):
        for folder in result["value"]:
            mail_folder = MailFolder(folder["id"],
                                     folder["parentFolderId"],
                                     folder["displayName"],
                                     folder["childFolderCount"])

            self._folder_map[folder["id"]] = mail_folder

            if mail_folder.children > 0:
                recursion_stack.append(mail_folder)

        if '@odata.nextLink' in result:
            result = self._sm.open(self._source).follow_next_link(result["@odata.nextLink"])
            self._process_result(result, recursion_stack)

        return recursion_stack

    def _recurse_child_folders(self, recursion_stack):
        ps = engine2_settings.model["msgraph"]["page_size"]
        head = recursion_stack.pop()
        fid = head.fid

        result = self._sm.open(self._source).get(
            (f"users/{self._pn}/mailFolders/{fid}/childFolders?$select=id,"
             f"parentFolderId,displayName,childFolderCount&$top={ps}"))

        recursion_stack = self._process_result(result, recursion_stack)

        if len(recursion_stack) > 0:
            self._recurse_child_folders(recursion_stack)

    def build_path(self, fid):
        """Builds a folder path given an fid"""
        root = self._folder_map.get(fid, None)

        def _reverse_traverse(folder: MailFolder):
            if folder is None:
                return ""

            parent = self._folder_map.get(folder.parent_folder_id, None)
            if parent is None:
                return folder.display_name

            return _reverse_traverse(parent) + '/' + folder.display_name

        return _reverse_traverse(root)


@dataclass
class MailFolder:
    """Object to represent a mail folder in MS Graph."""
    fid: str
    parent_folder_id: str
    display_name: str
    children: int
