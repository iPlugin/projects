from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Quote
from .forms import AuthorForm, TagForm, QuoteForm
from .models import Author, Tag


def main(request, page = 1):
    quotes = Quote.objects.all()
    per_page = 12
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/home.html', context={'quotes': quotes_on_page})


@login_required
def form_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:form_tag")
        else:
            return render(request, "quotes/home.html", context={'form': AuthorForm()})
    return render(request, "quotes/form_author.html", context={'form': AuthorForm()})


@login_required
def form_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:form_quote")
        else:
            return render(request, "quotes/home.html", context={'form': TagForm()})
    return render(request, "quotes/form_tag.html", context={'form': TagForm()})


@login_required
def form_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:home")
        else:
            return render(request, "quotes/home.html", context={'form': QuoteForm()})
    return render(request, "quotes/form_quote.html", context={'form': QuoteForm()})


def author(request, _id):
    author = Author.objects.get(pk=_id)
    return render(request, 'quotes/author.html', context={'author': author})