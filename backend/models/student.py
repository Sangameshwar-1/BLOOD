from mongoengine import StringField, IntField
from .base import TimestampedDocument

class Student(TimestampedDocument):
    name = StringField(required=True)
    age = IntField(required=True)
    branch = StringField(required=True)
    
    def to_json(self):
        data = {
            "id": str(self.id),
            "name": self.name,
            "age": self.age,
            "branch": self.branch
        }
        # Add timestamp fields
        data.update(self.get_timestamp_fields())
        return data