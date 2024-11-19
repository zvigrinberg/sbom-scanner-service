import logging
import os

from werkzeug.exceptions import HTTPException
from flask import Flask, request, abort, render_template
from service import sbom_processor
from utils.constants import LOGGING_LEVEL_MAPPING, SBOM_NOT_FOUND
from utils.general import not_empty
from utils.input_validator import InputValidator, COMPONENT, PRODUCT_ID

app = Flask(__name__)
LOG_LEVEL_ENV = os.getenv('LOG_LEVEL', 'INFO')
LOG_LEVEL = LOGGING_LEVEL_MAPPING.get(LOG_LEVEL_ENV)


def analyze_response(result, product_id: str, component: str) -> tuple | str:
    """
    Analyze the response and return it as a tuple if the result is int, otherwise, if it's a string, then return it as is.
    :param product_id:
    :param component:
    :param result: either numeric error if didn't found sbom/component for product or string containing the sbom/component
           part in sbom
    :return: if the result is a string then it returns it as is ( response from service),
     otherwise, returns a tuple containing the (http code, "description")
    what is wrong
    """
    if type(result) == str or type(result) == dict or type(result) == tuple:
        return result
    elif type(result) == int:
        return 404, f"Can't find Sbom for product {product_id.split(':')[0]} {product_id.split(':')[1]}" if result == SBOM_NOT_FOUND else f"Can't find component {component} in product' sbom"


@app.route("/pull/<string:product_id>")
def download_sbom_component(product_id):
    component = request.args.get("component")
    input_validator = InputValidator()

    if not input_validator.validate(PRODUCT_ID, product_id):
        abort(400,
              f'Wrong "product_id" input format, must conform to regex pattern {input_validator.product_id_regex}')
    elif not_empty(component) and not input_validator.validate(COMPONENT, component):
        abort(400,
              f'Wrong "component" input format, must conform to regex pattern {input_validator.component_regex}')

    result = sbom_processor.process(product_id, component)
    final_result = analyze_response(result, product_id, component)
    if type(final_result) is tuple:
        code, desc = final_result
        abort(code, desc)
    else:
        return final_result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True if LOG_LEVEL_ENV == 'DEBUG' else False, port=8081)


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500
