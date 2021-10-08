from pylambdarest import route
from commons.constants import CORS_HEADERS


@route()
def allergy_create_lambda_handler(request):
    return 201, {}, CORS_HEADERS


@route()
def allergy_list_lambda_handler():
    return 200, {}, CORS_HEADERS


@route()
def allergy_delete_lambda_handler(pk):
    return 200, None, CORS_HEADERS


@route()
def allergy_get_lambda_handler(pk):
    return 200, {}, CORS_HEADERS


@route()
def allergy_update_lambda_handler(pk):
    return 200, {}, CORS_HEADERS
