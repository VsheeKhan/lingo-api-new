import requests
import untangle
from pylambdarest import route
from requests.exceptions import ConnectionError

from commons.constants import CORS_HEADERS
from .constants import adp_config, ApiType


def security_token_creator(api_type=None):
    if api_type is None:
        raise TypeError
    if not isinstance(api_type, ApiType):
        return ValueError

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


def magic_creator(api_type=None, action=None, parameter_processor=lambda x: x):
    if api_type is None:
        raise TypeError
    if not isinstance(api_type, ApiType):
        return ValueError

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
                    'Parameter1': parameter_processor(request.json.get('Parameter1')),
                    'Parameter2': parameter_processor(request.json.get('Parameter2')),
                    'Parameter3': parameter_processor(request.json.get('Parameter3')),
                    'Parameter4': parameter_processor(request.json.get('Parameter4')),
                    'Parameter5': parameter_processor(request.json.get('Parameter5')),
                    'Parameter6': parameter_processor(request.json.get('Parameter6')),
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
