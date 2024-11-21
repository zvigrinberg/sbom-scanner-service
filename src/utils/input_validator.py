import re

PRODUCT_ID = 1
COMPONENT = 2


class InputValidator:

    def __init__(self):
        super().__init__()
        self.product_id_regex = "[a-z0-9_]+:[0-9]{1,2}(.[0-9]+)*"
        self.product_id_regex_pattern = re.compile(self.product_id_regex)
        self.component_regex = "[a-z0-9./-]+"
        self.component_regex_pattern = re.compile(self.component_regex)

    def validate(self, input_type, element: str):
        """
        Returns True if the input type is valid and the element of the type is follows the allowed pattern False otherwise.
        :param input_type:
        :param element:
        :return:
        """
        if input_type == PRODUCT_ID:
            return bool(self.product_id_regex_pattern.match(element))
        elif input_type == COMPONENT:
            return bool(self.component_regex_pattern.match(element))
        else:
            return False
