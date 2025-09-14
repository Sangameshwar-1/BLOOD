from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import StringField
from .base import TimestampedDocument

class User(TimestampedDocument):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField()
    contact = StringField()
    address = StringField()
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_json(self):
        data = {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "contact": self.contact,
            "address": self.address
        }
        # Add timestamp fields
        data.update(self.get_timestamp_fields())
        return data