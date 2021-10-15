import json

from pylambdarest import route
from pylambdarest.request import Request as PyLambdaRequest
from pynamodb.exceptions import DoesNotExist, DeleteError

from adp.app import magic_handler, parameter_processor_creator
from adp.constants import ApiType
from commons.constants import CORS_HEADERS
from .models import Contact

con_params_list = ['token', 'mi', 'gender', 'ssn', 'dob', 'street1', 'city', 'state', 'zip', 'is_guarantor', 'is_emergency_contact']

contact_create_body_schema = Contact.body_schema()
for param in con_params_list:
    contact_create_body_schema['properties'][param] = {
        "type": "object",
        "S": "string"
    }


@route(body_schema=contact_create_body_schema)
def contact_create_lambda_handler(request):
    json_request = request.json
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "demo1",
            "PatientID": int(json_request['patient_id']['S']),
            "Parameter1": 4185,  # TODO: ishan 15-10-2021 Can't hardcode this, get this from front-end
            "Parameter2": "",
            "Parameter6": {
                "contact": {
                    "lastName": json_request['non_patient_last_name']['S'],
                    "firstName": json_request['non_patient_first_name']['S'],
                    "mi": json_request['mi']['S'],
                    "suffix": "",
                    "gender": json_request['gender']['S'],
                    "ssn": json_request['ssn']['S'],
                    "dob": json_request['dob']['S'],
                    "street1": json_request['street1']['S'],
                    "street2": "",
                    "city": json_request['city']['S'],
                    "state": json_request['state']['S'],
                    "zip": json_request['zip']['S'],
                    "phone": json_request['non_patient_phone']['S'],
                    "workphone": "",
                    "workphoneext": "",
                    "cellphone": "",
                    "email": json_request['non_patient_email_address']['S'],
                    "employer": "",
                    "IsGuarantor": json_request['is_guarantor']['S'],
                    "IsEmergencyContact": json_request['is_emergency_contact']['S'],
                    "EmergencyContactRelation": "",
                    "IsSubscriber": "",
                    "CanGetStatements": "",
                    "comments": ""
                }
            }
            })
        })
    adp_status_code, adp_response, _ = magic_handler(
        request=adp_request,
        api_type=ApiType.PRO_PM,
        action='SaveAccountContact',
        parameter_processor=parameter_processor_creator(xml_attributes={
            'Parameter6': {
                'item_xml': None
            }
        })
    )
    print(adp_response)
    contact = Contact()
    contact.deserialize(request.json)
    contact.adp_contact_id = adp_response[0]['saveaccountcontactinfo'][0]['ContactID']
    contact.save()
    return 201, contact.serialize(), CORS_HEADERS


@route()
def contacts_list_lambda_handler():
    contacts = [result.serialize() for result in Contact.scan(Contact.patient_id == '36566')]  # TODO: ishan 15-10-2021 Can't hardcode this
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
    # contact.is_patient = json_request['is_patient']['BOOL'] #TODO : confirmarion is_patient to be updated or not (Just send this to front-end)
    # contact.contact_patient_id = json_request['contact_patient_id']['S'] #TODO : confirmarion contact_patiet_id to be updated or not
    contact.non_patient_first_name = json_request['non_patient_first_name']['S']
    contact.non_patient_last_name = json_request['non_patient_last_name']['S']
    contact.non_patient_age = json_request['non_patient_age']['S']
    contact.non_patient_phone = json_request['non_patient_phone']['S']
    contact.non_patient_email_address = json_request['non_patient_email_address']['S']
    contact.save()
    adp_request = PyLambdaRequest(event={
    'httpMethod': 'POST',
    'headers': {},
    'body': json.dumps({
        "Token": json_request['token']['S'],
        "AppUserID": "demo1",
        "PatientID": int(json_request['patient_id']['S']),
        "Parameter1": 4185,  # TODO: ishan 15-10-2021 can't hardcode this
        "Parameter2": int(json_request['adp_contact_id']['S']),
        "Parameter6": {
            "contact": {
                "lastName": json_request['non_patient_last_name']['S'],
                "firstName": json_request['non_patient_first_name']['S'],
                "mi": json_request['mi']['S'],
                "suffix": "",
                "gender": json_request['gender']['S'],
                "ssn": json_request['ssn']['S'],
                "dob": json_request['dob']['S'],
                "street1": json_request['street1']['S'],
                "street2": "",
                "city": json_request['city']['S'],
                "state": json_request['state']['S'],
                "zip": json_request['zip']['S'],
                "phone": json_request['non_patient_phone']['S'],
                "workphone": "",
                "workphoneext": "",
                "cellphone": "",
                "email": json_request['non_patient_email_address']['S'],
                "employer": "",
                "IsGuarantor": json_request['is_guarantor']['S'],
                "IsEmergencyContact": json_request['is_emergency_contact']['S'],
                "EmergencyContactRelation": "",
                "IsSubscriber": "",
                "CanGetStatements": "",
                "comments": ""
            }
        }
        })
    })
    adp_status_code, adp_response, _ = magic_handler(
        request=adp_request,
        api_type=ApiType.PRO_PM,
        action='SaveAccountContact',
        parameter_processor=parameter_processor_creator(xml_attributes={
            'Parameter6': {
                'item_xml': None
            }
        })
    )
    print(adp_response)
    return 201, contact.serialize(), CORS_HEADERS
