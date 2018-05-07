from aztk.core.models import Model, fields

class UserInfo(Model):
    name = fields.String()
    age = fields.Integer()

class User(Model):
    info = fields.Nested(UserInfo)
    enabled = fields.Boolean(default=True)


def test_models():
    user = User(
        info=UserInfo(
            name="Highlander",
            age=800,
        ),
        enabled = False,
    )

    assert user.info.name == "Highlander"
    assert user.info.age == 800
    assert user.enabled is False
