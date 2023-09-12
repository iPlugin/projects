from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment, Role
from src.repository.ratings import get_average_rating
from src.schemas.image_schemas import ImageUpdateModel, ImageAddModel, ImageAddTagModel
from src.services.images import images_service_normalize_tags


async def get_images(db: Session, user: User):
    """
     Функція get_images повертає список зображень та пов’язані з ними оцінки та коментарі.
         Якщо користувач є адміністратором, повертаються всі зображення. В іншому випадку повертаються лише власні зображення користувача.
     :param db: Сеанс: передайте сеанс бази даних функції
     :param user: Користувач: Визначте, чи є користувач адміністратором чи звичайним користувачем
     :return: Список словників, кожен словник містить об’єкт зображення та пов’язані з ним оцінки
     """
     # if user.role == Role.admin:
     # зображення = db.query(Image).order_by(Image.id).all()
     # ще:
    images = db.query(Image).order_by(Image.id).all()

    user_response = []
    for image in images:
        ratings = await get_average_rating(image.id, db)
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        user_response.append({"image": image, "ratings": ratings, "comments": comments})
    return user_response


async def get_image(db: Session, id: int, user: User):
    """
     Функція get_image приймає сеанс бази даних, ідентифікатор зображення та користувача.
     Якщо користувач є адміністратором, він повертає зображення з цим ідентифікатором із бази даних.
     В іншому випадку він повертає лише зображення з таким ідентифікатором, які належать цьому користувачу.
     :param db: Сеанс: отримати доступ до бази даних
     :param id: int: Укажіть ідентифікатор зображення, яке запитується
     :param user: Користувач: Перевірте, чи є користувач адміністратором
     :return: Кортеж із зображенням, оцінками та коментарями
     """
     # if user.role == Role.admin:
     # зображення = db.query(Image).filter(Image.id == id).first()
     # ще:
    image = db.query(Image).filter(Image.id == id).first()

    if image:
        ratings = await get_average_rating(image.id, db)
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        return image, ratings, comments
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def admin_get_image(db: Session, user_id: id):
    """
     Функція admin_get_image використовується для отримання всіх зображень для конкретного користувача.
         Функція приймає сеанс бази даних і user_id потрібного користувача.
         Потім він запитує всі зображення з цим конкретним ідентифікатором, упорядковує їх за ідентифікатором і повертає їх як масив об’єктів.
     :param db: Сеанс: підключення до бази даних
     :param user_id: id: отримати зображення певного користувача
     :return: Усі зображення в базі для конкретного користувача
     """
    images = db.query(Image).filter(Image.user_id == user_id).order_by(Image.id).all()
    if images:
        user_response = []
        for image in images:
            ratings = await get_average_rating(image.id, db)
            comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == image.user_id).all()
            user_response.append({"image": image, "ratings": ratings, "comments": comments})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return user_response


async def add_image(db: Session, image: ImageAddModel, tags: list[str], url: str, public_name: str, user: User):
    """
     Функція add_image додає зображення до бази даних.
         Аргументи:
             db (сеанс): об’єкт сеансу бази даних.
             зображення (ImageAddModel): Об’єкт ImageAddModel, що містить інформацію про нове зображення.
             теги (список[str]): список рядків, що представляють теги для цього нового зображення. Кожен тег — це рядок із максимальною довжиною 25 символів, і в нашій системі може бути до 5 тегів на зображення. Якщо вказано більше 5, лише перші п’ять будуть використані та збережені в нашій системі; будь-які додаткові будуть проігноровані цим викликом функції, але не будуть відкинуті
     :param tags:
     :param db: Сеанс: доступ до бази даних
     :param image: ImageAddModel: отримати опис зображення
     :param теги: список[str]: додайте теги до зображення
     :param url: str: зберегти URL-адресу зображення
     :param public_name: str: Збережіть назву зображення в базі даних
     :param user: Користувач: отримати ідентифікатор користувача з бази даних
     :return: Кортеж із двох елементів: зображення та рядок
     """
    if not user:
        return None

    detail = ""
    num_tags = 0
    image_tags = []
    for tag in tags:
        if len(tag) > 25:
            tag = tag[0:25]
        if not db.query(Tag).filter(Tag.name == tag.lower()).first():
            db_tag = Tag(name=tag.lower())
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
        if num_tags < 5:
            image_tags.append(tag.lower())
        num_tags += 1

    if num_tags >= 5:
        detail = " But be attentive you can add only five tags to an image"

    tags = db.query(Tag).filter(Tag.name.in_(image_tags)).all()
    # Зберегти картинку в базі даних
    db_image = Image(description=image.description, tags=tags, url=url, public_name=public_name, user_id=user.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image, detail


async def update_image(db: Session, image_id, image: ImageUpdateModel, user: User):
    """
     Функція update_image оновлює опис зображення в базі даних.
         Аргументи:
             db (сеанс): об’єкт сеансу SQLAlchemy.
             image_id (int): ідентифікатор зображення для оновлення.
             зображення (ImageUpdateModel): об’єкт ImageUpdateModel, що містить нові значення для оновлення наявного запису зображення в базі даних.

     :param db: Сеанс: доступ до бази даних
     :param image_id: Знайдіть зображення в базі даних
     :param image: ImageUpdateModel: передайте модель оновлення зображення
     :param user: Користувач: Перевірте, чи є користувач адміністратором
     :return: db_image
     """
    if user.role == Role.admin:
        db_image = db.query(Image).filter(Image.id == image_id).first()
    else:
        db_image = db.query(Image).filter(Image.id == image_id, Image.user_id == user.id).first()

    if db_image:
        db_image.description = image.description
        db.commit()
        db.refresh(db_image)
        return db_image
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def add_tag(db: Session, image_id, body: ImageAddTagModel, user: User):
    """
     Функція add_tag додає теги до зображення.
     :param db: Сеанс: доступ до бази даних
     :param image_id: Визначте зображення, до якого додано теги
     :param body: ImageAddTagModel: отримати теги з тіла запиту
     :param user: Користувач: Перевірте, чи є користувач адміністратором
     :return: Об’єкт зображення з оновленими тегами
     """
    tags = await images_service_normalize_tags(body)

    detail = ""
    num_tags = 0
    image_tags = []
    for tag in tags:
        if tag:
            if len(tag) > 25:
                tag = tag[0:25]
            if not db.query(Tag).filter(Tag.name == tag.lower()).first():
                db_tag = Tag(name=tag.lower())
                db.add(db_tag)
                db.commit()
                db.refresh(db_tag)
            if num_tags < 5:
                image_tags.append(tag.lower())
            num_tags += 1

    if num_tags >= 5:
        detail = "But be attentive you can add only five tags to an image"

    tags = db.query(Tag).filter(Tag.name.in_(image_tags)).all()

    if user.role == Role.admin:
        image = db.query(Image).filter(Image.id == image_id).first()
    else:
        image = db.query(Image).filter(Image.id == image_id, Image.user_id == user.id).first()

    if image:
        image.updated_at = datetime.utcnow()
        image.tags = tags
        db.commit()
        db.refresh(image)
        return image, detail
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def delete_image(db: Session, id: int, user: User):
    """
     Функція delete_image видаляє зображення з бази даних.
         Аргументи:
             db (сеанс): об’єкт сеансу бази даних.
             id (int): ідентифікатор зображення, яке потрібно видалити.
             користувач (Користувач): користувач, який видаляє зображення.
     :param db: Сеанс: доступ до бази даних
     :param id: int: Вкажіть ідентифікатор зображення, яке потрібно видалити
     :param user: Користувач: Перевірте, чи є користувач адміністратором
     :return: Видалене зображення
     """
    if user.role == Role.admin:
        db_image = db.query(Image).filter(Image.id == id).first()
    else:
        db_image = db.query(Image).filter(Image.id == id, Image.user_id == user.id).first()

    if db_image:
        db.delete(db_image)
        db.commit()
        return db_image
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
