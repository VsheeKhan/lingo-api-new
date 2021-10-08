import os
from typing import Dict, Any

from pynamodb.attributes import UnicodeAttribute

from commons.models import BaseModel


class Allergy(BaseModel):
    PatientID = UnicodeAttribute(null=False)
    AlergyType = UnicodeAttribute(null=False)
    AlergyName = UnicodeAttribute(null=False)
    AlergyOnsetDate = UnicodeAttribute(null=False)
    AlergyReactions = UnicodeAttribute(null=False)
    AllergyComments = UnicodeAttribute(null=True)
    class Meta:
        table_name = os.environ.get('ALLERGY_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        schema['properties']['pages']['exclusiveMinimum'] = 0
        # Placeholder for adding custom schema
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(Allergy, self).deserialize(attribute_values)