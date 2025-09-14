from mongoengine import StringField
from .base import TimestampedDocument

class Volunteer(TimestampedDocument):
    name = StringField(required=True)
    contact = StringField(required=True)
    availability = StringField(required=True)
    
    def to_json(self):
        data = {
            "id": str(self.id),
            "name": self.name,
            "contact": self.contact,
            "availability": self.availability
        }
        # Add timestamp fields
        data.update(self.get_timestamp_fields())
        return data