import os

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.image_schemas import ImageAddResponse, ImageUpdateModel, ImageAddModel, ImageAddTagResponse, \
    ImageAddTagModel, ImageGetAllResponse, ImageGetResponse, ImageDeleteResponse, ImageUpdateDescrResponse, \
    ImageAdminGetAllResponse
from src.repository import images
from src.services.auth import auth_service
from src.services.images import images_service_change_name, images_service_normalize_tags
from src.services.roles import RolesAccess

load_dotenv()

router = APIRouter(prefix='/images', tags=["images"])

access_all = RolesAccess([Role.admin, Role.moderator, Role.user])
access_admin = RolesAccess([Role.admin])


@router.get("", response_model=ImageGetAllResponse, dependencies=[Depends(access_all)])
async def get_images(db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція get_images повертає список зображень, які завантажив поточний користувач.
     :param db: Сеанс: передає сеанс бази даних функції
     :param current_user: Користувач: отримати інформацію про поточного користувача
     :return: Список усіх зображень, пов’язаних із поточним користувачем
     """

    user_images = await images.get_images(db, current_user)
    return {"images": user_images}


@router.get("/image_id/{id}", response_model=ImageGetResponse, dependencies=[Depends(access_all)])
async def get_image(id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція get_image повертає одне зображення з його оцінками та коментарями.
     Функція приймає параметр ідентифікатора, який є ідентифікатором зображення, яке потрібно повернути.
     Він також приймає параметр db, який використовується для доступу до бази даних. Поточний_користувач
     Параметр використовується для автентифікації.
     :param id: int: отримати зображення з цим ідентифікатором
     :param db: Сеанс: доступ до бази даних
     :param current_user: Користувач: отримати поточного користувача
     :return: Dict із зображенням, оцінками та коментарями
     """

    user_image, ratings, comments = await images.get_image(db, id, current_user)
    return {"image": user_image, "ratings": ratings, "comments": comments}


@router.get("/user_id/{user_id}", response_model=ImageAdminGetAllResponse, dependencies=[Depends(access_admin)])
async def admin_get_images(user_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція admin_get_images використовується для отримання всіх зображень для користувача.
         Ця функція потребує user_id користувача, чиї зображення ви хочете отримати.
         Параметр current_user необхідний для FastAPI та містить інформацію про адміністратора, який наразі ввійшов у систему.
     :param user_id: int: Вкажіть user_id користувача, зображення якого потрібно отримати
     :param db: Сеанс: доступ до бази даних
     :param current_user: Користувач: перевірте, чи є користувач адміністратором
     :return: Список усіх зображень користувача, які є в базі даних
     """

    user_response = await images.admin_get_image(db, user_id)
    return {"images": user_response}


@router.post("/add", response_model=ImageAddResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_all)])
async def upload_image(body: ImageAddModel = Depends(), file: UploadFile = File(), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція upload_image використовується для завантаження зображення на хмарний сервер.
         Функція приймає тіло, файл, сесію бази даних і поточного користувача як параметри.
         Параметр body використовується для тегів і опису зображення, яке завантажується.
         Параметр file використовується для завантаження фактичного файлу зображення з комп’ютера або пристрою користувача.
         Параметр db session дозволяє отримати доступ до нашої бази даних за допомогою методів і функцій SQLAlchemy ORM.
         Нарешті, ми використовуємо current_user, щоб ми могли пов’язати кожну завантажену фотографію з відповідним користувачем.
     :param body: ImageAddModel: отримати опис і теги з тіла запиту
     :param file: UploadFile: отримати файл із запиту
     :param db: Сеанс: отримати підключення до бази даних із пулу
     :param current_user: Користувач: отримати поточного користувача з бази даних
     :return: Словник із зображенням і детальним повідомленням
     """

    cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
            secure=True
        )

    correct_tags = await images_service_normalize_tags(body)

    public_name = file.filename.split(".")[0]

    correct_public_name = await images_service_change_name(public_name, db)

    file_name = correct_public_name + "_" + str(current_user.username)
    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoNet/{file_name}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoNet/{file_name}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    # r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShare/{file_name}', overwrite=True)
    # src_url = cloudinary.CloudinaryImage(f'PhotoShare/{file_name}') \
    #     .build_url(width=250, height=250, crop='fill', version=r.get('version'))

    image, details = await images.add_image(db, body, correct_tags, src_url, correct_public_name, current_user)

    return {"image": image, "detail": "Image was successfully added." + details}


@router.put("/update_description/{image_id}", response_model=ImageUpdateDescrResponse,
            dependencies=[Depends(access_all)])
async def update_description(image_id: int, image_info: ImageUpdateModel, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція update_description оновлює опис зображення.
         Функція приймає сеанс бази даних, current_user і image_id як параметри.
         Потім він використовує функцію update_image із зображень, щоб оновити опис зображення з цим ідентифікатором.
     :param image_id: int: Визначте зображення, яке оновлюється
     :param image_info: ImageUpdateModel: отримати новий опис для зображення
     :param db: Сеанс: доступ до бази даних
     :param current_user: Користувач: отримати поточного користувача, який увійшов у систему
     :return: Словник з ідентифікатором, описом і деталями оновленого зображення
     """

    user_image = await images.update_image(db, image_id, image_info, current_user)
    return {"id": user_image.id, "description": user_image.description, "detail": "Image was successfully updated"}


@router.put("/update_tags/{image_id}", response_model=ImageAddTagResponse, dependencies=[Depends(access_all)])
async def add_tag(image_id, body: ImageAddTagModel = Depends(), db: Session = Depends(get_db),
                  current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція add_tag додає тег до зображення.
         Функція приймає такі параметри:
             - image_id: ідентифікатор зображення, яке позначається тегом.
             - тіло: об'єкт JSON, що містить назву та опис тегу. Це підтверджується ImageAddTagModel().
     :param image_id: Визначте зображення, яке потрібно оновити
     :param body: ImageAddTagModel: отримати тег із тіла запиту
     :param db: Сеанс: отримати сеанс бази даних
     :param current_user: Користувач: отримати поточного користувача з бази даних
     :return: Словник із ідентифікатором зображення, тегами та детальним повідомленням
     """
    image, details = await images.add_tag(db, image_id, body, current_user)
    return {"id": image.id, "tags": image.tags, "detail": "Image was successfully updated." + details}


@router.delete("/{id}", response_model=ImageDeleteResponse, dependencies=[Depends(access_all)])
async def delete_image(id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
     Функція delete_image видаляє зображення з бази даних.
         Функція приймає user_id і image_id і повертає словник з інформацією про видалене зображення.
     :param id: int: Вкажіть ідентифікатор зображення, яке потрібно видалити
     :param db: Сеанс: передає сеанс бази даних функції
     :param current_user: Користувач: отримати поточного користувача з бази даних
     :return: Словник із зображенням і повідомленням про те, що його видалено
     """
    user_image = await images.delete_image(db, id, current_user)
    return {"image": user_image, "detail": "Image was successfully deleted"}
