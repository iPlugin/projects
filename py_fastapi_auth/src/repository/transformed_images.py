import cloudinary
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import TransformedImage, Image, User, Role
from src.database.db import get_db
from src.schemas.transformed_image_schemas import TransformedImageModel
from src.services.transformed_image import create_transformations, generate_and_upload_qr_code


async def create_transformed_picture(body: TransformedImageModel,
                                     current_user,
                                     image_id: int,
                                     db: Session = Depends(get_db)):
    """
     Функція create_transformed_picture приймає об’єкт TransformedImageModel, поточного користувача та ідентифікатор зображення.
     Потім він запитує в базі даних зображення з таким ідентифікатором і перевіряє, чи воно належить поточному користувачеві. Якщо ні, виникає помилка 404.
     Якщо так, він створює перетворення з об’єкта TransformedImageModel за допомогою функції create_transformations (див. нижче). Потім він використовує
     Cloudinary API, щоб створити нову URL-адресу для цього перетвореного зображення на основі цих трансформацій і завантажити цю нову URL-адресу як QR-код
     до Cloudinary за допомогою функції generate_and_upload_qr_code (див. нижче). Нарешті
     :param body: TransformedImageModel: отримати дані з тіла запиту
     :param current_user: отримати користувача, який зараз увійшов у систему
     :param image_id: int: отримати оригінальне зображення з бази даних
     :param db: Сеанс: отримати доступ до бази даних
     :return: Об’єкт transformedimage, який потім серіалізується у відповідь JSON
     """
    original_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == current_user.id)).first()
    if not original_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Original image not found")

    transformations = create_transformations(body)

    public_id = original_image.public_name
    file_name = public_id + "_" + str(current_user.username)
    # new_url = cloudinary.CloudinaryImage(f'PhotoShare/{file_name}').build_url(transformation=transformations)
    new_url = cloudinary.CloudinaryImage(f'PhotoNet/{file_name}').build_url(transformation=transformations)
    qrcode_url = generate_and_upload_qr_code(new_url)
    print(qrcode_url)

    new_transformed_image = TransformedImage(transform_image_url=new_url, qrcode_image_url=qrcode_url,
                                             image_id=original_image.id)
    db.add(new_transformed_image)
    db.commit()
    db.refresh(new_transformed_image)
    return new_transformed_image


async def get_all_transformed_images(skip: int, limit: int, image_id: int, db: Session, current_user):
    """
     Функція get_all_transformed_images повертає список усіх трансформованих зображень для даного зображення.
         Функція приймає ціле число skip, limit і image_id як параметри. Він також приймає сеанс бази даних
         і об’єкт поточного користувача з контексту запиту.
     :param skip: int: Пропустити кілька зображень у базі даних
     :param limit: int: обмежує кількість повернутих трансформованих зображень
     :param image_id: int: фільтрувати перетворені зображення за image_id
     :param db: Сеанс: передає сеанс бази даних функції
     :param current_user: Отримати ідентифікатор поточного користувача
     :return: Список усіх трансформованих зображень для заданого зображення
     """
    transformed_list = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.image_id == image_id, Image.user_id == current_user.id)). \
        offset(skip).limit(limit).all()
    if not transformed_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transformed images for this image not found or user is not owner of this image")
    return transformed_list


async def get_transformed_img_by_id(transformed_id: int, db: Session, current_user):
    """
     Функція get_transformed_img_by_id приймає transformed_id і об’єкт db Session,
     і повертає TransformedImage із цим ідентифікатором. Якщо таке зображення не існує, воно викликає HTTPException.
     :param transformed_id: int: отримати трансформоване зображення за ідентифікатором
     :param db: Сеанс: передає сеанс бази даних функції
     :param current_user: Перевірте, чи має користувач доступ до цього зображення
     :return: Трансформоване зображення за його ідентифікатором
     """
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.id == transformed_id, Image.user_id == current_user.id)).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transformed image not found or user is not owner of this image")
    return transformed_image


async def delete_transformed_image_by_id(transformed_id: int, db: Session, user):
    """
     Функція delete_transformed_image_by_id видаляє трансформоване зображення з бази даних.
         Він приймає ціле число, що представляє ідентифікатор трансформованого зображення, яке потрібно видалити, і об’єкт Session для
         взаємодія з нашою базою даних. Функція повертає об’єкт TransformedImage, що представляє видалений
         трансформований образ.
     :param transformed_id: int: Ідентифікуйте трансформоване зображення, яке потрібно видалити
     :param db: Сеанс: доступ до бази даних
     :param user: Перевірте, чи користувач має право видаляти зображення
     :return: Видалене трансформоване зображення
     """
    if user.role == Role.admin:
        transformed_image = db.query(TransformedImage).join(Image). \
            filter(TransformedImage.id == transformed_id).first()
        if not transformed_image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transformed image not found")
        db.delete(transformed_image)
        db.commit()
        return transformed_image
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the admin can delete this data")


async def get_qrcode_transformed_image_by_id(transformed_id: int, db: Session, current_user):
    """
     Функція get_qrcode_transformed_image_by_id приймає transformed_id і db,
     і повертає перетворене зображення з цим ідентифікатором. Якщо таке зображення не існує, воно викликає HTTPException.
     :param transformed_id: int: отримати трансформоване зображення за ідентифікатором
     :param db: Сеанс: передає сеанс бази даних функції
     :param current_user: Перевірте, чи користувач увійшов у систему
     :return: Трансформоване зображення за id
     """
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.id == transformed_id, Image.user_id == current_user.id)).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transformed image not found or user is not owner of this image")
    print(transformed_image.qrcode_image_url)
    return transformed_image


async def get_url_transformed_image_by_id(transformed_id: int, db: Session, current_user):
    """
     Функція get_url_transformed_image_by_id приймає transformed_id і db,
     і повертає URL-адресу перетвореного зображення з цим ідентифікатором.
     :param transformed_id: int: отримати трансформоване зображення за ідентифікатором
     :param db: Сеанс: доступ до бази даних
     :param current_user: Перевірте, чи має користувач доступ до зображення
     :return: URL-адреса трансформованого зображення
     """
    transformed_image = db.query(TransformedImage).join(Image). \
        filter(and_(TransformedImage.id == transformed_id, Image.user_id == current_user.id)).first()
    if not transformed_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transformed image not found or user is not owner of this image")
    return transformed_image
