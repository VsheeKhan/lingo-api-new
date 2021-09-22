import os
import uuid

import boto3
from pylambdarest import route

from .models import Book

# TODO ishan 16-09-2021 migrate from boto3.client to boto3.resource
# TODO ishan 21-09-2021 migrate from boto3.client to PynamoDB and fallback to boto3.resource if PynamoDB fails
dynamodb_client = boto3.client('dynamodb')
BOOKS_TABLE_NAME = os.environ.get('BOOKS_TABLE_NAME')

CORS_HEADERS = {
    'Access-Control-Allow-Headers': os.environ.get('ALLOW_HEADERS'),
    'Access-Control-Allow-Origin':  os.environ.get('ALLOW_ORIGIN'),
    'Access-Control-Allow-Methods': os.environ.get('ALLOW_METHODS'),
    'Access-Control-Allow-Credentials': os.environ.get('ALLOW_CREDENTIALS'),
}


@route(body_schema=Book.body_schema())
def books_create_lambda_handler(request):
    book = {
        'id': {
            'S': str(uuid.uuid4())
        },
        'name': {
            'S': request.json['name']
        },
        'author': {
            'S': request.json['author']
        },
        'pages': {
            'N': str(request.json['pages'])
        },
    }
    dynamodb_client.put_item(TableName=BOOKS_TABLE_NAME, Item=book)
    return 201, book, CORS_HEADERS


@route()
def books_list_lambda_handler():
    books = dynamodb_client.scan(TableName=BOOKS_TABLE_NAME)
    return 200, books['Items'], CORS_HEADERS


@route()
def books_delete_lambda_handler(id):
    dynamodb_client.delete_item(TableName=BOOKS_TABLE_NAME, Key={
        "id": {
            "S": id
        }
    })
    return 200, None, CORS_HEADERS


@route()
def book_get_single_lambda_handler(id):
    book = dynamodb_client.get_item(
        TableName=BOOKS_TABLE_NAME,
        Key={
            'id': {
                'S': id
            },
        }
    )
    return 200, book['Item'], CORS_HEADERS
