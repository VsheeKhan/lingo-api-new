import json

from pylambdarest import route
from pylambdarest.request import Request as PyLambdaRequest
from pynamodb.exceptions import DoesNotExist, DeleteError

from adp.app import magic_handler, parameter_processor_creator
from adp.constants import ApiType
from commons.constants import CORS_HEADERS
from .models import Patient

patient_create_body_schema = Patient.body_schema()
patient_create_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}
patient_create_body_schema['properties']['adp_birth_sex'] = {
    "type": "object",
    "S": "string"
}
patient_create_body_schema['properties']['adp_marital_status'] = {
    "type": "object",
    "S": "string"
}


@route(body_schema = patient_create_body_schema)
def patient_create_lambda_handler(request):
    json_request = request.json
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "demo1",  # TODO: ishan 14-10-2021 Move this value to the front-end
            "Parameter2": {
                "patient": {
                    "patientID": "",
                    "lastName": json_request['last_name']['S'],
                    "firstName": json_request['first_name']['S'],
                    "mi": json_request['middle_initial']['S'],
                    "suffix": json_request['suffix']['S'],
                    "gender": json_request['adp_birth_sex']['S'],
                    "ssn": json_request['ssn']['S'],
                    "dob": json_request['dob']['S'],
                    "street1": json_request['street1']['S'],
                    "street2": json_request['street2']['S'],
                    "city": json_request['city']['S'],
                    "state": json_request['state']['S'],
                    "zip": json_request['zip_code']['S'],
                    "phone": json_request['home_phone']['S'],
                    "primaryphone": json_request['home_phone']['S'],
                    "workphone": json_request['work_phone']['S'],
                    "workphoneext": json_request['work_phone_ext']['S'],
                    "cellphone": json_request['mobile_phone']['S'],
                    "email": json_request['email_address']['S'],
                    "maritalstatus": json_request['adp_marital_status']['S'],
                    "HIPAAStmtExp": "5/5/2020",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "usualprov": "MARFEE",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "referringdr": "MARFEE",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "pcp": "MARFEE",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "employer": "AHS",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "employmentstatus": "",
                    "studentstatus": "",
                    "IsGuarantor": "",
                    "RelationToGuarantor": "",
                    "IsEmergencyContact": "",
                    "EmergencyContactRelation": "",
                    "AccountType": "",
                    "PatientComments": "",
                    "MedRecLoc": ""
                }
            }
        })
    })
    adp_status_code, adp_response, _ = magic_handler(
        request=adp_request,
        api_type=ApiType.PRO_PM,
        action='SavePatient',
        parameter_processor=parameter_processor_creator(xml_attributes={
            'Parameter2': {
                'item_xml': None
            }
        })
    )
    print(adp_response[0]['savepatientinfo'][0]['PatientID'])
    patient = Patient()
    patient.deserialize(request.json)
    patient.patient_id = int(adp_response[0]['savepatientinfo'][0]['PatientID'])
    patient.save()
    return 201, patient.serialize(), CORS_HEADERS


@route()
def patient_delete_lambda_handler(pk):
    try:
        patient = Patient.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    try:
        patient.delete()
    except DeleteError as error:
        print(error)
        return 500, error.cause_response_message, CORS_HEADERS

    return 200, None, CORS_HEADERS


@route()
def patient_get_lambda_handler(pk):
    try:
        patient = Patient.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, patient.serialize(), CORS_HEADERS


patient_update_body_schema = Patient.body_schema()
patient_update_body_schema['properties']['token'] = {
    "type": "object",
    "S": "string"
}
patient_update_body_schema['properties']['adp_birth_sex'] = {
    "type": "object",
    "S": "string"
}
patient_update_body_schema['properties']['adp_marital_status'] = {
    "type": "object",
    "S": "string"
}


@route(body_schema = patient_update_body_schema)
def patient_update_lambda_handler(request, pk):
    json_request = request.json
    try:
        patient = Patient.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    patient.patient_id = json_request['patient_id']['N']
    patient.first_name = json_request['first_name']['S']
    patient.last_name = json_request['last_name']['S']
    patient.middle_initial = json_request['middle_initial']['S']
    patient.suffix = json_request['suffix']['S']
    patient.dob = json_request['dob']['S']
    patient.birth_sex = json_request['birth_sex']['S']
    patient.sexual_orientation = json_request['sexual_orientation']['S']
    patient.other_sexual_orientation = json_request['other_sexual_orientation']['S']
    patient.gender_identify = json_request['gender_identify']['S']
    patient.other_gender_identity = json_request['other_gender_identity']['S']
    patient.street1 = json_request['street1']['S']
    patient.street2 = json_request['street2']['S']
    patient.city = json_request['city']['S']
    patient.state = json_request['state']['S']
    patient.zip_code = json_request['zip_code']['S']
    patient.mobile_phone = json_request['mobile_phone']['S']
    patient.home_phone = json_request['home_phone']['S']
    patient.work_phone = json_request['work_phone']['S']
    patient.work_phone_ext = json_request['work_phone_ext']['S']
    patient.email_address = json_request['email_address']['S']
    patient.marital_status = json_request['marital_status']['S']
    patient.ssn = json_request['ssn']['S']
    patient.race = json_request['race']['S']
    patient.other_race = json_request['other_race']['S']
    patient.primary_language = json_request['primary_language']['S']
    patient.date_registered = json_request['date_registered']['S']
    patient.save()
    adp_request = PyLambdaRequest(event={
        'httpMethod': 'POST',
        'headers': {},
        'body': json.dumps({
            "Token": json_request['token']['S'],
            "AppUserID": "demo1",  # TODO: ishan 14-10-2021 Move this value to the front-end
            "Parameter2": {
                "patient": {
                    "patientID": json_request['patient_id']['N'],
                    "lastName": json_request['last_name']['S'],
                    "firstName": json_request['first_name']['S'],
                    "mi": json_request['middle_initial']['S'],
                    "suffix": json_request['suffix']['S'],
                    "gender": json_request['adp_birth_sex']['S'],
                    "ssn": json_request['ssn']['S'],
                    "dob": json_request['dob']['S'],
                    "street1": json_request['street1']['S'],
                    "street2": json_request['street2']['S'],
                    "city": json_request['city']['S'],
                    "state": json_request['state']['S'],
                    "zip": json_request['zip_code']['S'],
                    "phone": json_request['home_phone']['S'],
                    "primaryphone": json_request['home_phone']['S'],
                    "workphone": json_request['work_phone']['S'],
                    "workphoneext": json_request['work_phone_ext']['S'],
                    "cellphone": json_request['mobile_phone']['S'],
                    "email": json_request['email_address']['S'],
                    "maritalstatus": json_request['adp_marital_status']['S'],
                    "HIPAAStmtExp": "5/5/2020",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "usualprov": "MARFEE",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "referringdr": "MARFEE",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "pcp": "MARFEE",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "employer": "AHS",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "employmentstatus": "",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "studentstatus": "",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "IsGuarantor": "",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "RelationToGuarantor": "",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "IsEmergencyContact": "",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "EmergencyContactRelation": "",  # TODO: ishan 14-10-2021 Move this value to the front-end
                    "AccountType": "",
                    "PatientComments": "",
                    "MedRecLoc": ""
                }
            }
        })
    })
    adp_response = magic_handler(
        request=adp_request,
        api_type=ApiType.PRO_PM,
        action='SavePatient',
        parameter_processor=parameter_processor_creator(xml_attributes={
            'Parameter2': {
                'item_xml': None
            }
        })
    )
    print(adp_response)
    return 201, patient.serialize(), CORS_HEADERS
