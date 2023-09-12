from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.schemas.user_schemas import UserModel, UserResponse
from src.schemas.auth_schemas import TokenModel, RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email
from src.conf.messages import AuthMessages

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
     Функція реєстрації створює нового користувача в базі даних.
         Він приймає об’єкт UserModel як вхідні дані, які перевіряються pydantic.
         Пароль хешується і зберігається в базі даних.
         На електронну адресу користувача надсилається лист із посиланням для активації.
     :param body: UserModel: передати дані з тіла запиту до нашої функції
     :param background_tasks: Фонові завдання: Додати завдання до фонової черги
     :param запит: Запит: отримати базову URL-адресу програми
     :param db: Сеанс: отримати сеанс бази даних
     :return: Об’єкт користувача
     """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=AuthMessages.account_already_exists)
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
     Функція входу використовується для автентифікації користувача.
         Він бере ім’я користувача та пароль із тіла запиту,
         перевіряє їх правильність і повертає маркер доступу.
     :param body: OAuth2PasswordRequestForm: отримати ім’я користувача та пароль із тіла запиту
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Відповідь json із маркером доступу та маркером оновлення
     """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_email)
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.email_not_confirmed)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_password)
    if user.banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AuthMessages.banned)
    # Генерувати JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
     Функція refresh_token використовується для оновлення маркера доступу.
         Функція приймає маркер оновлення та повертає access_token, новий refresh_token і тип маркера.
         Якщо поточний refresh_token користувача не відповідає тому, що було передано в цю функцію, вона поверне помилку.
     :param credentials: HTTPAuthorizationCredentials: отримати маркер із заголовка запиту
     :param db: Сеанс: передає сеанс бази даних функції
     :return: Словник із access_token, refresh_token і типом маркера
     """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_refresh_token)
    if user.banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AuthMessages.banned)

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
     Функція confirmed_email використовується для підтвердження електронної адреси користувача.
     Він бере маркер із URL-адреси та використовує його для отримання електронної адреси користувача.
     Потім функція перевіряє, чи є користувач із такою електронною поштою в нашій базі даних, і якщо ні, повертає повідомлення про помилку.
     Якщо в нашій базі даних є користувач із такою електронною адресою, ми перевіряємо, чи його обліковий запис уже підтверджено.
     Якщо це вже підтверджено, ми повертаємо інше повідомлення про помилку з таким повідомленням; інакше ми називаємо repository_users
     функція confirmed_email, яка встановлює значення для поля «підтверджено» цього конкретного запису
     :param token: str: Отримати маркер з URL-адреси
     :param db: Сеанс: доступ до бази даних
     :return: Повідомлення про те, що електронна адреса вже підтверджена, або повідомлення про те, що її підтверджено
     """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AuthMessages.verification_error)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
     Функція request_email використовується для надсилання електронного листа користувачеві з посиланням, яке дозволить йому
     щоб підтвердити свій обліковий запис. Функція приймає об’єкт RequestEmail, який містить електронну пошту
     користувач, який хоче підтвердити свій обліковий запис. Потім він перевіряє, чи вже є підтверджений користувач
     цю адресу електронної пошти, і якщо так, повертає повідомлення про помилку про те, що вони вже підтверджені. Якщо ні, надсилає
     електронний лист із посиланням для підтвердження.
     :param body: RequestEmail: отримати електронний лист із тіла запиту
     :param background_tasks: BackgroundTasks: Додати завдання до черги фонових завдань
     :param запит: Запит: отримати базову URL-адресу сервера
     :param db: Сеанс: отримати сеанс бази даних
     :return: Повідомлення для користувача
     """
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": AuthMessages.your_email_is_already_confirmed}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": AuthMessages.check_your_email_for_confirmation}
