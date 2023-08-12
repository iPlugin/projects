from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.rating_schemas import RatingModel, RatingResponse, AverageRatingResponse
from src.repository import ratings as repository_ratings
from src.conf.messages import AuthMessages

from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/ratings', tags=["ratings"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator, Role.user])
access_update = RolesAccess([Role.admin, Role.moderator])
access_delete = RolesAccess([Role.admin, Role.moderator])


@router.get("/image/{image_id}", response_model=float, dependencies=[Depends(access_get)])
async def common_image_rating(image_id, _: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
     Функція common_image_rating повертає середню оцінку зображення.
         Аргументи:
             image_id (int): ідентифікатор зображення, яке буде оцінено.
             _ (Користувач): користувач, який робить запит. Це ін’єкція залежності, яка використовується лише для автентифікації. Її можна ігнорувати під час виклику цієї функції поза кодовою базою FastAPI, оскільки вона автоматично впроваджуватиметься самим FastAPI під час виклику з маршруту, який вимагає автентифікації.
     :param image_id: отримати зображення з бази даних
     :param _: Користувач: отримати поточного користувача з auth_service
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Середня оцінка зображення
     """
    common_rating = await repository_ratings.get_average_rating(image_id, db)
    return common_rating


@router.get("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_get)])
async def read_rating(rating_id: int, _: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
     Функція read_rating повертає рейтинг за його ідентифікатором.
         отримати:
           резюме: Отримайте рейтинг за ID.
           Опис: повертає деталі індивідуального рейтингу, включаючи користувача, який його створив, і його ім’я користувача.
           теги: [рейтинги]
           параметри:
               in: шлях
               name: id_rating # Унікальний ідентифікатор для цього конкретного рейтингу (наприклад, 1) передається як частина URL-шляху (наприклад, /ratings/{id_rating}). Це називається &quot;зв'язування шляху&quot;. Перегляньте https://fastapi
     :param rating_id: int: Визначте рейтинг, який потрібно видалити
     :param _: Користувач: дозволити auth_service вставляти об’єкт користувача у функцію
     :param db: Сеанс: доступ до бази даних
     :return: Об'єкт рейтингу
     """
    rating = await repository_ratings.get_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    return rating


@router.post("/{image_id}", response_model=RatingResponse, dependencies=[Depends(access_create)])
async def create_rate(image_id, body: RatingModel, current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    """
     Функція create_tag створює новий тег у базі даних.
     :param image_id: отримати зображення з бази даних
     :param body: RatingModel: отримати дані з тіла запиту
     :param current_user: Користувач: отримати користувача, який зараз увійшов у систему
     :param db: Сеанс: підключення до бази даних
     :return: Об’єкт тегу
     """
    rating = await repository_ratings.create_rating(image_id, body, current_user, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please, check the image_id. You can't rate your images or give 2 or more rates for 1 image")
    return rating


@router.put("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_update)])
async def update_rating(body: RatingModel, rating_id: int, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """
     Функція update_rating оновлює рейтинг у базі даних.
     :param body: RatingModel: отримати тіло запиту
     :param rating_id: int: Визначте рейтинг, який потрібно оновити
     :param db: Сеанс: передайте з’єднання з базою даних функції
     :param _: Користувач: отримати поточного користувача з auth_service
     :return: Об'єкт рейтингу
     """
    rating = await repository_ratings.update_rating(rating_id, body, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Rating not found or you can't update the rating because of rules or roles")
    return rating


@router.delete("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(access_delete)])
async def remove_rating(rating_id: int, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """
     Функція remove_rating видаляє оцінку з бази даних.
     :param rating_id: int: Знайдіть рейтинг у базі даних
     :param db: Сеанс: отримати сеанс бази даних
     :param _: Користувач: переконайтеся, що користувач увійшов у систему
     :return: Видалений рейтинг
     """
    rating = await repository_ratings.remove_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Rating not found or you don't have enough rules to delete")
    return rating
