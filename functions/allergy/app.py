from pylambdarest import route
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError

from commons.constants import CORS_HEADERS
# from functions.adp.constants import ApiType
from .models import AllergyModel
# from functions.adp.app import magic_handler

@route(body_schema = AllergyModel.body_schema())
def allergy_create_lambda_handler(request):
    allergy = AllergyModel()
    allergy.deserialize(request.json)
    allergy.save()
    return 201, allergy.serialize(), CORS_HEADERS


@route()
def allergy_list_lambda_handler():
    allergies = [result.serialize() for result in AllergyModel.scan(AllergyModel.PatientID == '36566')]
    return 200, {'items':allergies}, CORS_HEADERS

@route()
def allergy_delete_lambda_handler(pk):
    try:
        allergy = AllergyModel.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    try:
        allergy.delete()
    except DeleteError as error:
        print(error)
        return 500, error.cause_response_message, CORS_HEADERS

    return 200, None, CORS_HEADERS


@route()
def allergy_get_lambda_handler(pk):
    try:
        allergy = AllergyModel.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, allergy.serialize(), CORS_HEADERS


@route(body_schema = AllergyModel.body_schema())
def allergy_update_lambda_handler(request, pk):
    jsonRequest = request.json
    try:
        allergy = AllergyModel.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    allergy.AlergyType = jsonRequest['AlergyType']['S']
    allergy.AlergyName = jsonRequest['AlergyName']['S']
    allergy.AlergyOnsetDate = jsonRequest['AlergyOnsetDate']['S']
    allergy.AlergyReactions = jsonRequest['AlergyReactions']['S']
    allergy.AllergyComments = jsonRequest['AllergyComments']['S']
    allergy.save()
    # adpResponse = magic_handler(api_type=ApiType.PRO_EHR, action='SaveAllergy', request={
    # 'json': {
    #     "Token": jsonRequest['Token'],
    #     "AppUserID": "terry",
    #     "PatientID": 36566,
    #     "Parameter1": "",
    #     "Parameter2": "HISTORY/24045",
    #     "Parameter3": "",
    #     "Parameter4": "",
    #     "Parameter6": jsonRequest['AllergyComments']['S']
    #     }
    # })
    return 201, allergy.serialize(), CORS_HEADERS
