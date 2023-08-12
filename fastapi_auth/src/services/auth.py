
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.conf.config import settings
from src.conf.messages import AuthMessages
from src.database.db import get_db
from src.repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.jwt_secret_key
    ALGORITHM = settings.jwt_algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password):
        """
         Функція verify_password приймає простий текстовий пароль і хешує його
         пароль як аргументи. Потім він використовує об’єкт pwd_context, щоб перевірити, що
         простий текстовий пароль збігається з хешованим.
         :param plain_password: Перевірте, чи пароль, введений користувачем, збігається з тим, що зберігається в базі даних
         :param hashed_password: Перевірте пароль, який передається, зі збереженим хешованим паролем
         в базі даних
         :return: True, якщо plain_password правильний, і false в іншому випадку
         """

        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
         Функція get_password_hash приймає пароль як вхідні дані та повертає хеш цього пароля.
         Хеш генерується за допомогою об’єкта pwd_context, який є екземпляром класу Bcrypt Flask-Bcrypt.
         :param password: str: Вкажіть пароль, який буде хешовано
         :return: Рядок, який є хешем пароля
         """
        return self.pwd_context.hash(password)

    # визначте функцію для створення нового маркера доступу
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
         Функція create_access_token створює новий маркер доступу.
         :param data: dict: передати дані, які будуть закодовані в маркері доступу
         :param expires_delta: Необов’язково [float]: установіть час закінчення терміну дії маркера
         :return: Закодований маркер доступу
         """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token


    # визначте функцію для створення нового маркера оновлення
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
         Функція create_refresh_token створює маркер оновлення для користувача.
         :param data: dict: передати інформацію про користувача, наприклад ім’я користувача та електронну адресу
         :param expires_delta: Необов’язково [float]: установіть час закінчення терміну дії маркера оновлення
         :return: Закодований маркер, який містить передані йому дані, а також мітку часу
         дата створення маркера та термін дії
         """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
         Функція decode_refresh_token використовується для декодування маркера оновлення.
         Він приймає refresh_token як аргумент і повертає електронну адресу користувача, якщо вона дійсна.
         Якщо ні, виникає HTTPException із кодом статусу 401 (НЕАВТОРИЗОВАНО)
         і докладно «Не вдалося перевірити облікові дані».
         :param refresh_token: str: Передайте маркер оновлення функції
         :return: Електронна адреса користувача, пов’язана з маркером оновлення
         """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_scope_for_token)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=AuthMessages.could_not_validate_credentials)

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
         Функція get_current_user — це залежність, яка використовуватиметься в
         захищені кінцеві точки. Він приймає маркер як аргумент і повертає користувача
         якщо він дійсний, інакше викликає HTTPException із кодом статусу 401.
         :param token: str: отримати маркер із заголовка авторизації
         :param db: Сеанс: передає сеанс бази даних функції
         :return: Об’єкт користувача
         """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthMessages.could_not_validate_credentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Декодувати JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
     
        user = await repository_users.get_user_by_email(email, db)

        return user

    def create_email_token(self, data: dict):
        """
         Функція create_email_token приймає словник даних і повертає маркер.
         Маркер створюється шляхом кодування даних за допомогою SECRET_KEY і ALGORITHM,
         і додавання до нього мітки часу iat (випущено о) та мітки часу exp (термін дії).
         :param data: dict: передати дані, які будуть закодовані в маркер
         :return: Жетона
         """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        Функція get_email_from_token приймає маркер як аргумент
         і повертає адресу електронної пошти, пов’язану з цим маркером.
         Функція використовує бібліотеку jwt для декодування маркера, який потім використовується для повернення електронної адреси.
         :param token: str: передати маркер, який надсилається на електронну адресу користувача
         :return: Адреса електронної пошти користувача, який зараз увійшов у систему
         """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=AuthMessages.invalid_token_for_email_verification)


auth_service = Auth()
