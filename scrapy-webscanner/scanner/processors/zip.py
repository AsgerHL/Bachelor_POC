"""Zip file processors."""

from processor import Processor
import subprocess


class ZipProcessor(Processor):

    """A processor which can handle zip-compressed files using unzip."""

    item_type = "zip"

    def handle_spider_item(self, data, url_object):
        """Add the item to the queue."""
        return self.add_to_queue(data, url_object)

    def handle_queue_item(self, item):
        """Conver the queue item."""
        return self.convert_queue_item(item)

    def convert(self, item, tmp_dir):
        """Extract the item using unzip."""
        return_code = subprocess.call(
            ["unzip", "-o", "-q", "-d", tmp_dir, item.file_path]
        )
        return return_code == 0

Processor.register_processor(ZipProcessor.item_type, ZipProcessor)
