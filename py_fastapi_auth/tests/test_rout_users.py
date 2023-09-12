from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    """
     Функція маркера використовується для створення користувача, підтвердження користувача, а потім входу в систему як цього
     користувача. Він повертає маркер доступу для цього користувача.
     :param client: Перевірте маршрути
     :param user: Створіть користувача для перевірки функції маркера
     :param session: Створіть новий сеанс для тесту
     :param monkeypatch: імітація функції send_email у функції token
     :return: Токен, який є рядком
     """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_read_users_me_authenticated(client, token):
    """
     Функція test_read_users_me_authenticated перевіряє, чи може користувач читати власну інформацію.
     Він робить це, спочатку висміюючи кеш redis, щоб повернути None, що спричинить потрапляння функції в базу даних.
     Потім він створює запит із заголовком авторизації, що містить дійсний маркер, і надсилає його до /api/users/me/.
     Відповідь перевіряється на наявність коду статусу 200 (ОК), а потім перевіряються дані JSON щодо імені користувача, електронної пошти, але не пароля.
     :param client: надсилайте запити до API
     :param token: передати маркер тестовій функції
     :return: Код статусу 200 і об’єкт користувача з іменем користувача та електронною поштою
     """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/users/me/", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert "username" in data
        assert "email" in data
        assert "password" not in data


def test_profile_info(client, token):
    """
     Функція test_profile_info перевіряє /api/users/&lt;username&gt; кінцева точка.
     Це робиться, спочатку виправляючи об’єкт r модуля auth_service, щоб повернути None,
     потім він робить запит GET до /api/users/deadpool/, передаючи заголовок авторизації з дійсним маркером.
     Потім відповідь перевіряється на наявність коду статусу 200 і на те, що вона містить &quot;ім’я користувача&quot; і &quot;Дедпул&quot;.
     :param client: Надішліть запит на сервер API
     :param token: передати маркер, згенерований фікстурою
     :return: Код статусу 200 і об’єкт json з іменем користувача
     """
    with patch.object(auth_service, 'r') as r_mock:
            r_mock.get.return_value = None
            username = "deadpool"
            response = client.get(f"/api/users/{username}/",
                                  headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200, response.text
            data = response.json()
            assert "username" in data
            assert data["username"] == username


def test_profile_info_user_not_found(client, token):
    """
     Функція test_profile_info_user_not_found перевіряє кінцеву точку profile_info з іменем користувача, якого не існує.
     Він використовує фікстуру клієнта, щоб зробити запит GET до /api/users/not_deadpool/ і передає заголовок авторизації з
     дійсний маркер. Потім тест підтверджує, що код статусу відповіді – 404, і перевіряє, чи data[&quot;detail&quot;] == &quot;Користувача не знайдено&quot;.
     :param client: Зробіть запит до API
     :param token: передати маркер тестовій функції
     :return: Код статусу 404 і деталі помилки
     """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        username = "not_deadpool"
        response = client.get(f"/api/users/{username}/",
                              headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "User not found"
