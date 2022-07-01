from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)  # not dumping, loading!
        dump_only = ("id", "activated")
        load_instance = True

    # id = fields.Int()
    # username = fields.Str(required=True)
    # password = fields.Str(required=True)
