import json

from pylambdarest import route
from pylambdarest.request import Request as PyLambdaRequest
from pynamodb.exceptions import DoesNotExist, DeleteError

from adp.app import magic_handler
from adp.constants import ApiType
from commons.constants import CORS_HEADERS
from .models import Contact

contact_create_body_schema = Contact.body_schema()
contact_create_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}

@route(body_schema=contact_create_body_schema)
def contact_create_lambda_handler(request):
    json_request = request.json
    contact = Contact()
    contact.deserialize(request.json)
    contact.save()
    # adp_request = PyLambdaRequest(event={
    #     'httpMethod': 'POST',
    #     'headers': {},
    #     'body': json.dumps({
    #         "Token": json_request['token']['S'],
    #         "AppUserID": "demo1",
    #         "PatientID": json_request['patient_id']['S'],
    #         "Parameter1": "",
    #         "Parameter2": json_request['allergen_id']['S'] or "HISTORY/24045",  
    #         "Parameter3": "",
    #         "Parameter4": "",
    #         "Parameter6": json_request['contact_comments']['S']
    #     })
    # })
    # adp_response = magic_handler(request=adp_request, api_type=ApiType.PRO_PM, action='SaveContact')
    # print(adp_response)
    return 201, contact.serialize(), CORS_HEADERS


@route()
def contacts_list_lambda_handler():
    contacts = [result.serialize() for result in Contact.scan(Contact.patient_id == '36566')]
    return 200, {'items': contacts}, CORS_HEADERS


@route()
def contact_delete_lambda_handler(pk):
    try:
        contact = Contact.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    try:
        contact.delete()
    except DeleteError as error:
        print(error)
        return 500, error.cause_response_message, CORS_HEADERS

    return 200, None, CORS_HEADERS


@route()
def contact_get_lambda_handler(pk):
    try:
        contact = Contact.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, contact.serialize(), CORS_HEADERS


contact_update_body_schema = Contact.body_schema()
contact_update_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}

@route(body_schema=contact_update_body_schema)
def contact_update_lambda_handler(request, pk):
    json_request = request.json
    try:
        contact = Contact.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    contact.contact_relationship = json_request['contact_relationship']['S']
    # contact.is_patient = json_request['is_patient']['BOOL'] #TODO : confirmarion is_patient to be updated or not
    # contact.contact_patient_id = json_request['contact_patient_id']['S'] #TODO : confirmarion contact_patiet_id to be updated or not
    contact.non_patient_first_name = json_request['non_patient_first_name']['S']
    contact.non_patient_last_name = json_request['non_patient_last_name']['S']
    contact.non_patient_age = json_request['non_patient_age']['S']
    contact.non_patient_phone = json_request['non_patient_phone']['S']
    contact.non_patient_email_address = json_request['non_patient_email_address']['S']
    contact.save()
    # adp_request = PyLambdaRequest(event={
    #     'httpMethod': 'POST',
    #     'headers': {},
    #     'body': json.dumps({
    #         "Token": json_request['token']['S'],
    #         "AppUserID": "terry",
    #         "PatientID": json_request['patient_id']['S'],
    #         "Parameter1": "",
    #         "Parameter2": json_request['allergen_id'] or "HISTORY/24045",  # TODO: ishan 12-10-2021 make similar changes like create handler
    #         "Parameter3": "",
    #         "Parameter4": "",
    #         "Parameter6": json_request['contact_comments']['S']
    #     })
    # })
    # adp_response = magic_handler(request=adp_request, api_type=ApiType.PRO_EHR, action='SaveContact')
    # print(adp_response)
    return 201, contact.serialize(), CORS_HEADERS
