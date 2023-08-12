from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Rating, User, Image
from src.schemas.rating_schemas import RatingModel

from fastapi import HTTPException


async def get_average_rating(image_id, db: Session):
    """
     Функція get_average_rating приймає image_id і сеанс бази даних.
     Потім він запитує таблицю рейтингів для всіх рейтингів, пов’язаних із цим image_id.
     Якщо оцінок немає, повертається 0 як середня оцінка. Якщо є рейтинги,
     він підсумовує всі значення зірок (одна зірка = 1 бал, дві зірки = 2 бали тощо)
     і ділиться на загальну кількість голосів, щоб отримати середній рейтинг.
     :param image_id: Знайдіть зображення в базі даних
     :param db: Сеанс: доступ до бази даних
     :return: Середня оцінка зображення з заданим ідентифікатором
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


async def get_rating(rating_id: int, db: Session) -> Rating:
    """
     Функція get_rating повертає об’єкт рейтингу з бази даних.
     :param rating_id: int: Вкажіть ідентифікатор рейтингу, який ви хочете отримати
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об’єкт рейтингу, який є моделлю sqlalchemy
     """
    return db.query(Rating).filter(Rating.id == rating_id).first()


def get_image(db: Session, image_id: int):
    """
     Функція get_image повертає об’єкт зображення з бази даних.
         Якщо зображення не знайдено, виникає помилка 404.
     :param db: Сеанс: передає сеанс бази даних функції
     :param image_id: int: фільтрувати зображення за ідентифікатором
     :return: Один об’єкт зображення
     """
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


async def create_rating(image_id: int, body: RatingModel, user: User, db: Session) -> Rating:
    """
     Функція create_rating створює новий рейтинг для зображення.
         Аргументи:
             image_id (int): ідентифікатор зображення, яке буде оцінено.
             тіло (RatingModel): об’єкт RatingModel, що містить інформацію про рейтинг.
             користувач (User): Користувач, який створює рейтинг.
             db (сеанс): об’єкт сеансу бази даних, який використовується для запиту та внесення змін до бази даних.
     :param image_id: int: отримати зображення з бази даних
     :param body: RatingModel: передати дані з тіла запиту в цю функцію
     :param user: Користувач: отримати ідентифікатор користувача, який увійшов у систему
     :param db: Сеанс: доступ до бази даних
     :return: Об'єкт рейтингу
     """
    image_in_database = get_image(db, image_id)
    if image_in_database.user_id == user.id:
        return None
    sum_of_rates = 0
    for el in body:
        if el[1]:
            sum_of_rates += 1
    if sum_of_rates != 1:
        return None
    rating_in_database = db.query(Rating).filter(Rating.image_id == image_id, Rating.user_id == user.id).first()
    if rating_in_database:
        return rating_in_database
    rating = Rating(one_star=body.one_star, two_stars=body.two_stars, three_stars=body.three_stars,
                    four_stars=body.four_stars, five_stars=body.five_stars, user_id=user.id, image_id=image_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


async def update_rating(rating_id: int, body: RatingModel, db: Session):
    """
     Функція update_rating оновлює рейтинг у базі даних.
     :param rating_id: int: Визначте, який рейтинг оновити
     :param body: RatingModel: отримати дані з тіла запиту
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об’єкт рейтингу, якщо рейтинг існує в базі даних
     """
    sum_of_rates = 0
    for el in body:
        if el[1]:
            sum_of_rates += 1
    if sum_of_rates > 1:
        return None
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        rating.one_star = body.one_star
        rating.two_stars = body.two_stars
        rating.three_stars = body.three_stars
        rating.four_stars = body.four_stars
        rating.five_stars = body.five_stars
        db.commit()
    return rating


async def remove_rating(rating_id: int, db: Session):
    """
     Функція remove_rating видаляє оцінку з бази даних.
     :param rating_id: int: Повідомте функції, який рейтинг потрібно видалити
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об'єкт рейтингу
     """
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        db.delete(rating)
        db.commit()
    return rating
