import os
from typing import Dict, Any
from datetime import datetime
import uuid

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel


class AllergyModel(BaseModel):
    id = UnicodeAttribute(hash_key=True, null=False, default_for_new=lambda : str(uuid.uuid4()))
    Token = UnicodeAttribute(null=True)
    PatientID = UnicodeAttribute(null=False)
    AlergyType = UnicodeAttribute(null=False)
    AlergyName = UnicodeAttribute(null=False)
    AlergyOnsetDate = UnicodeAttribute(null=False)
    AlergyReactions = UnicodeAttribute(null=False)
    AllergyComments = UnicodeAttribute(null=True)
    CreatedAt = UTCDateTimeAttribute(null=True, default=datetime.now())
    UpdatedAt = UTCDateTimeAttribute(null=True)
    class Meta:
        table_name = os.environ.get('ALLERGY_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(AllergyModel, self).deserialize(attribute_values)