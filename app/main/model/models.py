from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    """User class"""

    Email = db.StringField(max_length=160, unique=True, required=True)
    Password = db.StringField(max_length=300, required=True)
    occupation = db.ReferenceField("Occupation", on_delete=db.CASCADE)
    category = db.ReferenceField("Category", on_delete=db.CASCADE)
    activate = db.BooleanField(default=False)
    image = db.ImageField(null=True, required=False)

    def __str__(self):
        return f"User( Email={self.Email}, Occupation={self.occupation}, Category={self.category.Name}, activate={self.activate} )"

    def get_id_str(self):
        return str(self.id)


class Tokens(db.Document):
    """Token class"""

    token = db.StringField(max_length=300, null=True)  # refresh token
    activationToken = db.StringField(max_length=300, null=True)  # activate token
    userId = db.ReferenceField(User, on_delete=db.CASCADE)

    def __str__(self):
        return f"Token( activationToken={self.activationToken}, token={self.token}, userId={self.userId} )"


class Category(db.Document):
    """Category class"""

    Name = db.StringField(max_length=100, unique=True, required=True)
    english_name = db.StringField(max_length=100, unique=True, null=True, required=False)

    def __str__(self):
        return f"Category( Name={self.Name} )"


class Occupation(db.Document):
    """Occupation class"""

    Name = db.StringField(max_length=100, unique=True, required=True)
    english_name = db.StringField(max_length=100, unique=True, null=True, required=False)

    def __str__(self):
        return f"Occupation( Name={self.Name} )"
