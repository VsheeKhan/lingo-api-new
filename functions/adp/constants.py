import os
from enum import Enum, unique, auto


@unique
class ApiType(Enum):
    PRO_EHR = auto()  # Professional EHR 16 GA
    PRO_PM = auto()  # Pro-PM DEV Practice Management 14.0.2


adp_config = {
    'json_api': {
        ApiType.PRO_EHR: 'https://pro16ga-azure.unitysandbox.com/Unity/unityservice.svc/json/',
        ApiType.PRO_PM: 'http://propmdev-azure.unitysandbox.com/UnityPM/unityservice.svc/json/',
    },
    'app_name': 'LingoUI.LingoUIServices.TestApp',
    'svc_username': 'Lingo-19a5-LingoUISer-test',
    'svc_password': 'L#nGb^9l5Ng4^cs%rv2ccSt%StbPp9',
    # 'ssl_verify': os.environ.get('ENVIRONMENT') != 'DEV',  # Don't verify SSL if in DEV mode
    'ssl_verify': False,  # TODO ishan 27-09-2021 This is temporary for now
}
