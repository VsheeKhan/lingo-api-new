import json

import requests
import untangle
from json2xml.json2xml import Json2xml
from json2xml.utils import readfromstring
from pylambdarest import route
from requests.exceptions import ConnectionError

from commons.constants import CORS_HEADERS
from .constants import adp_config, ApiType


# Creator functions (functions to create API(s))
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


# API(s)
# Security Token
pro_ehr_get_security_token_lambda_handler = security_token_creator(api_type=ApiType.PRO_EHR)
pro_pm_get_security_token_lambda_handler = security_token_creator(api_type=ApiType.PRO_PM)

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

# Get Patient Demographics
pro_pm_get_patient_demographics_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPatientDemographics')

# GetResources
pro_pm_get_resources_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetResources')

# GetResourceByID
pro_pm_get_resource_by_id_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetResourceByID')

# GetAvailableSchedule
pro_pm_get_available_schedule_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAvailableSchedule')

# GetSchedulingLocations
pro_pm_get_scheduling_locations_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetSchedulingLocations')

# GetSchedulingDepartments
pro_pm_get_scheduling_departments_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetSchedulingDepartments')

# SavePatient
pro_pm_save_patient_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='SavePatient',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter2'])
)

# GetSchedule
pro_pm_get_schedule_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetSchedule')

# GetScheduleByPatientID
pro_pm_get_schedule_by_patient_id_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetScheduleByPatientID')

# GetAppointmentById
pro_pm_get_appointment_by_id_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAppointmentById')

# SaveAppointment
pro_pm_save_appointment_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='SaveAppointment',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter1'])
)

# SaveForcedAppointment
pro_pm_save_forced_appointment_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='SaveForcedAppointment',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter1'])
)

# SaveMemoAppointment
pro_pm_save_memo_appointment_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='SaveMemoAppointment',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter1'])
)

# GetAppointmentTypes
pro_pm_get_appointment_types_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAppointmentTypes')

# GetAvailableTimeBlocks
pro_pm_get_available_time_blocks_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAvailableTimeBlocks')

# GetAppointmentRestrictions
pro_pm_get_appointment_restriction_types_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAppointmentRestrictions')

# GetAppointmentConfirmationResults
pro_pm_get_appointment_confirmation_results_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAppointmentConfirmationResults')

# GetAppointmentCancellationReasons
pro_pm_get_appointment_cancellation_reasons_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAppointmentCancellationReasons')

# GetAppointmentsByChangeDTTM
pro_pm_get_appointments_by_change_dttm_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='GetAppointmentsByChangeDTTM',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter6'])
)

# SetAppointmentStatus
pro_pm_set_appointment_status_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='SetAppointmentStatus')

# GetPractitioners
pro_pm_get_practitioners_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPractitioners')

# GetPractitionerSpecialties
pro_pm_get_practitioner_specialities_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPractitionerSpecialties')

# GetOperators
pro_pm_get_operators_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetOperators')

# GetPatientPolicyPCPs
pro_pm_get_patient_policy_pcps_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPatientPolicyPCPs')

# GetAccountTypes
pro_pm_get_account_types_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetAccountTypes')

# GetBatchCategories
pro_pm_get_batch_categories_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetBatchCategories')

# GetBatchDetail
pro_pm_get_batch_detail_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetBatchDetail')

# GetCarriers
pro_pm_get_carriers_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetCarriers')

# GetCoverageTypes
pro_pm_get_coverage_types_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetCoverageTypes')

# GetDepartments
pro_pm_get_departments_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetDepartments')

# GetDivisions
pro_pm_get_divisions_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetDivisions')

# GetEmployerBenefitPlan
pro_pm_get_employer_benefit_plan_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetEmployerBenefitPlan')

# GetLocations
pro_pm_get_locations_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetLocations')

# GetPatientAccountBalance
pro_pm_get_patient_account_balance_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='GetPatientAccountBalance',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter6'])
)

# GetPatientAccountBalanceCalc
pro_pm_get_patient_account_balance_calc_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPatientAccountBalanceCalc')

# GetPatientPolicy
pro_pm_get_patient_policy_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPatientPolicy')

# GetPatientSlidingFeeInfo
pro_pm_get_patient_sliding_fee_info_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPatientSlidingFeeInfo')

# GetPlacesOfService
pro_pm_get_places_of_service_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetPlacesOfService')

# GetServicesByVoucherID
pro_pm_get_services_by_voucher_id_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetServicesByVoucherID')

# GetSlidingFeeScales
pro_pm_get_sliding_fee_scales_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetSlidingFeeScales')

# GetTransactionCodes
pro_pm_get_transaction_codes_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='GetTransactionCodes')

# ReopenBatch
pro_pm_reopen_batch_lambda_handler = magic_creator(api_type=ApiType.PRO_PM, action='ReopenBatch')

# SaveChargeVoucher
pro_pm_save_charge_voucher_lambda_handler = magic_creator(
    api_type=ApiType.PRO_PM,
    action='SaveChargeVoucher',
    parameter_processor=parameter_processor_creator(xml_attributes=['Parameter6'])
)
