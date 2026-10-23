from unittest.mock import Mock, patch
import pytest
from src.utils import eleva_quadrado, requires_role
from http import HTTPStatus

@pytest.mark.parametrize("test_input, expected", [(2,4), (3,9), (5,25)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected

@pytest.mark.parametrize(
        "test_input, exc_class,msg",
        [
            ("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'" ),
            (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'"),
        ]
    )
def test_eleva_quadrado_falha_string(test_input, exc_class,msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
    assert str(exc.value) == msg

def test_requires_role_success():
    mock_user = Mock()
    mock_user.role.name = "admin"

    with patch("src.utils.get_jwt_identity"), patch("src.utils.db.get_or_404", return_value=mock_user):
        decorated_function = requires_role("admin")(lambda: "success")
        result = decorated_function()
    assert result == "success"

def test_requires_role_fail():
    # Given
    mock_user = Mock()
    mock_user.role.name = "normal"

    with patch("src.utils.get_jwt_identity"), patch("src.utils.db.get_or_404", return_value=mock_user):
        decorated_function = requires_role("admin")(lambda: "success")

    # When
        result = decorated_function()

    # Then
    assert result == ({"message": "User dont have access."}, HTTPStatus.FORBIDDEN)