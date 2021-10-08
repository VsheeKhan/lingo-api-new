from pylambdarest import route
from pynamodb.exceptions import DoesNotExist, DeleteError

from commons.constants import CORS_HEADERS
from .models import Allergy

@route(body_schema = Allergy.body_schema())
def allergy_create_lambda_handler(request):
    allergy = Allergy()
    allergy.deserialize(request.json)
    allergy.save()
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
