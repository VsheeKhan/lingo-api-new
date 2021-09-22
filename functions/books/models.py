import os
import uuid
from typing import Dict, Any

from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model

ATTRIBUTE_CODE_MAP = {
    UnicodeAttribute: {
        'rest': 'string',
        'db': 'S',
    },
    NumberAttribute: {
        'rest': 'number',
        'db': 'N',
    },
}


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
                'type': 'object',
                ATTRIBUTE_CODE_MAP[type(attr)]['db']: ATTRIBUTE_CODE_MAP[type(attr)]['rest']
            }
            if not attr.null and not attr.default_for_new:
                body_schema['required'].append(attr_name)
        return body_schema


class Book(BaseModel):
    id = UnicodeAttribute(hash_key=True, null=False, default_for_new=lambda : str(uuid.uuid4()))
    name = UnicodeAttribute(null=False)
    author = UnicodeAttribute(null=True)
    pages = NumberAttribute(null=True)

    class Meta:
        table_name = os.environ.get('BOOKS_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        schema['properties']['pages']['exclusiveMinimum'] = 0
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        body = attribute_values
        # update with 'id'
        body['id'] = {
            'S': self.id,
        }
        super(Book, self).deserialize(attribute_values)
