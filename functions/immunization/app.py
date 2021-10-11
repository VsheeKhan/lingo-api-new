from pylambdarest import route
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError

from commons.constants import CORS_HEADERS
from .models import ImmunizationModel

@route(body_schema = ImmunizationModel.body_schema())
def immunization_create_lambda_handler(request):
    immunization = ImmunizationModel()
    immunization.deserialize(request.json)
    immunization.save()
    return 201, immunization.serialize(), CORS_HEADERS


@route()
def immunization_list_lambda_handler():
    immunizations = [result.serialize() for result in ImmunizationModel.scan(ImmunizationModel.PatientID == '36566')]
    return 200, {'items':immunizations}, CORS_HEADERS

@route()
def immunization_delete_lambda_handler(pk):
    try:
        immunization = ImmunizationModel.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    try:
        immunization.delete()
    except DeleteError as error:
        print(error)
        return 500, error.cause_response_message, CORS_HEADERS

    return 200, None, CORS_HEADERS


@route()
def immunization_get_lambda_handler(pk):
    try:
        immunization = ImmunizationModel.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, immunization.serialize(), CORS_HEADERS


@route(body_schema = ImmunizationModel.body_schema())
def immunization_update_lambda_handler(request):
    # try:
    #     immunization = ImmunizationModel.get(pk)
    # except DoesNotExist:
    #     return 404, None, CORS_HEADERS
    immunization = ImmunizationModel()
    immunization.deserialize(request.json)
    immunization.save()
    return 201, immunization.serialize(), CORS_HEADERS
