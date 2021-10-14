import json

from pylambdarest import route
from pylambdarest.request import Request as PyLambdaRequest
from pynamodb.exceptions import DoesNotExist, DeleteError

from adp.app import magic_handler
from adp.constants import ApiType
from commons.constants import CORS_HEADERS
from .models import Immunization

immunization_create_body_schema = Immunization.body_schema()
immunization_create_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}
@route(body_schema = immunization_create_body_schema)
def immunization_create_lambda_handler(request):
    json_request = request.json
    immunization = Immunization()
    immunization.deserialize(request.json)
    immunization.save()
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "terry",
            "PatientID": json_request['patient_id']['S'],
            "Parameter1": "",
            "Parameter2": {
                "saveimmunization": {
                    "immunization_id": 8,
                    "status": "Complete",
                    "contact_id": "",
                    "encounter_id": "",
                    "procedure_id": "",
                    "entered_date": "",
                    "entered_by_caregiver": "terry",
                    "completed_date": "20212109",
                    "completedbycaregiver_id": "terry",
                    "facility_code": "1",
                    "reason_non_code": "0",
                    "given_date": "20212109 12:34",
                    "given_date_mask": "4",
                    "givenbycaregiver_id": "terry",
                    "comment": "This is a test.",
                    "dose_value": "0.5",
                    "dose_units": "ml",
                    "lot_number": "F1212",
                    "expiration_date": "20240410",
                    "expiration_date_mask": "3",
                    "mvxcode": "WAL",
                    "injectionroute_code": "Intramuscular",
                    "injectionsite_code": "Deltoid (Right)",
                    "informed_consent": "0",
                    "patient_positive_id": "123",
                    "historical_flag": "123",
                    "adverse_reaction_flag": "1",
                    "drug_code": "010889",
                    "ndc": "00000-0000-00",
                    "excludefromccd": "Y",
                    "historical_facility": "",
                    "vfc_no_participation": "",
                    "vis_code": "110"
                }
            }
        })
    })
    adp_response = magic_handler(request=adp_request, api_type=ApiType.PRO_EHR, action='SaveImmunization')
    print(adp_response)
    return 201, immunization.serialize(), CORS_HEADERS


@route()
def immunization_list_lambda_handler():
    immunizations = [result.serialize() for result in Immunization.scan(Immunization.patient_id == '36566')]
    return 200, {'items':immunizations}, CORS_HEADERS

@route()
def immunization_delete_lambda_handler(pk):
    try:
        immunization = Immunization.get(pk)
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
        immunization = Immunization.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, immunization.serialize(), CORS_HEADERS

immunization_update_body_schema = Immunization.body_schema()
immunization_update_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}
@route(body_schema=immunization_update_body_schema)
def immunization_update_lambda_handler(request, pk):
    json_request = request.json
    try:
        immunization = Immunization.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    immunization.immunization_name = json_request['immunization_name']['S']
    immunization.immunization_date = json_request['immunization_date']['S']
    immunization.immunization_status = json_request['immunization_status']['S']
    immunization.immunization_provider = json_request['immunization_provider']['S']
    immunization.immunization_facility = json_request['immunization_facility']['S']
    immunization.save()
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "terry",
            "PatientID": json_request['patient_id']['S'],
            "Parameter1": "",
            "Parameter2": {
                "saveimmunization": {
                    "immunization_id": 8,
                    "status": "Complete",
                    "contact_id": "",
                    "encounter_id": "",
                    "procedure_id": "",
                    "entered_date": "",
                    "entered_by_caregiver": "terry",
                    "completed_date": "20212109",
                    "completedbycaregiver_id": "terry",
                    "facility_code": "1",
                    "reason_non_code": "0",
                    "given_date": "20212109 12:34",
                    "given_date_mask": "4",
                    "givenbycaregiver_id": "terry",
                    "comment": "This is a test.",
                    "dose_value": "0.5",
                    "dose_units": "ml",
                    "lot_number": "F1212",
                    "expiration_date": "20240410",
                    "expiration_date_mask": "3",
                    "mvxcode": "WAL",
                    "injectionroute_code": "Intramuscular",
                    "injectionsite_code": "Deltoid (Right)",
                    "informed_consent": "0",
                    "patient_positive_id": "123",
                    "historical_flag": "123",
                    "adverse_reaction_flag": "1",
                    "drug_code": "010889",
                    "ndc": "00000-0000-00",
                    "excludefromccd": "Y",
                    "historical_facility": "",
                    "vfc_no_participation": "",
                    "vis_code": "110"
                }
            }
        })
    })
    adp_response = magic_handler(request=adp_request, api_type=ApiType.PRO_EHR, action='SaveImmunization')
    print(adp_response)
    return 201, immunization.serialize(), CORS_HEADERS
