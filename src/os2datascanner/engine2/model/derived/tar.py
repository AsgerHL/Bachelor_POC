from tarfile import open as open_tar
from datetime import datetime
from contextlib import contextmanager

from ...conversions.types import OutputType
from ...conversions.utilities.navigable import make_values_navigable
from ..core import Source, Handle, FileResource
from .derived import DerivedSource


@Source.mime_handler("application/x-tar")
class TarSource(DerivedSource):
    type_label = "tar"

    def handles(self, sm):
        tarfile = sm.open(self)
        for f in tarfile.getmembers():
            if f.isfile():
                yield TarHandle(self, f.name)

    def _generate_state(self, sm):
        with self.handle.follow(sm).make_path() as r, open_tar(str(r), "r") as tp:
            yield tp


tarinfo_attributes = (
        "chksum", "devmajor", "devminor", "gid", "gname", "linkname",
        "linkpath", "mode", "mtime", "name", "offset", "offset_data", "path",
        "pax_headers", "size", "sparse", "type", "uid", "uname",)


class TarResource(FileResource):
    def __init__(self, handle, sm):
        super().__init__(handle, sm)
        self._mr = None

    def _get_raw_info(self):
        return self._get_cookie().getmember(self.handle.relative_path)

    def check(self) -> bool:
        try:
            self._get_raw_info()
            return True
        except KeyError:
            return False

    def unpack_info(self):
        if not self._mr:
            raw_info = self._get_raw_info()
            ts = datetime.fromtimestamp(raw_info.mtime)
            self._mr = make_values_navigable(
                    {k: getattr(raw_info, k) for k in tarinfo_attributes} |
                    {OutputType.LastModified: ts})
        return self._mr

    def get_size(self):
        return self.unpack_info()["size"]

    def get_last_modified(self):
        return self.unpack_info().setdefault(OutputType.LastModified,
                                             super().get_last_modified())

    @contextmanager
    def make_stream(self):
        with self._get_cookie().extractfile(self.handle.relative_path) as s:
            yield s


@Handle.stock_json_handler("tar")
class TarHandle(Handle):
    type_label = "tar"
    resource_type = TarResource

    @property
    def presentation_name(self):
        return self.relative_path

    @property
    def presentation_place(self):
        return str(self.source.handle)

    @property
    def sort_key(self):
        return self.source.handle.sort_key
