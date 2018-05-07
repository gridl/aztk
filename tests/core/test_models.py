from enum import Enum

import pytest

from aztk.core.models import Model, fields
from aztk.error import InvalidModelFieldError


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
    state = fields.Enum(UserState, default=UserState.Ready)

def test_models():
    user = User(
        info=UserInfo(
            name="Highlander",
            age=800,
        ),
        enabled=False,
        state=UserState.Creating,
    )

    assert user.info.name == "Highlander"
    assert user.info.age == 800
    assert user.enabled is False
    assert user.state == UserState.Creating



def test_enum_invalid_type_raise_error():
    class SimpleStateModel(Model):
        state = fields.Enum(UserState)


    with pytest.raises(
        InvalidModelFieldError,
        match="SimpleStateModel state unknown is not a valid option. Use one of \\['creating', 'ready', 'deleting'\\]"):

        obj = SimpleStateModel(state="unknown")
        obj.validate()

def test_enum_parse_string():
    class SimpleStateModel(Model):
        state = fields.Enum(UserState)

    obj = SimpleStateModel(state="creating")
    obj.validate()

    assert obj.state == UserState.Creating



def test_convert_nested_dict_to_model():
    user = User(
        info=dict(
            name="Highlander",
            age=800,
        ),
        enabled=False,
        state="deleting",
    )
    assert isinstance(user.info, UserInfo)
    assert user.info.name == "Highlander"
    assert user.info.age == 800
    assert user.enabled is False
    assert user.state == UserState.Deleting

def test_raise_error_if_missing_required_field():
    class SimpleRequiredModel(Model):
        name = fields.String()

    missing = SimpleRequiredModel()

    with pytest.raises(InvalidModelFieldError, match="SimpleRequiredModel name is required"):
        missing.validate()

def test_raise_error_if_string_field_invalid_type():
    class SimpleStringModel(Model):
        name = fields.String()

    missing = SimpleStringModel(name=123)

    with pytest.raises(InvalidModelFieldError, match="SimpleStringModel name 123 should be a string"):
        missing.validate()

def test_raise_error_if_int_field_invalid_type():
    class SimpleIntegerModel(Model):
        age = fields.Integer()

    missing = SimpleIntegerModel(age='123')

    with pytest.raises(InvalidModelFieldError, match="SimpleIntegerModel age 123 should be an integer"):
        missing.validate()

def test_raise_error_if_bool_field_invalid_type():
    class SimpleBoolModel(Model):
        enabled = fields.Boolean()

    missing = SimpleBoolModel(enabled="false")

    with pytest.raises(InvalidModelFieldError, match="SimpleBoolModel enabled false should be a boolean"):
        missing.validate()
