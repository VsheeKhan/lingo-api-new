import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from commons.models import BaseModel


class Immunization(BaseModel):
    patient_id = UnicodeAttribute(null=False)
    immunization_id = UnicodeAttribute(null=False)  # TODO: ishan 15-10-2021 map with immunization_id
    immunization_date = UnicodeAttribute(null=False)  # TODO: ishan 15-10-2021 Use UTCDateTimeAttribute (update in other places too)
    immunization_status = UnicodeAttribute(null=False)  # TODO: ishan 15-10-2021 ask from front-end (hardcode as complete if need be)
    immunization_provider = UnicodeAttribute(null=False)  # TODO: ishan 15-10-2021 map with historical_facility
    immunization_facility = UnicodeAttribute(null=False)  # TODO: ishan 15-10-2021 Map with facility_code
    trans_id = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(null=True, default=datetime.now)
    updated_at = UTCDateTimeAttribute(null=True)

    class Meta:
        table_name = os.environ.get('IMMUNIZATION_TABLE_NAME')
