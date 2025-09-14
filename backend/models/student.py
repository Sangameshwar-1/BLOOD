from mongoengine import Document, StringField, IntField

class Student(Document):
    name = StringField(required=True)
    age = IntField(required=True)
    branch = StringField(required=True)
    
    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "age": self.age,
            "branch": self.branch
        }