from mongoengine import Document, StringField

class Volunteer(Document):
    name = StringField(required=True)
    contact = StringField(required=True)
    availability = StringField(required=True)
    
    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "contact": self.contact,
            "availability": self.availability
        }