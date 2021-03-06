import os
from datetime import datetime
from typing import Dict, Any

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel


class Allergy(BaseModel):
    patient_id = UnicodeAttribute(null=False)
    allergy_type = UnicodeAttribute(null=False)  # TODO: ishan 12-10-2021 Control input via Enum/fixed values
    allergy_name = UnicodeAttribute(null=False)  # TODO: ishan 12-10-2021 Control input via Enum/fixed values
    allergy_onset_date = UnicodeAttribute(null=False)  # TODO: ishan 12-10-2021 Control input format
    allergy_reactions = UnicodeAttribute(null=False)
    allergy_comments = UnicodeAttribute(null=True)
    allergen_id = UnicodeAttribute(null=False)  # TODO: ishan 12-10-2021 this should be fixed to the possible values from ADP
    created_at = UTCDateTimeAttribute(null=True, default=datetime.now)
    updated_at = UTCDateTimeAttribute(null=True)  # TODO: ishan 12-10-2021 This needs to be auto-filled

    class Meta:
        table_name = os.environ.get('ALLERGY_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(Allergy, self).deserialize(attribute_values)
