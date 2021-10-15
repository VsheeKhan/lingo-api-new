import os
from datetime import datetime
from typing import Dict, Any

from pynamodb.attributes import BooleanAttribute, UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel


class Contact(BaseModel):
    patient_id = UnicodeAttribute(null=False)
    adp_contact_id = UnicodeAttribute(null=True)  
    contact_relationship = UnicodeAttribute(null=False)  # TODO: ishan 15-10-2021 Use Enum to limit options
    is_patient = BooleanAttribute(null=False, default=False)
    contact_patient_id = UnicodeAttribute(null=True)  
    non_patient_first_name = UnicodeAttribute(null=True)  # TODO: ishan 15-10-2021 rename this to first_name (similar for others)
    non_patient_last_name = UnicodeAttribute(null=True)
    non_patient_age = UnicodeAttribute(null=True)
    non_patient_phone = UnicodeAttribute(null=True)  # TODO: ishan 15-10-2021 Let's research how to apply rules
    non_patient_email_address = UnicodeAttribute(null=True)  # TODO: ishan 15-10-2021 rules for email validation
    created_at = UTCDateTimeAttribute(null=True, default=datetime.now)
    updated_at = UTCDateTimeAttribute(null=True)

    class Meta:
        table_name = os.environ.get('CONTACTS_TABLE_NAME')

    @classmethod
    def body_schema(cls):
        schema = super().body_schema()
        return schema

    def deserialize(self, attribute_values: Dict[str, Dict[str, Any]]) -> None:
        # Placeholder for adding custom deserialization
        super(Contact, self).deserialize(attribute_values)
