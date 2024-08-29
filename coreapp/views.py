from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    designers = Designer.verified.all()
    styles = Style.published.all()
    context = {
        "designers": designers,
        "styles": styles
    }
    return render(request, 'core/index.html', context)
