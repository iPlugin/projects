from pathlib import Path

import logging
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from src.conf.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="PhotoNet",  # TODO Change name
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
     Функція send_email надсилає користувачеві електронний лист із посиланням для підтвердження електронної адреси.
     Функція приймає три параметри:
     -email: EmailStr, адреса електронної пошти користувача, яку він ввів під час реєстрації облікового запису.
     -username: str, ім’я користувача, який намагається зареєструвати обліковий запис. Це буде використано в
     поєднання з хостом (див. нижче) і token_verification (див. нижче) як частину URL-адреси, яка буде надіслана
     електронною поштою, щоб підтвердити їх особу та надати їм доступ до нашої системи.
     :param email: EmailStr: Вкажіть адресу електронної пошти одержувача
     :param ім'я користувача: str: Передайте ім'я користувача в шаблон
     :param host: str: Створіть посилання на інтерфейс
     :return: Об'єкт співпрограми
     """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        print(token_verification)
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        logging.error(err)
