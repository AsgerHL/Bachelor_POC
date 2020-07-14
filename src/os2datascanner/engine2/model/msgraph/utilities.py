import requests

from ..core import Source


def _make_token_endpoint(tenant_id):
    return "https://login.microsoftonline.com/{0}/oauth2/v2.0/token".format(
            tenant_id)


class MSGraphSource(Source):
    def __init__(self, client_id, tenant_id, client_secret):
        super().__init__()
        self._client_id = client_id
        self._tenant_id = tenant_id
        self._client_secret = client_secret

    def censor(self):
        return type(self)(self._client_id, self._tenant_id, None)

    def _generate_state(self, sm):
        response = requests.post(
                _make_token_endpoint(self._tenant_id),
                {
                    "client_id": self._client_id,
                    "scope": "https://graph.microsoft.com/.default",
                    "client_secret": self._client_secret,
                    "grant_type": "client_credentials"
                })
        response.raise_for_status()
        token = response.json()["access_token"]

        yield MSGraphSource.GraphCaller(token)

    def _list_users(self, sm):
        return sm.open(self).get("users")

    class GraphCaller:
        def __init__(self, token):
            self._token = token

        def get(self, tail, *, json=True):
            response = requests.get(
                    "https://graph.microsoft.com/v1.0/{0}".format(tail),
                    headers={"authorization": "Bearer {0}".format(self._token)})
            response.raise_for_status()
            if json:
                return response.json()
            else:
                return response.content

        def head(self, tail):
            response = requests.head(
                    "https://graph.microsoft.com/v1.0/{0}".format(tail),
                    headers={"authorization": "Bearer {0}".format(self._token)})
            response.raise_for_status()
            return response
