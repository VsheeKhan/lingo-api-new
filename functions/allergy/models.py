import os
from typing import Dict, Any

from commons.models import BaseModel


class Allergy(BaseModel):
    class Meta:
        table_name = os.environ.get('ALLERGY_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        # Placeholder for adding custom schema
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(Allergy, self).deserialize(attribute_values)