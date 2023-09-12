from collections import OrderedDict

from fastapi import HTTPException, status

from src.database.models import Image
from src.schemas.image_schemas import ImageAddModel


async def images_service_change_name(public_name, db):
    """
     Функція images_service_change_name приймає public_name і db.
     Потім він перевіряє, чи public_name вже зайнято іншим зображенням, і якщо так, він додає суфікс до кінця
     назву, доки не залишиться дублікатів. Він повертає цю нову назву.
     :param public_name: Перевірте, чи ім’я вже використовується
     :param db: Доступ до бази даних
     :return: Ім'я, яке не використовується в базі даних
     """
    correct_public_name = public_name
    suffix = 1

    while db.query(Image).filter(Image.public_name == correct_public_name).first():
        suffix += 1
        correct_public_name = f"{public_name}_{suffix}"

    return correct_public_name


async def images_service_normalize_tags(body):
    """
     Функція images_service_normalize_tags отримує список тегів і повертає список унікальних нормалізованих тегів.
         Аргументи:
             тіло (список): список рядків, що представляють теги зображення.
     :param body: отримати теги з тіла запиту
     :return: Список тегів без дублікатів
     :doc-author: Трелент
     """
    tags = [tag[:25].strip() for tag_str in body.tags for tag in tag_str.split(",") if tag]
    correct_tags = list(OrderedDict.fromkeys(tags))
    return correct_tags
