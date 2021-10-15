import os
from datetime import datetime
from typing import Dict, Any

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel


class Immunization(BaseModel):
    patient_id = UnicodeAttribute(null=False)
    immunization_name = UnicodeAttribute(null=False)
    immunization_date = UnicodeAttribute(null=False)
    immunization_status = UnicodeAttribute(null=False)
    immunization_provider = UnicodeAttribute(null=False)
    immunization_facility = UnicodeAttribute(null=False)
    transid = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(null=True, default=datetime.now)
    updated_at = UTCDateTimeAttribute(null=True)
    class Meta:
        table_name = os.environ.get('IMMUNIZATION_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(Immunization, self).deserialize(attribute_values)