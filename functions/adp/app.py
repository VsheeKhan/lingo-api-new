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
    print(token)
    return 200, {
        'GetSecurityTokenResult': token
    }, CORS_HEADERS
