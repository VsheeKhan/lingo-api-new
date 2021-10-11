import os
from typing import Dict, Any
from datetime import datetime
import uuid

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel


class ImmunizationModel(BaseModel):
    # id = UnicodeAttribute(hash_key=True, null=False, default_for_new=lambda : str(uuid.uuid4()))
    PatientID = UnicodeAttribute(null=False)
    ImmunizationName = UnicodeAttribute(null=False)
    ImmunizationDate = UnicodeAttribute(null=False)
    ImmunizationStatus = UnicodeAttribute(null=False)
    ImmunizationProvider = UnicodeAttribute(null=False)
    ImmunizationFacility = UnicodeAttribute(null=False)
    CreatedAt = UTCDateTimeAttribute(null=True, default=datetime.now())
    UpdatedAt = UTCDateTimeAttribute(null=True)
    class Meta:
        table_name = os.environ.get('IMMUNIZATION_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(ImmunizationModel, self).deserialize(attribute_values)