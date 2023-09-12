import pytest
from sqlalchemy.orm import Session

from src.database.models import User
from src.repository.users import get_user_by_email, update_token, confirmed_email, get_user_info, update_user_info


@pytest.mark.asyncio
async def test_get_user_by_email(session: Session):
    """
     Функція test_get_user_by_email перевіряє функцію get_user_by_email у файлі users.py.
     Він створює користувача з електронною адресою, додає його до бази даних, а потім викликає get_user_by_email
     з тією самою електронною адресою як аргумент. Він стверджує, що цей виклик повертає об’єкт User і
     що його атрибут email дорівнює тому, що було передано в get user by email.
     :param session: Сеанс: Передайте сеанс бази даних до функції
     :return: Об’єкт користувача з адресою електронної пошти, яку було передано
     """
    email = "test@example.com"
    user = User(username="testuser", email=email, password="password")
    session.add(user)
    session.commit()

    result = await get_user_by_email(email, session)

    assert result is not None
    assert result.email == email


@pytest.mark.asyncio
async def test_update_token(session: Session):
    """
     Функція test_update_token перевіряє функцію update_token.
     Це робиться шляхом створення користувача, додавання його до бази даних, а потім виклику update_token з цим користувачем.
     Тест пройдено, якщо маркер оновлення цього користувача дорівнює &quot;new_token&quot;.
     :param session: Сеанс: Передайте сеанс бази даних до функції
     :return: Жодного
     """
    user = User(username="testuser", email="test@example.com", password="password")
    session.add(user)
    session.commit()
    token = "new_token"

    await update_token(user, token, session)

    session.refresh(user)
    assert user.refresh_token == token


@pytest.mark.asyncio
async def test_confirmed_email(session: Session):
    """
     Функція test_confirmed_email перевіряє функцію confirmed_email.
     Він створює користувача з адресою електронної пошти та встановлює для поля підтвердження значення False.
     Потім він викликає функцію confirmed_email, передаючи цю адресу електронної пошти та об’єкт сеансу.
     Нарешті, він перевіряє, чи підтверджене поле користувача тепер має значення True.
     :param session: Сеанс: передати функцію сеанс бази даних
     :return: Логічне значення, яке є істинним, якщо електронну адресу користувача було підтверджено
     """
    email = "test@example.com"
    user = User(username="testuser", email=email, password="password", confirmed=False)
    session.add(user)
    session.commit()

    await confirmed_email(email, session)

    confirmed_user = await get_user_by_email(email, session)
    assert confirmed_user.confirmed is True


@pytest.mark.asyncio
async def test_get_user_info(session: Session):
    """
     Функція test_get_user_info перевіряє функцію get_user_info.
     Це робиться шляхом створення користувача в базі даних, а потім виклику get_user_info з цим іменем користувача.
     Перевірку проходить, якщо він повертає об’єкт User з тим самим іменем користувача та електронною адресою, що й створений.
     :param session: Сеанс: Перейти до сеансу бази даних
     :return: Об’єкт, що містить інформацію про користувача
     """
    username = "testuser"
    user = User(username=username, email="test@example.com", password="password")
    session.add(user)
    session.commit()

    user_info = await get_user_info(username, session)

    assert user_info is not None
    assert user_info.username == username
    assert user_info.email == "test@example.com"


@pytest.mark.asyncio
async def test_update_user_info(session: Session):
    """
     Функція test_update_user_info перевіряє функцію update_user_info.
         Аргументи:
             сеанс (Сеанс): сеанс бази даних для використання для цього тесту.
     :param session: Сеанс: Створіть сеанс бази даних для тесту
     :return: Оновлений користувач
     """
    username = "testuser"
    user = User(username=username, email="test@example.com", password="password")
    session.add(user)
    session.commit()

    updated_username = "newuser"
    updated_email = "new@example.com"
    updated_body = User(username=updated_username, email=updated_email)

    # Дія
    updated_user = await update_user_info(updated_body, username, session)

    # Assert
    assert updated_user is not None
    assert updated_user.username == updated_username
    assert updated_user.email == updated_email
