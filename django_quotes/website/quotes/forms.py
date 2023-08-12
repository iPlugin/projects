from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, ModelChoiceField, Select, SelectMultiple

from .models import Author, Tag, Quote


class AuthorForm(ModelForm):
    fullname = CharField(
        max_length=50,
        min_length=3,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter his fullname",
            'id': "fullname"}))
    born_date = CharField(
        max_length=50,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter his bitrhday",
            "id": "born_date"}))
    born_location = CharField(
        max_length=150,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter his where was born",
            "id": "born_location"}))
    description = CharField(
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter something about him",
            "id": "description"}))
    picture = CharField(
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter data:image/jpeg;base64...",
            "id": "picture"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description', 'picture']


class TagForm(ModelForm):
    name = CharField(
        max_length=50,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "New name tag",
            "id": "name"}))

    class Meta:
        model = Tag
        fields = ["name"]


class QuoteForm(ModelForm):
    quote = CharField(
        min_length=5,
        required=True,
        widget=TextInput({
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "New name quote",
            "id": "quote"}))
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("name"),
        required=True,
        widget=SelectMultiple({
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Chose tags",
            "id": "tags"}))
    author = ModelChoiceField(
        queryset=Author.objects.all().order_by("fullname"),
        widget=Select({
            'class': "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Chose author",
            'id': "author"}))

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']