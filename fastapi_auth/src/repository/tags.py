from typing import List, Type

from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas.tag_schemas import TagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[Type[Tag]]:
    """
     Функція get_tags повертає список тегів із бази даних.
     :param skip: int: Пропустити ряд записів у базі даних
     :param limit: int: обмежити кількість результатів, що повертаються
     :param db: Сеанс: доступ до бази даних
     :return: Список об’єктів тегів
     """
    return db.query(Tag).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, db: Session) -> Type[Tag] | None:
    """
     Функція get_tag повертає об’єкт Tag із бази даних. 
     :param tag_id: int: Відфільтрувати запит, щоб повернути лише тег з ідентифікатором, який відповідає параметру
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об’єкт тегу
     """
    return db.query(Tag).filter(Tag.id == tag_id).first()


async def create_tag(body: TagModel, db: Session) -> Tag:
    """
     Функція create_tag створює новий тег у базі даних.
     Функція create_tag приймає об’єкт TagModel як вхідні дані та повертає об’єкт Tag.
     :param body: TagModel: передати дані, які надсилаються в API
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Тег
     """
    tag = Tag(name=body.name.lower())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    """
     Функція update_tag оновлює тег у базі даних.
         Аргументи:
             tag_id (int): ідентифікатор тегу для оновлення.
             body (TagModel): оновлений об’єкт TagModel з новими значеннями для імені та опису.
             db (сеанс): екземпляр сеансу, який використовується для запиту до бази даних.
         Повернення:
             Тег | Немає: у разі успіху повертає оновлений об’єкт Tag; інакше повертає None.
     :param tag_id: int: Визначте тег, який потрібно оновити
     :param body: TagModel: введіть нову назву тегу
     :param db: Сеанс: доступ до бази даних
     :return: Об’єкт тегу
     """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        new_tag_name_in_base = db.query(Tag).filter(Tag.name == body.name.lower()).first()
        if new_tag_name_in_base:
            return None
        tag.name = body.name.lower()
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    """
     Функція remove_tag видаляє тег із бази даних.
     :param tag_id: int: Вкажіть ідентифікатор тегу, який потрібно видалити
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Об’єкт тегу
     """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    """
     Функція remove_tag видаляє тег із бази даних.
     :param tag_id: int: Вкажіть ідентифікатор тегу, який потрібно видалити
     :param db: Сеанс: доступ до бази даних
     :return: Об’єкт тегу
     """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag


async def get_tag_by_name(tag_name: str, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.name == tag_name.lower()).first()
    return tag
