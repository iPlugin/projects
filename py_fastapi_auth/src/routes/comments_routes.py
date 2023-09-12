from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role, Image
from src.schemas.comment_schemas import CommentResponse, CommentModel, CommentDeleteResponse
from src.repository import comments as repository_comments
from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/comments', tags=['comments'])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator, Role.user])
access_delete = RolesAccess([Role.admin, Role.moderator])


@router.get('/', response_model=List[CommentResponse],
            dependencies=[Depends(access_get)])
async def get_comments(db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
     Функція get_comments повертає список коментарів із бази даних.
     :param db: Сеанс: передає сеанс бази даних функції
     :param _: Користувач: Перевірте, чи користувач автентифікований
     :return: Список коментарів
     """
    comments = await repository_comments.get_comments(db)
    return comments


@router.get('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(access_get)])
async def get_comment_by_id(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                            _: User = Depends(auth_service.get_current_user)):
    """
     Функція get_comment_by_id повертає коментар за його ідентифікатором.
         Аргументи:
             comment_id (int): ідентифікатор коментаря, який буде повернуто.
             db (сеанс, необов’язково): об’єкт сеансу бази даних для запиту до бази даних. За замовчуванням Depends(get_db).
             _ (Користувач, необов’язково): автентифікований об’єкт користувача для перевірки, чи має користувач доступ до цієї кінцевої точки. За замовчуванням залежить від (auth_service.get_current_user).
     :param comment_id: int: отримати ідентифікатор коментаря з url
     :param db: Сеанс: передайте сеанс бази даних на рівень сховища
     :param _: Користувач: отримати поточного користувача
     :return: Об’єкт коментаря
     """
    comment = await repository_comments.get_comment_by_id(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment


@router.post('/', response_model=CommentResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_create)])
async def create_comment(body: CommentModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція create_comment створює новий коментар у базі даних.
         Функція приймає об’єкт CommentModel як вхідні дані та повертає щойно створений коментар.
     :param body: CommentModel: Створіть об’єкт коментаря з тіла запиту
     :param db: Сеанс: передайте сеанс бази даних на рівень сховища
     :param current_user: Користувач: отримати user_id поточного користувача
     :return: Об'єкт коментаря
     """
    try:
        image = db.query(Image).filter_by(id=body.image_id).first()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such image")
    body.user_id = current_user.id
    comment = await repository_comments.create_comment(body, db)
    return comment


@router.put('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(access_update)])
async def update_comment(body: CommentModel, comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція update_comment оновлює коментар у базі даних.
     :param body: CommentModel: отримати тіло коментаря із запиту
     :param comment_id: int: отримати ідентифікатор коментаря з url
     :param db: Сеанс: отримати сеанс бази даних
     :param current_user: Користувач: отримати користувача, який зараз увійшов у систему
     :return: Оновлений коментар
     """
    if current_user.id != body.user_id and current_user.role == 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't change not your comment")
    comment = await repository_comments.update_comment(body, comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment


@router.delete('/{comment_id}', response_model=CommentDeleteResponse, dependencies=[Depends(access_delete)])
async def remove_comment(comment_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    """
     Функція remove_comment видаляє коментар із бази даних.
         Аргументи:
             comment_id (int): ідентифікатор коментаря, який потрібно видалити.
             db (сеанс, необов’язково): об’єкт сеансу бази даних, який використовується для запиту та зміни даних у базі даних. За замовчуванням Depends(get_db).
             _ (Користувач, необов’язково): об’єкт, що представляє автентифікованого користувача, який робить цей запит. За замовчуванням залежить від (auth_service.get_current_user).
     :param comment_id: int: Отримати ідентифікатор коментаря зі шляху
     :param db: Сеанс: передайте з’єднання з базою даних функції
     :param _: Користувач: отримати поточного користувача з auth_service
     :return: Об’єкт коментаря
     """
    comment = await repository_comments.remove_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such comment")
    return comment
