from typing import List

from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository.search import find_image_by_tag
from src.routes.tags import access_get, access_delete, access_create
from src.schemas.image_schemas import ImageDb
from src.schemas.transformed_image_schemas import SearchImageResponse
from src.services.auth import auth_service
from src.repository.search import get_img_by_user_id

router = APIRouter(prefix="/search", tags=["search and filter"])


@router.get("/image/{user_id}", response_model=list[ImageDb],
            dependencies=[Depends(access_get)])
async def get_image_by_user_id(user_id: int = Path(ge=1),
                               skip: int = 0, limit: int = 10,
                               filter_type: str = 'd',
                               db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція get_image_by_user_id повертає список зображень, які пов’язані з user_id.
         Функція приймає необов’язкові параметри пропуску та обмеження для керування розбивкою на сторінки, а також необов’язковий filter_type
         параметр, щоб контролювати, чи потрібно фільтрувати повернуті зображення за датою (d) або (-d).
         Якщо тип фільтра не вказано, за замовчуванням фільтрується за датою.
     :param user_id: int: отримати зображення конкретного користувача
     :param skip: int: Пропустити певну кількість зображень
     :param limit: int: обмежити кількість зображень, що повертаються
     :param filter_type: str: фільтрувати зображення за датою, оцінками "подобається" чи коментарями
     :param db: Сеанс: отримати сеанс бази даних
     :param current_user: Користувач: отримати поточного користувача
     :return: Список зображень, які завантажив користувач
     """
    images = await get_img_by_user_id(user_id, skip, limit, filter_type, db, current_user)
    return images


@router.get("/", response_model=List[SearchImageResponse], dependencies=[Depends(access_get)])
async def search_images_by_tag(skip: int = 0, limit: int = 10,
                               search_tag: str = "",
                               filter_type: str = 'd',
                               db: Session = Depends(get_db),
                               user: User = Depends(auth_service.get_current_user)):
    """
     Функція search_images_by_tag шукає зображення за тегом.
         Аргументи:
             skip (int): кількість зображень, які потрібно пропустити в результатах пошуку. За замовчуванням 0.
             limit (int): Максимальна кількість зображень для повернення в результатах пошуку. За замовчуванням 10, максимум 100.
             search_tag (str): Рядок, що містить один або кілька тегів, розділених комами, наприклад, &quot;собака&quot; або &quot;собака,кішка&quot;. Якщо теги не надано, буде повернено всі записи зображень, незалежно від їх пов’язаних тегів.
     :param skip: int: Пропустити перші n зображень
     :param limit: int: обмежити кількість зображень, що повертаються
     :param search_tag: str: Пошук зображень за тегом
     :param filter_type: str: Визначити сортування зображень за датою 'd' чи '-d' (зворотне сортування)
     :param db: Сеанс: отримати сеанс бази даних
     :param user: Користувач: отримати поточного користувача
     :return: Список об’єктів зображення
     """
    images = await find_image_by_tag(skip, limit, search_tag, filter_type, db, user)
    return images
