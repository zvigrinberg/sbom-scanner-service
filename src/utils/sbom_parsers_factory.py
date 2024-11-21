import os

from visitor.spdx_rh_walker import SpdxJsonSbomParser

DEFAULT_PARSER_NAME = "spdx_json_sbom_parser"
SBOM_DEFAULT_PARSER = os.getenv("SBOM_DEFAULT_PARSER", DEFAULT_PARSER_NAME)
SBOM_PARSERS = {"spdx_json_sbom_parser": SpdxJsonSbomParser}


class SbomParsersFactory:

    def get_sbom_parser(self, data: any):
        return self.__get_sbom_parser(SBOM_DEFAULT_PARSER, data)

    def __get_sbom_parser(self, name: str, data: any):
        return SBOM_PARSERS.get(name)(data)
