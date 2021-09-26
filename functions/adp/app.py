import requests
from requests.exceptions import ConnectionError
import untangle
from pylambdarest import route

from commons.constants import CORS_HEADERS
from .constants import adp_config


@route()
def get_security_token_lambda_handler(request):
    try:
        response = requests.post(
            '{0}/GetSecurityToken'.format(adp_config['json_api']),
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


def magic_creator():
    @route()
    def handler(request):
        try:
            response = requests.post(
                '{0}/MagicJson'.format(adp_config['json_api']),
                json={
                    'Action': request.json.get('Action'),
                    'Appname': adp_config['app_name'],
                    'Token': request.json.get('Token'),
                    'AppUserID': request.json.get('AppUserID'),
                    'PatientID': request.json.get('PatientID'),
                    'Parameter1': request.json.get('Parameter1'),
                    'Parameter2': request.json.get('Parameter2'),
                    'Parameter3': request.json.get('Parameter3'),
                    'Parameter4': request.json.get('Parameter4'),
                    'Parameter5': request.json.get('Parameter5'),
                    'Parameter6': request.json.get('Parameter6'),
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
magic_lambda_handler = magic_creator()

# # Echo
# echo_lambda_handler = magic_creator()