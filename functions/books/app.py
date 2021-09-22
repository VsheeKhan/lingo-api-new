import os

from pylambdarest import route
from pynamodb.exceptions import DoesNotExist, DeleteError

from models import Book

CORS_HEADERS = {
    'Access-Control-Allow-Headers': os.environ.get('ALLOW_HEADERS'),
    'Access-Control-Allow-Origin':  os.environ.get('ALLOW_ORIGIN'),
    'Access-Control-Allow-Methods': os.environ.get('ALLOW_METHODS'),
    'Access-Control-Allow-Credentials': os.environ.get('ALLOW_CREDENTIALS'),
}


@route(body_schema=Book.body_schema())
def books_create_lambda_handler(request):
    book = Book()
    book.deserialize(request.json)
    book.save()
    return 201, book.serialize(), CORS_HEADERS


@route()
def books_list_lambda_handler():
    books = [b.serialize() for b in Book.scan(limit=10)]
    return 200, books, CORS_HEADERS


@route()
def books_delete_lambda_handler(pk):
    try:
        book = Book.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS
    try:
        book.delete()
    except DeleteError as error:
        print(error)
        return 500, error.cause_response_message, CORS_HEADERS

    return 200, None, CORS_HEADERS


@route()
def book_get_single_lambda_handler(pk):
    try:
        book = Book.get(pk)
    except DoesNotExist:
        return 404, None, CORS_HEADERS

    return 200, book.serialize(), CORS_HEADERS
