import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from fastapi_limiter import FastAPILimiter
from src.conf.config import settings
from src.database.db import engine
from src.database.models import User, Image, Tag, Comment, TransformedImage, Rating
from src.routes import transformed_images, auth, tags, comments_routes, images, ratings, users, search


# Стоврюємо екземпляр FastApi, встановлюємо назву додатка в swagger та відсоруємо роути по методам:
app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"}, title='PhotoNet app')


# створюємо адмінку
admin = Admin(app, engine)


# визначаємо зміст адмінки: якими моделями бази даних і якими полями хочемо керувати через адмінку:
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]
    column_searchable_list = [User.username]
    column_sortable_list = [User.id]
    column_default_sort = [(User.email, True), (User.username, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class ImageAdmin(ModelView, model=Image):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class TagAdmin(ModelView, model=Tag):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class CommentAdmin(ModelView, model=Comment):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class TransformedImageAdmin(ModelView, model=TransformedImage):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class RatingAdmin(ModelView, model=Rating):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


admin.add_view(UserAdmin)
admin.add_view(ImageAdmin)
admin.add_view(TagAdmin)
admin.add_view(CommentAdmin)
admin.add_view(RatingAdmin)
admin.add_view(TransformedImageAdmin)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


app.include_router(comments_routes.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(transformed_images.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(images.router, prefix='/api')
app.include_router(ratings.router, prefix='/api')
app.include_router(search.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
