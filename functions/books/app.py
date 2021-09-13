import json
import boto3
import uuid
import os

dynamodb_client = boto3.client('dynamodb')
TABLE_NAME = os.environ.get("BOOKS_TABLE_NAME")


def books_create_lambda_handler(event, context):
    print(json.dumps(event))
    body = json.loads(event['body'])

    book = {
        'id': {
            'S': str(uuid.uuid4())
        },
        'name': {
            'S': body['name']
        },
        'author': {
            'S': body['author']
        },
        'pages': {
            'N': str(body['pages'])
        },
    }
    dynamodb_client.put_item(TableName=TABLE_NAME, Item=book)

    return {
        "isBase64Encoded": False,
        "statusCode": 201,
        "headers": {},
        "multiValueHeaders": {},
        "body": json.dumps(book)
    }


def books_list_lambda_handler(event, context):
    books = dynamodb_client.scan(TableName=TABLE_NAME)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "multiValueHeaders": {},
        "body": json.dumps(books)
    }


def books_delete_lambda_handler(event, context):
    dynamodb_client.delete_item(TableName=TABLE_NAME, Key={
        "id": {
            "S": event['pathParameters']['id']
        }
    })
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "multiValueHeaders": {},
        "body": ""
    }


def book_get_single_lambda_handler(event, context):
    book = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={
            'id': {
                'S': event['pathParameters']['id']
            },
        }
    )
    print(book)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "multiValueHeaders": {},
        "body": json.dumps(book)
    }
