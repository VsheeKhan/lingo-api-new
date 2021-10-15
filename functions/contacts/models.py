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
    first_name = UnicodeAttribute(null=True)  # TODO: ishan 15-10-2021 rename this to first_name (similar for others)
    last_name = UnicodeAttribute(null=True)
    age = UnicodeAttribute(null=True)
    phone = UnicodeAttribute(null=True)  # TODO: ishan 15-10-2021 Let's research how to apply rules
    email_address = UnicodeAttribute(null=True)  # TODO: ishan 15-10-2021 rules for email validation
    created_at = UTCDateTimeAttribute(null=True, default=datetime.now)
    updated_at = UTCDateTimeAttribute(null=True)

    class Meta:
        table_name = os.environ.get('CONTACTS_TABLE_NAME')
