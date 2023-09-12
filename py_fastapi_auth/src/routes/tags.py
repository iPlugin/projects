from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.tag_schemas import TagModel, TagResponse
from src.repository import tags as repository_tags
from src.conf.messages import AuthMessages

from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/tags', tags=["tags"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator])
access_delete = RolesAccess([Role.admin, Role.moderator])


@router.get("/", response_model=List[TagResponse], dependencies=[Depends(access_get)])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
     Функція read_tags повертає список тегів.
     :param skip: int: Пропустити перші n тегів
     :param limit: int: обмежити кількість повернутих тегів
     :param db: Сеанс: передає сеанс бази даних функції
     :param _: Користувач: Скажіть fastapi, що користувач потрібен, але він не використовуватиметься у функції
     :return: Список тегів
     """
    tags = await repository_tags.get_tags(skip, limit, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse, dependencies=[Depends(access_get)])
async def read_tag(tag_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
     Функція read_tag повертає один тег за його ідентифікатором.
     :param tag_id: int: Вкажіть ідентифікатор тегу, який потрібно видалити
     :param db: Сеанс: передає сеанс бази даних функції
     :param _: Користувач: перевірте, чи користувач автентифікований і має доступ до кінцевої точки
     :return: Об’єкт тегу
     """
    tag = await repository_tags.get_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.post("/", response_model=TagResponse, dependencies=[Depends(access_create)])
async def create_tag(body: TagModel, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
     Функція create_tag створює новий тег у базі даних.
         Функція приймає об’єкт TagModel як вхідні дані та повертає створений тег.
     :param body: TagModel: отримати дані з тіла запиту
     :param db: Сеанс: передає сеанс бази даних функції
     :param _: Користувач: отримати поточного користувача
     :return: Об’єкт моделі тегів
     """
    check_tag = await repository_tags.get_tag_by_name(body.name.lower(), db)
    if check_tag:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Such tag already exist')
    tag = await repository_tags.create_tag(body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AuthMessages.verification_error)
    return tag


@router.put("/{tag_id}", response_model=TagResponse, dependencies=[Depends(access_update)])
async def update_tag(body: TagModel, tag_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
     Функція update_tag оновлює тег у базі даних.
     :param body: TagModel: передає дані з тіла запиту до функції
     :param tag_id: int: Визначте тег, який потрібно видалити
     :param db: Сеанс: передайте сеанс бази даних на рівень сховища
     :param _: Користувач: отримати поточного користувача з auth_service
     :return: Об’єкт моделі тегів
     """
    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found or exists or you don't have enough rules to update")
    return tag


@router.delete("/{tag_id}", response_model=TagResponse, dependencies=[Depends(access_delete)])
async def remove_tag(tag_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
     Функція remove_tag видаляє тег із бази даних.
         Аргументи:
             tag_id (int): ідентифікатор тегу, який потрібно видалити.
             db (сеанс, необов’язково): об’єкт сеансу бази даних для взаємодії з базою даних. За замовчуванням Depends(get_db).
             _ (Користувач, необов’язково): автентифікований об’єкт користувача для перевірки дозволів і права власності на теги. За замовчуванням залежить від (auth_service.get_current_user).
     :param tag_id: int: Вкажіть ідентифікатор тегу, який потрібно видалити
     :param db: Сеанс: передає сеанс бази даних функції
     :param _: Користувач: отримати поточного користувача
     :return: Видалений тег
     """
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found or you don't have enough rules to delete")
    return tag
