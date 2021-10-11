import json

from pylambdarest import route
from pylambdarest.request import Request as PyLambdaRequest
from pynamodb.exceptions import DoesNotExist, DeleteError

from adp.app import magic_handler
from adp.constants import ApiType
from commons.constants import CORS_HEADERS
from .models import Allergy


@route(body_schema=Allergy.body_schema())
def allergy_create_lambda_handler(request):
    json_request = request.json
    allergy = Allergy()
    allergy.deserialize(request.json)
    allergy.save()
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'PUT',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['Token']['S'],
            "AppUserID": "terry",
            "PatientID": 36566,
            "Parameter1": "",
            "Parameter2": "HISTORY/24045",
            "Parameter3": "",
            "Parameter4": "",
            "Parameter6": json_request['AllergyComments']['S']
        })
    })
    adp_response = magic_handler(api_type=ApiType.PRO_EHR, action='SaveAllergy', request=adp_request)
    print(adp_response)
    return 201, allergy.serialize(), CORS_HEADERS


@route()
def allergy_list_lambda_handler():
    allergies = [result.serialize() for result in Allergy.scan(Allergy.patient_id == '36566')]
    return 200, {'items': allergies}, CORS_HEADERS


@route()
def allergy_delete_lambda_handler(pk):
    try:
        allergy = Allergy.get(pk)
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
        allergy = Allergy.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, allergy.serialize(), CORS_HEADERS


@route(body_schema=Allergy.body_schema())
def allergy_update_lambda_handler(request, pk):
    jsonRequest = request.json
    try:
        allergy = Allergy.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    allergy.allergy_type = jsonRequest['AlergyType']['S']
    allergy.allergy_name = jsonRequest['AlergyName']['S']
    allergy.allergy_onset_date = jsonRequest['AlergyOnsetDate']['S']
    allergy.allergy_reactions = jsonRequest['AlergyReactions']['S']
    allergy.allergy_comments = jsonRequest['AllergyComments']['S']
    allergy.save()
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'PUT',
        'headers': {},
        'body': json.dumps({
            "Token": jsonRequest['Token']['S'],
            "AppUserID": "terry",
            "PatientID": 36566,
            "Parameter1": "",
            "Parameter2": "HISTORY/24045",
            "Parameter3": "",
            "Parameter4": "",
            "Parameter6": jsonRequest['AllergyComments']['S']
        })
    })
    adp_response = magic_handler(api_type=ApiType.PRO_EHR, action='SaveAllergy', request=adp_request)
    print(adp_response)
    return 201, allergy.serialize(), CORS_HEADERS
