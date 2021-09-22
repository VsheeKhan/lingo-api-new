import os
import uuid

from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model

ATTRIBUTE_NAME_MAP = {
    UnicodeAttribute: 'string',
    NumberAttribute: 'number',
}
BOOKS_TABLE_NAME = os.environ.get('BOOKS_TABLE_NAME')


class BaseModel(Model):
    @classmethod
    def body_schema(cls):
        excluded_attributes = ['Meta', 'attribute_values']
        excluded_attributes.extend(dir(Model))
        body_schema = {
            'type': 'object',
            'properties': {},
            'required': [],
            'additionalProperties': False
        }
        for attr_name in dir(cls):
            if attr_name in excluded_attributes:
                continue

            attr = getattr(cls, attr_name)
            if type(attr).__name__ in ['function', 'method']:
                continue

            body_schema['properties'][attr_name] = {
                'type': ATTRIBUTE_NAME_MAP[type(attr)]
            }
            if not attr.null:
                body_schema['required'].append(attr_name)
        return body_schema


class Book(BaseModel):
    id = UnicodeAttribute(null=False, default_for_new=uuid.uuid4())
    name = UnicodeAttribute(null=False)
    author = UnicodeAttribute(null=True)
    pages = NumberAttribute(null=True)

    class Meta:
        table_name = BOOKS_TABLE_NAME

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        schema['properties']['pages']['exclusiveMinimum'] = 0
        return schema
