import json

from pylambdarest import route
from pylambdarest.request import Request as PyLambdaRequest
from pynamodb.exceptions import DoesNotExist, DeleteError

from adp.app import magic_handler
from adp.constants import ApiType
from commons.constants import CORS_HEADERS
from .models import Allergy

allergy_create_body_schema = Allergy.body_schema()
allergy_create_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}
allergy_create_body_schema['properties']['allergen_id'] = {
    "type": "object",
    "S": "string"
}


@route(body_schema=allergy_create_body_schema)
def allergy_create_lambda_handler(request):
    json_request = request.json
    allergy = Allergy()
    allergy.deserialize(request.json)
    allergy.save()
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "terry",
            "PatientID": json_request['patient_id']['S'],
            "Parameter1": "",
            "Parameter2": json_request['allergen_id']['S'] or "HISTORY/24045",  # TODO ishan 12-10-2021 fallback for now, but make it mandatory for the client
            "Parameter3": "",
            "Parameter4": "",
            "Parameter6": json_request['allergy_comments']['S']
        })
    })
    adp_response = magic_handler(request=adp_request, api_type=ApiType.PRO_EHR, action='SaveAllergy')
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


allergy_update_body_schema = Allergy.body_schema()
allergy_update_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}
allergy_update_body_schema['properties']['allergen_id'] = {
    "type": "object",
    "S": "string"
}


@route(body_schema=allergy_update_body_schema)
def allergy_update_lambda_handler(request, pk):
    json_request = request.json
    try:
        allergy = Allergy.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    allergy.allergy_type = json_request['allergy_type']['S']
    allergy.allergy_name = json_request['allergy_name']['S']
    allergy.allergy_onset_date = json_request['allergy_onset_date']['S']
    allergy.allergy_reactions = json_request['allergy_reactions']['S']
    allergy.allergy_comments = json_request['allergy_comments']['S']
    allergy.allergen_id = json_request['allergen_id']['S']
    allergy.save()
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "terry",
            "PatientID": json_request['patient_id']['S'],
            "Parameter1": "",
            "Parameter2": json_request['allergen_id'] or "HISTORY/24045",  # TODO: ishan 12-10-2021 make similar changes like create handler
            "Parameter3": "",
            "Parameter4": "",
            "Parameter6": json_request['allergy_comments']['S']
        })
    })
    adp_response = magic_handler(request=adp_request, api_type=ApiType.PRO_EHR, action='SaveAllergy')
    print(adp_response)
    return 201, allergy.serialize(), CORS_HEADERS
