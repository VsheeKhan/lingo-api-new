import os
import uuid
from datetime import datetime
from typing import Dict, Any

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel


class Allergy(BaseModel):
    # id = UnicodeAttribute(hash_key=True, null=False, default_for_new=lambda : str(uuid.uuid4()))
    token = UnicodeAttribute(null=True)
    patient_id = UnicodeAttribute(null=False)
    allergy_type = UnicodeAttribute(null=False)
    allergy_name = UnicodeAttribute(null=False)
    allergy_onset_date = UnicodeAttribute(null=False)
    allergy_reactions = UnicodeAttribute(null=False)
    allergy_comments = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(null=True, default=datetime.now())
    updated_at = UTCDateTimeAttribute(null=True)

    class Meta:
        table_name = os.environ.get('ALLERGY_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(Allergy, self).deserialize(attribute_values)
