from mongoengine import Document, StringField, ReferenceField, DateTimeField, FloatField

class Donor(Document):
    user_id = ReferenceField('User', required=True)
    name = StringField(required=True)
    dob = DateTimeField(required=True)
    weight = FloatField(required=True)
    blood_type = StringField(required=True)
    contact = StringField(required=True)
    address = StringField(required=True)
    district = StringField(required=True)
    
    def to_json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id.id),
            "name": self.name,
            "dob": self.dob.isoformat(),
            "weight": self.weight,
            "blood_type": self.blood_type,
            "contact": self.contact,
            "address": self.address,
            "district": self.district
        }