from typing import List

from fastapi import APIRouter, Path, status, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.routes.tags import access_get, access_delete, access_create
from src.schemas.transformed_image_schemas import TransformedImageModel, TransformedImageResponse, \
    UrlTransformedImageResponse, UrlQRCodeTransformedImageResponse
from src.repository.transformed_images import get_all_transformed_images, delete_transformed_image_by_id, \
    create_transformed_picture, get_qrcode_transformed_image_by_id, get_transformed_img_by_id, \
    get_url_transformed_image_by_id
from src.services.auth import auth_service

router = APIRouter(prefix="/transformed_images", tags=["transformed images"])


@router.post("/{image_id}", response_model=TransformedImageResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_create)])
async def create_new_transformed_image(body: TransformedImageModel,
                                       user: User = Depends(auth_service.get_current_user),
                                       image_id: int = Path(ge=1),
                                       db: Session = Depends(get_db), ):
    """
     Функція create_new_transformed_image створює нове трансформоване зображення.
     Функція приймає такі параметри:
         тіло (TransformedImageModel): об’єкт TransformedImageModel, що містить інформацію для нового трансформованого зображення.
         користувач (User): необов’язковий об’єкт User, що містить інформацію про поточного користувача, якщо такий є. За замовчуванням немає.
             Цей параметр використовується декоратором Depends() FastAPI, щоб визначити, чи було надано з цим запитом дійсний маркер JWT, і якщо так, то який його вміст.
     :param body: TransformedImageModel: отримати дані з тіла запиту
     :param user: Користувач: отримати поточного користувача
     :param image_id: int: отримати ідентифікатор зображення зі шляху
     :param db: Сеанс: передає сеанс бази даних функції
     :param : отримати ідентифікатор зображення з url
     :return: Трансформований об’єкт зображення
     """
    new_transformed_picture = await create_transformed_picture(body, user, image_id, db)
    return new_transformed_picture


@router.get("/{image_id}", response_model=List[TransformedImageResponse], dependencies=[Depends(access_get)])
async def get_all_transformed_images_for_original_image_by_id(skip: int = 0, limit: int = 10,
                                                              image_id: int = Path(ge=1),
                                                              db: Session = Depends(get_db),
                                                              user: User = Depends(auth_service.get_current_user)):
    """
     Функція get_all_transformed_images_for_original_image_by_id повертає всі трансформовані зображення для даного оригінального зображення.
         Функція приймає додатковий параметр пропуску та обмеження, а також ідентифікатор вихідного зображення, яке потрібно запитати.
         Також потрібно передати сеанс бази даних і об’єкт користувача.
     :param skip: int: Пропустити перші n зображень
     :param limit: int: обмежити кількість повернутих зображень
     :param image_id: int: отримати image_id з url
     :param db: Сеанс: доступ до бази даних
     :param user: Користувач: Перевірте, чи користувач увійшов у систему
     :return: Список усіх трансформованих зображень для даного оригінального зображення
     """
    images = await get_all_transformed_images(skip, limit, image_id, db, user)
    return images


@router.get("/transformed/{transformed_image_id}", response_model=TransformedImageResponse,
            dependencies=[Depends(access_get)])
async def get_transformed_images_by_image_id(transformed_image_id: int = Path(ge=1),
                                             db: Session = Depends(get_db),
                                             user: User = Depends(auth_service.get_current_user)):
    """
     Функція get_transformed_images_by_image_id повертає трансформоване зображення за його ідентифікатором.
         Функція приймає ціле число, що представляє ідентифікатор перетвореного зображення, і два необов’язкові параметри:
             - db: об’єкт сеансу бази даних, який використовується для запиту інформації до бази даних.
             - користувач: об'єкт, що містить інформацію про поточного користувача, який робить цей запит.
     :param transformed_image_id: int: отримати трансформоване зображення за ідентифікатором
     :param db: Сеанс: підключення до бази даних
     :param user: Користувач: отримати поточного користувача
     :return: Трансформоване зображення за його ідентифікатором
     """
    transformed_image = await get_transformed_img_by_id(transformed_image_id, db, user)
    return transformed_image


@router.get("/transformed/{transformed_image_id}/qrcode", response_model=UrlQRCodeTransformedImageResponse,
            dependencies=[Depends(access_get)])
async def get_qrcode_for_transformed_image(transformed_image_id: int = Path(ge=1),
                                           db: Session = Depends(get_db),
                                           user: User = Depends(auth_service.get_current_user)):
    """
     Функція get_qrcode_for_transformed_image повертає qrcode для трансформованого зображення.
         Функція приймає ціле число, що представляє ідентифікатор перетвореного зображення, і повертає його
         qrcode перетвореного зображення.
     :param transformed_image_id: int: отримати ідентифікатор трансформованого зображення зі шляху
     :param db: Сеанс: отримати сеанс бази даних
     :param user: Користувач: Перевірте, чи користувач автентифікований
     :return: Трансформоване зображення з заданим ідентифікатором
     """
    transformed_image = await get_qrcode_transformed_image_by_id(transformed_image_id, db, user)
    return transformed_image


@router.get("/transformed/{transformed_image_id}/url", response_model=UrlTransformedImageResponse,
            dependencies=[Depends(access_get)])
async def get_url_for_transformed_image(transformed_image_id: int = Path(ge=1),
                                        db: Session = Depends(get_db),
                                        user: User = Depends(auth_service.get_current_user)):
    """
     Функція get_url_for_transformed_image повертає URL-адресу трансформованого зображення.
         Функція приймає ціле число, що представляє ідентифікатор перетвореного зображення, і повертає
         який змінив URL-адресу зображення.
     :param transformed_image_id: int: отримати ідентифікатор трансформованого зображення зі шляху
     :param db: Сеанс: отримати сеанс бази даних
     :param user: Користувач: Перевірте, чи користувач автентифікований
     :return: URL-адреса перетвореного зображення
     """
    transformed_image = await get_url_transformed_image_by_id(transformed_image_id, db, user)
    return transformed_image


@router.delete("/transformed/{transformed_image_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(access_delete)])
async def delete_transformed_image(transformed_image_id: int = Path(ge=1),
                                   db: Session = Depends(get_db),
                                   user: User = Depends(auth_service.get_current_user)):
    """
     Функція delete_transformed_image видаляє трансформоване зображення з бази даних.
         Функція приймає ціле число, що представляє ідентифікатор трансформованого зображення, яке потрібно видалити,
         і повертає None.
     :param transformed_image_id: int: Вкажіть ідентифікатор трансформованого зображення, яке потрібно видалити
     :param db: Сеанс: отримати сеанс бази даних
     :param user: Користувач: Перевірте, чи користувач автентифікований
     :return: Жодного, тому нам потрібно створити нову функцію
     """
    transformed_image = await delete_transformed_image_by_id(transformed_image_id, db, user)
    return None
