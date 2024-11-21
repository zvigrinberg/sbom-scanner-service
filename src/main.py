import os
from http import HTTPStatus

from werkzeug.exceptions import HTTPException
from flask import Flask, request, abort, render_template, make_response
from service import sbom_processor
from utils.constants import LOGGING_LEVEL_MAPPING, SBOM_NOT_FOUND
from utils.general import not_empty
from utils.input_validator import InputValidator, COMPONENT, PRODUCT_ID
from model.request_models import ProductIdPath, ComponentQuery
from model.response_models import SbomResponse, SbomResponsePayload

from flask_openapi3 import OpenAPI, Tag, Info, APIView, RawModel, APIBlueprint

LOG_LEVEL_ENV = os.getenv('LOG_LEVEL', 'INFO')
LOG_LEVEL = LOGGING_LEVEL_MAPPING.get(LOG_LEVEL_ENV)

info = Info(title='SBOM Scanner API', version='1.0.0')
app = OpenAPI(__name__, info=info)
api = APIBlueprint('sbom', __name__, url_prefix='/')

sbom_tag = Tag(name='sbom', description='Some Product SBOM')


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


@app.get('/sbom/<string:product_id>',
         tags=[sbom_tag],
         summary='get sbom product or component of product details',

         responses={200: SbomResponsePayload,
                    400: SbomResponse,
                    404: SbomResponse
                    }

         )
# @app.doc(summary="get sbom document for a product or component data from sbom")
def download_sbom_component(path: ProductIdPath, query: ComponentQuery):
    component = request.args.get("component")
    product_id = path.product_id
    # component = query.component
    input_validator = InputValidator()
    if not input_validator.validate(PRODUCT_ID, product_id):
        return make_response(f'Wrong "product_id" input format, must conform to regex pattern '
                             f'{input_validator.product_id_regex}', 400)

    elif not_empty(component) and not input_validator.validate(COMPONENT, component):
        return make_response(
            f'Wrong "component" input format, must conform to regex pattern {input_validator.component_regex}', 400)

    result = sbom_processor.process(product_id, component)
    final_result = analyze_response(result, product_id, component)
    if type(final_result) is tuple:
        code, desc = final_result
        response = make_response(desc, code)
        return response
    else:
        response = make_response(final_result, HTTPStatus.OK.value)
        response.mimetype = 'application/json'
        return response


app.register_api(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True if LOG_LEVEL_ENV == 'DEBUG' else False, port=8081)


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500
