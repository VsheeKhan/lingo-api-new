import json

from pylambdarest import route
from pylambdarest.request import Request as PyLambdaRequest
from pynamodb.exceptions import DoesNotExist, DeleteError

from adp.app import magic_handler, parameter_processor_creator
from adp.constants import ApiType
from commons.constants import CORS_HEADERS
from .models import Immunization

im_params_list = ["token", "status", "contact_id", "encounter_id", "procedure_id", "entered_date", "entered_by_caregiver", "completed_date", "completedbycaregiver_id", "facility_code", "reason_non_code", "given_date", "given_date_mask", "givenbycaregiver_id", "comment", "dose_value", "dose_units", "lot_number", "expiration_date", "expiration_date_mask", "mvxcode", "injectionroute_code", "injectionsite_code", "informed_consent", "patient_positive_id", "historical_flag", "adverse_reaction_flag", "drug_code", "ndc", "excludefromccd", "historical_facility", "vfc_no_participation", "vis_code"]

immunization_create_body_schema = Immunization.body_schema()
for param in im_params_list:
    immunization_create_body_schema['properties'][param] = {
        "type": "object",
        "S": "string"
    }
@route(body_schema = immunization_create_body_schema)
def immunization_create_lambda_handler(request):
    json_request = request.json
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "terry",
            "PatientID": int(json_request['patient_id']['S']),
            "Parameter1": "",
            "Parameter2": {
                "saveimmunization": {
                    "immunization_id": json_request['immunization_name']['S'],
                    "status": json_request['immunization_status']['S'],
                    "contact_id": "",
                    "encounter_id": "",
                    "procedure_id": "",
                    "entered_date": json_request['immunization_date']['S'],
                    "entered_by_caregiver": json_request['entered_by_caregiver']['S'],
                    "completed_date": json_request['completed_date']['S'],
                    "completedbycaregiver_id": json_request['completedbycaregiver_id']['S'],
                    "facility_code": json_request['facility_code']['S'],
                    "reason_non_code": json_request['reason_non_code']['S'],
                    "given_date": json_request['given_date']['S'],
                    "given_date_mask": json_request['given_date_mask']['S'],
                    "givenbycaregiver_id": json_request['givenbycaregiver_id']['S'],
                    "comment": json_request['comment']['S'],
                    "dose_value": json_request['dose_value']['S'],
                    "dose_units": json_request['dose_units']['S'],
                    "lot_number": json_request['lot_number']['S'],
                    "expiration_date": json_request['expiration_date']['S'],
                    "expiration_date_mask": json_request['expiration_date_mask']['S'],
                    "mvxcode": json_request['mvxcode']['S'],
                    "injectionroute_code": json_request['injectionroute_code']['S'],
                    "injectionsite_code": json_request['injectionsite_code']['S'],
                    "informed_consent": json_request['informed_consent']['S'],
                    "patient_positive_id": json_request['patient_positive_id']['S'],
                    "historical_flag": json_request['historical_flag']['S'],
                    "adverse_reaction_flag": json_request['adverse_reaction_flag']['S'],
                    "drug_code": json_request['drug_code']['S'],
                    "ndc": json_request['ndc']['S'],
                    "excludefromccd": json_request['excludefromccd']['S'],
                    "historical_facility": "",
                    "vfc_no_participation": "",
                    "vis_code": ""
                    }
                }
            })
        })
    adp_status_code, adp_response, _ = magic_handler(
        request=adp_request,
        api_type=ApiType.PRO_EHR,
        action='SaveImmunization',
        parameter_processor=parameter_processor_creator(xml_attributes={
            'Parameter2': {
                'item_xml': {
                    'top_level': 'saveimmunization',
                    'item_name': 'field'
                }
            }
        })
    )
    print(adp_response)
    immunization = Immunization()
    immunization.deserialize(request.json)
    immunization.transid = adp_response[0]['saveimmunizationinfo'][0]['transid']
    immunization.save()
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
for param in im_params_list:
    immunization_update_body_schema['properties'][param] = {
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
            "PatientID": int(json_request['patient_id']['S']),
            "Parameter1": int(json_request['transid']['S']),
            "Parameter2": {
                "saveimmunization": {
                    "immunization_id": json_request['immunization_name']['S'],
                    "status": json_request['immunization_status']['S'],
                    "contact_id": "",
                    "encounter_id": "",
                    "procedure_id": "",
                    "entered_date": json_request['immunization_date']['S'],
                    "entered_by_caregiver": json_request['entered_by_caregiver']['S'],
                    "completed_date": json_request['completed_date']['S'],
                    "completedbycaregiver_id": json_request['completedbycaregiver_id']['S'],
                    "facility_code": json_request['facility_code']['S'],
                    "reason_non_code": json_request['reason_non_code']['S'],
                    "given_date": json_request['given_date']['S'],
                    "given_date_mask": json_request['given_date_mask']['S'],
                    "givenbycaregiver_id": json_request['givenbycaregiver_id']['S'],
                    "comment": json_request['comment']['S'],
                    "dose_value": json_request['dose_value']['S'],
                    "dose_units": json_request['dose_units']['S'],
                    "lot_number": json_request['lot_number']['S'],
                    "expiration_date": json_request['expiration_date']['S'],
                    "expiration_date_mask": json_request['expiration_date_mask']['S'],
                    "mvxcode": json_request['mvxcode']['S'],
                    "injectionroute_code": json_request['injectionroute_code']['S'],
                    "injectionsite_code": json_request['injectionsite_code']['S'],
                    "informed_consent": json_request['informed_consent']['S'],
                    "patient_positive_id": json_request['patient_positive_id']['S'],
                    "historical_flag": json_request['historical_flag']['S'],
                    "adverse_reaction_flag": json_request['adverse_reaction_flag']['S'],
                    "drug_code": json_request['drug_code']['S'],
                    "ndc": json_request['ndc']['S'],
                    "excludefromccd": json_request['excludefromccd']['S'],
                    "historical_facility": "",
                    "vfc_no_participation": "",
                    "vis_code": ""
                    }
                }
            })
        })
    adp_status_code, adp_response, _ = magic_handler(
        request=adp_request,
        api_type=ApiType.PRO_EHR,
        action='SaveImmunization',
        parameter_processor=parameter_processor_creator(xml_attributes={
            'Parameter2': {
                'item_xml': {
                    'top_level': 'saveimmunization',
                    'item_name': 'field'
                }
            }
        })
    )
    print(adp_response)
    return 201, immunization.serialize(), CORS_HEADERS
