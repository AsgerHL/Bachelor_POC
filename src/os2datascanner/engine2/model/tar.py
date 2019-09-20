from .core import Source, Handle, FileResource
from .utilities import NamedTemporaryResource

from tarfile import open as open_tar
from datetime import datetime
from contextlib import contextmanager

@Source.mime_handler("application/x-tar")
class TarSource(Source):
    def __init__(self, handle):
        self._handle = handle

    def __str__(self):
        return "TarSource({0})".format(self._handle)

    def handles(self, sm):
        tarfile = sm.open(self)
        for f in tarfile.getmembers():
            if f.isfile():
                yield TarHandle(self, f.name)

    def _generate_state(self, sm):
        with self._handle.follow(sm).make_path() as r:
            with open_tar(str(r), "r") as tp:
                yield tp

class TarHandle(Handle):
    def follow(self, sm):
        return TarResource(self, sm)

class TarResource(FileResource):
    def __init__(self, handle, sm):
        super().__init__(handle, sm)
        self._info = None

    def get_info(self):
        if not self._info:
            self._info = self._get_cookie().getmember(
                    self.get_handle().get_relative_path())
        return self._info

    def get_hash(self):
        return self.get_info().chksum

    def get_size(self):
        return self.get_info().size

    def get_last_modified(self):
        return datetime.fromtimestamp(self.get_info().mtime)

    @contextmanager
    def make_path(self):
        ntr = NamedTemporaryResource(Path(self.get_handle().get_name()))
        try:
            with ntr.open("wb") as f:
                with self.make_stream() as s:
                    f.write(s.read())
            yield ntr.get_path()
        finally:
            ntr.finished()

    @contextmanager
    def make_stream(self):
        with self._get_cookie().extractfile(
                 self.get_handle().get_relative_path()) as s:
            yield s
