import os

CORS_HEADERS = {
    'Access-Control-Allow-Headers': os.environ.get('ALLOW_HEADERS'),
    'Access-Control-Allow-Origin':  os.environ.get('ALLOW_ORIGIN'),
    'Access-Control-Allow-Methods': os.environ.get('ALLOW_METHODS'),
    'Access-Control-Allow-Credentials': os.environ.get('ALLOW_CREDENTIALS'),
}

adp_config = {
    'json_api': 'https://pro16ga-azure.unitysandbox.com/Unity/unityservice.svc/json/',
    'app_name': 'LingoUI.LingoUIServices.TestApp',
    'svc_username': 'Lingo-19a5-LingoUISer-test',
    'svc_password': 'L#nGb^9l5Ng4^cs%rv2ccSt%StbPp9',
    'ehr_username': 'terry', # This probably can't be a constant
    'ehr_password': 'manning', # This probably can't be a constant
    'ssl_verify': False, # TODO: ishan 23-09-2021 This should only be done for test and removed for production
}