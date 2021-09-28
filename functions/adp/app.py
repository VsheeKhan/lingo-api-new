import json

import requests
import untangle
from json2xml.json2xml import Json2xml
from json2xml.utils import readfromstring
from pylambdarest import route
from requests.exceptions import ConnectionError

from commons.constants import CORS_HEADERS
from .constants import adp_config, ApiType


def security_token_creator(api_type=None):
    if api_type is None:
        raise TypeError('api_type cannot be None')
    if not isinstance(api_type, ApiType):
        return TypeError(f'api_type should be of type: {ApiType}')

    @route()
    def handler(request):
        try:
            response = requests.post(
                f'{adp_config["json_api"][api_type]}/GetSecurityToken',
                json={
                    "Username": adp_config['svc_username'],
                    "Password": adp_config['svc_password']
                },
                verify=adp_config['ssl_verify']
            )
        except ConnectionError as error:
            print(error)
            return 500, str(error), CORS_HEADERS

        token_result = untangle.parse(response.text)
        token = token_result.GetSecurityTokenResponse.GetSecurityTokenResult.cdata
        return 200, {
            'GetSecurityTokenResult': token
        }, CORS_HEADERS

    return handler


# Security Token
pro_ehr_get_security_token_lambda_handler = security_token_creator(api_type=ApiType.PRO_EHR)
pro_pm_get_security_token_lambda_handler = security_token_creator(api_type=ApiType.PRO_PM)


def magic_creator(api_type=None, action=None, parameter_processor=lambda name, value: value):
    if api_type is None:
        raise TypeError('api_type cannot be None')
    if not isinstance(api_type, ApiType):
        return TypeError(f'api_type should be of type: {ApiType}')

    @route()
    def handler(request):
        try:
            response = requests.post(
                f'{adp_config["json_api"][api_type]}/MagicJson',
                json={
                    'Action': action or request.json.get('Action'),
                    'Appname': adp_config['app_name'],
                    'Token': request.json.get('Token'),
                    'AppUserID': request.json.get('AppUserID'),
                    'PatientID': request.json.get('PatientID'),
                    'Parameter1': parameter_processor('Parameter1', request.json.get('Parameter1')),
                    'Parameter2': parameter_processor('Parameter2', request.json.get('Parameter2')),
                    'Parameter3': parameter_processor('Parameter3', request.json.get('Parameter3')),
                    'Parameter4': parameter_processor('Parameter4', request.json.get('Parameter4')),
                    'Parameter5': parameter_processor('Parameter5', request.json.get('Parameter5')),
                    'Parameter6': parameter_processor('Parameter6', request.json.get('Parameter6')),
                },
                verify=adp_config['ssl_verify']
            )
        except ConnectionError as error:
            print(error)
            return 500, str(error), CORS_HEADERS

        if int(response.status_code / 100) != 2:
            response_content = response.text
        else:
            response_content = response.json()
        return response.status_code, response_content, CORS_HEADERS

    return handler


# Magic (generic)
pro_ehr_magic_lambda_handler = magic_creator(api_type=ApiType.PRO_EHR)
pro_pm_magic_lambda_handler = magic_creator(api_type=ApiType.PRO_PM)

# Echo
pro_ehr_echo_lambda_handler = magic_creator(api_type=ApiType.PRO_EHR, action='Echo')
pro_pm_echo_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='Echo')

# Get User Authentication
pro_ehr_get_user_authentication_lambda_handler = magic_creator(api_type=ApiType.PRO_EHR, action='GetUserAuthentication')
pro_pm_get_user_authentication_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetUserAuthentication')

# Search Patients
pro_ehr_search_patients_lambda_handler = magic_creator(api_type=ApiType.PRO_EHR, action='SearchPatients')
pro_pm_search_patients_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='SearchPatients')

def parameter_processor_creator(xml_attributes=None):
    xml_attributes = xml_attributes or []
    # Check for iterable of strings
    if not isinstance(xml_attributes, list):
        raise TypeError('xml_attributes must be a list of strings')

    def json_to_partial_xml(value):
        value_json = readfromstring(json.dumps(value))
        value_xml = Json2xml(value_json, attr_type=False, item_wrap=False).to_xml()
        stripped_xml_lines = value_xml.split('\n')[2:-2]
        return "".join(stripped_xml_lines).replace('\t', '')  # Remove \t to reduce bandwidth consumption

    def handler(name, value):
        if name not in xml_attributes:
            return value
        return json_to_partial_xml(value)

    return handler


# Save Patient
pro_pm_save_patient_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='SavePatient',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter2'])
)
