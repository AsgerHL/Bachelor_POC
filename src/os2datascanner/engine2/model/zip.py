from .core import Source, Handle, FileResource
from .utilities import NamedTemporaryResource

from zipfile import ZipFile
from datetime import datetime
from contextlib import contextmanager

@Source.mime_handler("application/zip")
class ZipSource(Source):
    def __init__(self, handle):
        self._handle = handle

    def __str__(self):
        return "ZipSource({0})".format(self._handle)

    def handles(self, sm):
        zipfile = sm.open(self)
        for f in zipfile.namelist():
            if not f[-1] == "/":
                yield ZipHandle(self, f)

    def _generate_state(self, sm):
        with self._handle.follow(sm).make_path() as r:
            with ZipFile(str(r)) as zp:
                yield zp

    def to_handle(self):
        return self._handle

class ZipHandle(Handle):
    def follow(self, sm):
        return ZipResource(self, sm)

class ZipResource(FileResource):
    def __init__(self, handle, sm):
        super().__init__(handle, sm)
        self._info = None

    def get_info(self):
        if not self._info:
            self._info = self._get_cookie().getinfo(
                    str(self.get_handle().get_relative_path()))
        return self._info

    def get_hash(self):
        return self.get_info().CRC

    def get_size(self):
        return self.get_info().file_size

    def get_last_modified(self):
        return datetime(*self.get_info().date_time)

    @contextmanager
    def make_path(self):
        ntr = NamedTemporaryResource(self.get_handle().get_name())
        try:
            with ntr.open("wb") as f:
                with self.make_stream() as s:
                    f.write(s.read())
            yield ntr.get_path()
        finally:
            ntr.finished()

    @contextmanager
    def make_stream(self):
        with self._get_cookie().open(
                self.get_handle().get_relative_path()) as s:
            yield s