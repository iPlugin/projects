from fastapi import Depends, HTTPException, status
from sqlalchemy import desc, asc, func, String
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import or_

from src.database.models import Image, User, Tag, Rating, image_m2m_tag, Role
from src.database.db import get_db


def calc_average_rating(image_id, db: Session):
    """
     Функція calc_average_rating обчислює середню оцінку для даного зображення.
         Аргументи:
             image_id (int): ідентифікатор зображення, для якого потрібно обчислити середню оцінку.
     :param image_id: Ідентифікувати зображення в базі даних
     :param db: Сеанс: передайте сеанс бази даних, щоб ми могли використовувати його для запиту до бази даних
     :return: Середня оцінка зображення
     """
    image_ratings = db.query(Rating).filter(Rating.image_id == image_id).all()
    if len(image_ratings) == 0:
        return 0
    sum_user_rating = 0
    for element in image_ratings:
        if element.one_star:
            sum_user_rating += 1
        if element.two_stars:
            sum_user_rating += 2
        if element.three_stars:
            sum_user_rating += 3
        if element.four_stars:
            sum_user_rating += 4
        if element.five_stars:
            sum_user_rating += 5
    average_user_rating = sum_user_rating / len(image_ratings)
    return average_user_rating


async def get_img_by_user_id(user_id, skip, limit, filter_type, db, user):
    """
     Функція get_img_by_user_id використовується для отримання всіх зображень для конкретного користувача.
         Він приймає наступні параметри:
             - user_id: ідентифікатор користувача, зображення якого запитуються.
             - пропустити: кількість записів, які потрібно пропустити перед поверненням результатів (для розбиття на сторінки). Значення за замовчуванням 0.
             - обмеження: максимальна кількість записів для повернення (для розбиття на сторінки). Значення за замовчуванням 10.
     :param user_id: фільтрувати зображення за user_id
     :param skip: Пропустити перші n зображень
     :param limit: обмежує кількість зображень, що повертаються
     :param filter_type: Визначте, чи потрібно повертати зображення в порядку зростання чи спадання
     :param db: Зробіть запит до бази даних
     :param користувач: перевірте, чи є користувач адміністратором чи модератором
     :return: Список зображень для конкретного користувача
     """
    if user.role in (Role.admin, Role.moderator):
        if filter_type == "d":
            images = db.query(Image).filter(Image.user_id == user_id).order_by(desc(Image.created_at)).offset(
                skip).limit(limit).all()
        elif filter_type == "-d":
            images = db.query(Image).filter(Image.user_id == user_id).order_by(asc(Image.created_at)).offset(
                skip).limit(limit).all()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="parameter filter_type must be 'd" or '-d')
        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images for this user not found")
        return images
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin or moderator can get this data")


async def find_image_by_tag(skip: int, limit: int, search: str, filter_type: str, db: Session, user: User):
    """
     Функція find_image_by_tag використовує skip, limit, search string і filter_type.
     Потім він запитує в базі даних зображення, які відповідають рядку пошуку, і повертає їх користувачеві.
     :param skip: int: Пропустити кілька зображень
     :param limit: int: обмежити кількість зображень, що повертаються
     :param search: str: Пошук за назвою тегу
     :param filter_type: str: Визначити сортування зображень за датою в порядку зростання чи спадання
     :param db: Сеанс: доступ до бази даних
     :param user: Користувач: отримати user_id поточного зареєстрованого користувача
     :return: Список зображень
     """
    search = search.lower().strip()
    images = []

    if filter_type == "d":
        images = db.query(Image) \
            .join(image_m2m_tag). \
            join(Tag) \
            .filter(
            or_(func.cast(Image.description, String).op('~')(search), func.cast(Tag.name, String).op('~')(search))) \
            .order_by(desc(Image.created_at)) \
            .offset(skip).limit(limit).all()

    elif filter_type == "-d":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag) \
            .filter(
            or_(func.cast(Image.description, String).op('~')(search), func.cast(Tag.name, String).op('~')(search))) \
            .order_by(asc(Image.created_at)) \
            .offset(skip).limit(limit).all()

    elif filter_type == "r":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).filter(
            or_(func.cast(Image.description, String).op('~')(search), func.cast(Tag.name, String).op('~')(search))) \
            .offset(skip).limit(limit).all()

        images_rating_list = list(map(lambda x: (x.id, calc_average_rating(x.id, db)), images))
        sorted_images_rating_list = sorted(images_rating_list, key=lambda x: x[1], reverse=False)
        final_images = []
        for img_rating in sorted_images_rating_list:
            for image in images:
                if img_rating[0] == image.id:
                    image.rating = img_rating[1]
                    final_images.append(image)
        images = final_images

    elif filter_type == "-r":
        images = db.query(Image) \
            .join(image_m2m_tag) \
            .join(Tag).filter(
            or_(func.cast(Image.description, String).op('~')(search), func.cast(Tag.name, String).op('~')(search))) \
            .offset(skip).limit(limit).all()

        images_rating_list = list(map(lambda x: (x.id, calc_average_rating(x.id, db)), images))
        sorted_images_rating_list = sorted(images_rating_list, key=lambda x: x[1], reverse=True)
        final_images = []
        for img_rating in sorted_images_rating_list:
            for image in images:
                if img_rating[0] == image.id:
                    image.rating = img_rating[1]
                    final_images.append(image)
        images = final_images
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="parameter filter_type must be 'd' / '-d' for sorting by date or 'r' / '-r' for sorting by rating)")
    if not images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found for this tag")
    return images
