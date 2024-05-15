import structlog
from lxml.etree import ParserError

from .types import OutputType
from .registry import conversion
from ..model.utilities.crawler import (parse_html, make_outlinks)

logger = structlog.get_logger("engine2")


@conversion(OutputType.Links, "text/html")
def links_processor(r, **kwargs):
    """return a list of links found on the given resource"""
    with r.make_stream() as fp:
        try:
            content = fp.read().decode()
            html = parse_html(content, str(r.handle))
            return [
                    link for _, link in make_outlinks(html)
                    if link.url.startswith("http")]
        except ParserError:
            logger.error("Conversion error while extracting links",
                         exc_info=True)
            return None
