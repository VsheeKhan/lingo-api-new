import requests
import untangle
from pylambdarest import route

from constants import CORS_HEADERS, adp_config


@route()
def get_security_token_lambda_handler(request):
    response = requests.post(
        '{0}/GetSecurityToken'.format(adp_config['json_api']),
        json={
            "Username": adp_config['svc_username'],
            "Password": adp_config['svc_password']
        },
        verify=adp_config['ssl_verify']
    )
    token_result = untangle.parse(response.text)
    token = token_result.GetSecurityTokenResponse.GetSecurityTokenResult.cdata
    return 200, {
        'GetSecurityTokenResult': token
    }, CORS_HEADERS


@route()
def magic_lambda_handler(request):
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
    if int(response.status_code / 100) != 2:
        return response.status_code, response.text, CORS_HEADERS

    return response.status_code, response.json(), CORS_HEADERS