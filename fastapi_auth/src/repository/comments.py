from sqlalchemy.orm import Session

from src.database.models import Comment, Image
from src.schemas.comment_schemas import CommentModel


async def get_comments(db: Session):
    """
     Функція get_comments повертає всі коментарі в базі даних.
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Всі коментарі з бази
     """
    return db.query(Comment).all()


async def get_comment_by_id(comment_id: int, db: Session):
    """
     Функція get_comment_by_id повертає об’єкт коментаря з бази даних на основі його ідентифікатора.
     :param comment_id: int: фільтрувати базу даних для певного коментаря
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об’єкт коментаря
     """
    return db.query(Comment).filter_by(id=comment_id).first()


async def create_comment(body: CommentModel, db: Session):
    """
     Функція create_comment створює новий коментар у базі даних.
     :param body: CommentModel: передайте дані для створення нового коментаря
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об’єкт коментаря
     """
    comment = Comment(**body.dict())
    db.add(comment)
    db.commit()
    return comment


async def update_comment(body: CommentModel, comment_id, db: Session):
    """
     Функція update_comment оновлює коментар у базі даних.
         Аргументи:
             body (CommentModel): об’єкт CommentModel для оновлення.
             comment_id (int): ідентифікатор об’єкта CommentModel для оновлення.
             db (сеанс, необов’язково): екземпляр сеансу SQLAlchemy. За замовчуванням немає.
         Повернення:
             Необов’язково [Коментар]: словник, що містить інформацію про оновлений коментар, або «Немає», якщо такого коментаря немає.
     :param body: CommentModel: передати оновлений коментар у функцію
     :param comment_id: отримати коментар із бази даних
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об'єкт коментаря
     """
    comment = await get_comment_by_id(comment_id, db)
    if comment:
        comment.comment = body.comment
        db.commit()
    return comment


async def remove_comment(comment_id, db: Session):
    """
     Функція remove_comment видаляє коментар із бази даних.
         Аргументи:
             comment_id (int): ідентифікатор коментаря, який потрібно видалити.
             db (сеанс): підключення до бази даних.
         Повернення:
             Коментар: видалений об’єкт «Коментар».
     :param comment_id: Знайдіть коментар, який потрібно видалити
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Коментар, який було видалено
     """
    comment = await get_comment_by_id(comment_id, db)
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def get_image_by_id(image_id: int, db: Session):
    """
     Функція get_image_by_id приймає image_id і сеанс бази даних,
     і повертає об’єкт Image із цим ідентифікатором. Якщо такого зображення не існує, повертається None.
     :param image_id: int: Вкажіть ідентифікатор зображення, яке потрібно отримати
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Зображення з указаним ідентифікатором
     """
    image = db.query(Image).filter_by(id=image_id).first()
    return image
