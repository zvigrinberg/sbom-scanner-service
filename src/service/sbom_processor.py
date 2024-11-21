

import orjson

from utils.constants import SBOM_NOT_FOUND
from utils.general import not_empty
from utils.unpack import unpack_bz2
from utils.sbom_downloader import download
from utils.sbom_parsers_factory import SbomParsersFactory


def process(product_id: str, component: str) -> dict | str | int:
    buffer = download(product_id)
    if not buffer:
        return SBOM_NOT_FOUND
    elif type(buffer) is tuple and buffer[0] == 404:
        return SBOM_NOT_FOUND

    sbom_content = unpack_bz2(buffer)
    if not_empty(component):
        sbom_object = orjson.loads(sbom_content)
        sbom_parser_factory = SbomParsersFactory()
        sbom_parser = sbom_parser_factory.get_sbom_parser(sbom_object)
        return sbom_parser.walk(component)
    else:
        return sbom_content


