from model.core import Source, Handle, Resource

from urllib.parse import quote, urlunsplit
from hashlib import md5
from pathlib import Path
from datetime import datetime

class FilesystemSource(Source):
    def __init__(self, path):
        self._path = Path(path)
        assert self._path.is_absolute()

    def handles(self, sm):
        for d in self._path.glob("**"):
            for f in d.iterdir():
                if f.is_file():
                    yield FilesystemHandle(self, f.relative_to(self._path))

    def __str__(self):
        return "FilesystemSource({0})".format(self._path)

    def _open(self, sm):
        return self._path

    def _close(self, sm):
        pass

    def to_url(self):
        return urlunsplit(('file', '', quote(str(self._path)), None, None))

    @staticmethod
    def from_url(scheme, netloc, path=None):
        assert not netloc
        return FilesystemSource(path)

Source._register_url_handler("file", FilesystemSource.from_url)

class FilesystemHandle(Handle):
    def __init__(self, source, relpath):
        super(FilesystemHandle, self).__init__(source, relpath)

    def follow(self, sm):
        return FilesystemResource(self, sm)

class FilesystemResource(Resource):
    def __init__(self, handle, sm):
        super(FilesystemResource, self).__init__(handle, sm)
        self._full_path = \
            self._open_source().joinpath(self.get_handle().get_relative_path())
        self._hash = None
        self._stat = None

    def _open(self):
        return open(self._full_path, "rb")

    def get_hash(self):
        if not self._hash:
            with self._open() as f:
                self._hash = md5(f.read())
        return self._hash

    def get_stat(self):
        if not self._stat:
            self._stat = self._full_path.stat()
        return self._stat

    def get_last_modified(self):
        return datetime.fromtimestamp(self.get_stat().st_mtime)

    def __enter__(self):
        return str(self._full_path)

    def __exit__(self, exc_type, exc_value, traceback):
        pass
