import os
from typing import Dict, Any

from pynamodb.attributes import UnicodeAttribute, NumberAttribute

from commons.models import BaseModel


class Book(BaseModel):
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
        # Placeholder for adding custom deserialization
        super(Book, self).deserialize(attribute_values)
