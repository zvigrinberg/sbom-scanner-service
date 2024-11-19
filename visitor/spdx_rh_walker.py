from visitor.base_walker import BaseSbomParser
from utils.constants import COMPONENT_NOT_FOUND

class SpdxJsonSbomParser(BaseSbomParser):
    def __init__(self,
                 json_tree: dict):
        self.json = json_tree

    def walk(self, component: str) -> str:
        for package in self.json.get('packages'):
            if component == package.get('name') or component == package.get('homepage'):
                return package
        else:
            return COMPONENT_NOT_FOUND

