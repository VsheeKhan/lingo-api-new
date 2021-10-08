from pylambdarest import route
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError

from commons.constants import CORS_HEADERS
from .models import Allergy

@route(body_schema = Allergy.body_schema())
def allergy_create_lambda_handler(request):
    allergy = Allergy()
    allergy.deserialize(request.json)
    allergy.save()
    return 201, allergy.serialize(), CORS_HEADERS


@route()
def allergy_list_lambda_handler():
    allergies = [a.serialize() for a in Allergy.scan(limit=10)]
    return 200, allergies, CORS_HEADERS


@route()
def allergy_delete_lambda_handler(pk):
    try:
        allergy = Allergy.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    try:
        allergy.delete()
    except DeleteError as error:
        print(error)
        return 500, error.cause_response_message, CORS_HEADERS

    return 200, None, CORS_HEADERS


@route()
def allergy_get_lambda_handler(pk):
    try:
        allergy = Allergy.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, allergy.serialize(), CORS_HEADERS


@route(body_schema = Allergy.body_schema())
def allergy_update_lambda_handler(request):
    try:
        allergy = Allergy()
        updateData = allergy.deserialize(request.json)
        allergy.update(Key={
            "id": updateData['id']
        },
        UpdateExpression= " set AlergyType = :AT, AlergyName = :AN, AlergyOnsetDate = :AOD, AlergyReactions = :AR, AllergyComments = :AC ", 
        ExpressionAttributeValues = {
            ":AT" : updateData['AlergyType'],
            ":AN" : updateData['AlergyName'],
            ":AOD" : updateData['AlergyOnsetDate'],
            ":AR" : updateData['AlergyReactions'],
            ":AC" : updateData['AllergyComments']
        },
        ReturnValues="UPDATED_NEW"
        )
    except UpdateError as error:
        return 500, error, CORS_HEADERS
    return 200, {}, CORS_HEADERS
