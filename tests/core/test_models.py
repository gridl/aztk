import pytest
from enum import Enum
from aztk.error import InvalidModelFieldError
from aztk.core.models import Model, fields

class UserState(Enum):
    Creating = "creating"
    Ready = "ready"
    Deleting = "deleting"

class UserInfo(Model):
    name = fields.String()
    age = fields.Integer()

class User(Model):
    info = fields.Nested(UserInfo)
    enabled = fields.Boolean(default=True)
    state = fields.Enum(UserState, default = UserState.Ready)

def test_models():
    user = User(
        info=UserInfo(
            name="Highlander",
            age=800,
        ),
        enabled = False,
        state = UserState.Creating,
    )

    assert user.info.name == "Highlander"
    assert user.info.age == 800
    assert user.enabled is False
    assert user.state == UserState.Creating



def test_enum_invalid_type_raise_error():
    class SimpleStateModel(Model):
        state = fields.Enum(UserState)


    with pytest.raises(InvalidModelFieldError, message="SimpleStateModel state unknown is not a valid option. Use one of ['creating', 'ready', 'deleting']"):
        obj = SimpleStateModel(state="unknown")
        obj.validate()

def test_enum_parse_string():
    class SimpleStateModel(Model):
        state = fields.Enum(UserState)

    obj = SimpleStateModel(state="creating")
    obj.validate()

    assert obj.state == UserState.Creating
