from ma import ma
from marshmallow import pre_dump
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password",)  # Fields: skip during serial. Write only.
        dump_only = ("id", "confirmation") # Fields: skip during deserial. Read only

    @pre_dump  # dump bef UserModel to json
    def _pre_dump(self, user: UserModel, **kwargs):
        # returns most recent confirmation
        user.confirmation = [user.most_recent_confirmation]
        return user

    # id = fields.Int()
    # username = fields.Str(required=True)
    # password = fields.Str(required=True)
