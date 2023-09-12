from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import User, Role
from src.repository.users import get_user_info, update_user_info, block
from src.schemas.user_schemas import UserResponse, UserUpdate, UserBlackList, UserBlacklistResponse
from src.services.auth import auth_service
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin])
access_block = RolesAccess([Role.admin])

router = APIRouter(prefix="/users", tags=["Users profile"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція read_users_me — це запит GET, який повертає інформацію про поточного користувача.
         Він вимагає автентифікації та використовує auth_service для отримання поточного користувача.
     :param current_user: Користувач: передати об’єкт поточного користувача у функцію
     :return: Поточний об'єкт користувача, отриманий від auth_service
     """
    return current_user


@router.get("/{username}/", response_model=UserResponse)
async def profile_info(username: str, db: Session = Depends(get_db)):
    """
     Отримати інформацію про користувача на основі його імені користувача.
     :param ім'я користувача: str: Ім'я користувача користувача
     :param db: Сеанс: доступ до бази даних
     :return: Об'єкт користувача
     """
    user_info = await get_user_info(username, db)
    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info


@router.put('/{username}', response_model=UserResponse, dependencies=[Depends(access_update)])
async def profile_update(username: str, body: UserUpdate, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція profile_update оновлює інформацію профілю користувача.
         Функція приймає ім’я користувача, тіло (що є об’єктом UserUpdate), db (сеанс бази даних) і current_user.
         Якщо ім’я користувача current_user не збігається з даним іменем користувача, а їхня роль — «користувач», тоді HTTPException
             з кодом статусу 403 Заборонено буде виведено разом із повідомленням про помилку про те, що вони можуть лише оновлювати
             власний профіль. В іншому випадку, updated_user буде налаштовано на очікування update_user_info(body, username, db). нарешті,
             оновлений користувач буде повернено.
     :param ім'я користувача: str: отримати ім'я користувача для оновлення
     :param body: UserUpdate: отримати дані з тіла запиту
     :param db: Сеанс: отримати сеанс бази даних
     :param current_user: Користувач: отримати поточного користувача,
     :return: Оновлений об’єкт користувача
     """
    if current_user.username != username and current_user.role == 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own profile")

    updated_user = await update_user_info(body, username, db)

    return updated_user


@router.patch("/{email}/blacklist", response_model=UserBlacklistResponse, dependencies=[Depends(access_block)])
async def block_user(email: str, body: UserBlackList, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """Опис"""
    blocked_user = await block(email, body, db)
    if blocked_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return blocked_user
