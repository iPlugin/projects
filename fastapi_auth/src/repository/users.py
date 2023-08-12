from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from src.database.models import User
from src.schemas.user_schemas import UserModel, UserUpdate, UserBlackList


async def get_user_by_email(email: str, db: Session) -> User | None:
    """

     Функція get_user_by_email приймає електронну пошту та сеанс бази даних,
     і повертає користувача, пов’язаного з цією електронною поштою. Якщо такого користувача не існує, повертається None.
     :param email: str: Передайте адресу електронної пошти користувача, яку потрібно отримати
     :param db: Сеанс: Перейти до сеансу бази даних
     :return: Об’єкт користувача або жодного
     :doc-author: Трелент
     """

    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """

     Функція create_user створює нового користувача в базі даних.
         Якщо немає користувачів із роллю адміністратора, новий користувач буде створено як адміністратор.
         В іншому випадку він буде створений як звичайний користувач.
     :param body: UserModel: Створіть новий об’єкт користувача
     :param db: Сеанс: доступ до бази даних
     :return: Об’єкт користувача
     """

    admin_exists = db.query(User).filter(User.role == 'admin').first()

    if admin_exists:
        new_user = User(**body.dict(), role='user')
    else:
        new_user = User(**body.dict(),  role='admin')

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """

     Функція update_token оновлює маркер оновлення для користувача.
     :param user: Користувач: Ідентифікуйте користувача, який оновлюється
     :param token: str | Немає: передати маркер, який повертається з api
     :param db: Сеанс: доступ до бази даних
     :return: Нічого
     """

    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """

     Функція confirmed_email приймає електронний лист і сеанс бази даних,
     і встановлює для поля підтвердження користувача з цією електронною поштою значення True.

     :param email: str: Передайте електронну адресу користувача, який потрібно підтвердити
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Нічого
     """

    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def get_user_info(username: str, db: Session):

    """
     Функція get_user_info приймає ім’я користувача та повертає інформацію про користувача.
         Аргументи:
             ім'я користувача (str): ім'я користувача, яке буде отримано з бази даних.
     :param ім'я користувача: str: Вкажіть ім'я користувача
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Словник інформації про користувача
     """

    user = db.query(User).filter(User.username == username).first()
    return user


async def update_user_info(body: UserUpdate, username: str, db: Session):
    """

     Оновіть інформацію про користувача за допомогою наданих оновлених полів на основі імені користувача.
     :param body: UserUpdate: Оновлені поля для користувача
     :param ім'я користувача: str: Ім'я користувача користувача
     :param db: Сеанс: доступ до бази даних
     :return: Оновлений об'єкт користувача
     """

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.username = body.username
    user.email = body.email
    db.commit()
    return user


async def block(email: str, body: UserBlackList, db: Session):

    """Опис"""

    user = await get_user_by_email(email, db)
    if user:
        user.banned = body.banned
        db.commit()
    return user
