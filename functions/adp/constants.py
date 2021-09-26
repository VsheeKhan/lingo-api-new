import os

adp_config = {
    'json_api': 'https://pro16ga-azure.unitysandbox.com/Unity/unityservice.svc/json/',
    'app_name': 'LingoUI.LingoUIServices.TestApp',
    'svc_username': 'Lingo-19a5-LingoUISer-test',
    'svc_password': 'L#nGb^9l5Ng4^cs%rv2ccSt%StbPp9',
    'ssl_verify': os.environ.get('ENVIRONMENT') == 'DEV',
}