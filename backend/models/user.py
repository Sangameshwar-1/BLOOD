from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import Document, StringField

class User(Document):
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
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "contact": self.contact,
            "address": self.address
        }