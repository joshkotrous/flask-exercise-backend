import pytest
from marshmallow import ValidationError

from backend.dto.user import UserCreationSchema


@pytest.mark.parameterize(
    "password,valid",
    [{"Abcde1234", True}, {"abcde1234", False}, {"Abc", False}, {"AbCde1234", True}],
)
def test_validate_password(password, valid):
    # given
    schema = UserCreationScema()
    data = {"username": "josh", "password": password, "email": "test@gmail.com"}

    # when
    try:
        user = schema.load(data)
        assert valid
        # then
        assert user is not None
        assert user.username == data["username"]
        assert user.password == data["password"]
        assert user.email == data["email"]
    except ValidationError:
        assert not valid


def test_missing_fields():
    # given
    schema = UserCreationSchema()
    data = {"username": "test", "password": "Abcde1234"}

    # when
    with pytest.raises(ValidationError):
        schema.load(data)
