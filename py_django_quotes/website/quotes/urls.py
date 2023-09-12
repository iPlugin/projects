from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name='home'),
    path("page/<int:page>/", views.main, name='home_paginate'),

    path("author/<int:_id>/", views.author, name='author'),

    path("form_author/", views.form_author, name='form_author'),
    path("form_tag/", views.form_tag, name='form_tag'),
    path("form_quote/", views.form_quote, name='form_quote')
]
