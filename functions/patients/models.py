import os
from typing import Dict, Any
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel

class Patient(BaseModel):
    patient_id = UnicodeAttribute(null=True)
    first_name = UnicodeAttribute(null=False)
    last_name = UnicodeAttribute(null=False)
    middle_initial = UnicodeAttribute(null=True)
    suffix = UnicodeAttribute(null=True)
    dob = UnicodeAttribute(null=True)
    birth_sex = UnicodeAttribute(null=True)
    sexual_orientation = UnicodeAttribute(null=True)
    other_sexual_orientation = UnicodeAttribute(null=True)
    gender_identify = UnicodeAttribute(null=True)
    other_gender_identity = UnicodeAttribute(null=True)
    street1 = UnicodeAttribute(null=True)
    street2 = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)
    state = UnicodeAttribute(null=True)
    zip_code = UnicodeAttribute(null=True)
    mobile_phone = UnicodeAttribute(null=True)
    home_phone = UnicodeAttribute(null=True)
    work_phone = UnicodeAttribute(null=True)
    work_phone_ext = UnicodeAttribute(null=True)
    email_address = UnicodeAttribute(null=True)
    marital_status = UnicodeAttribute(null=True)
    ssn = UnicodeAttribute(null=True)
    race = UnicodeAttribute(null=True)
    other_race = UnicodeAttribute(null=True)
    primary_language = UnicodeAttribute(null=True)
    date_registered = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(null=True, default=datetime.now)
    updated_at = UTCDateTimeAttribute(null=True)
    class Meta:
        table_name = os.environ.get('PATIENTS_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(Patient, self).deserialize(attribute_values)

