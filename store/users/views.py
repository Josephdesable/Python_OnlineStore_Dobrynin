from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm

# Create your views here.

# users/views.py



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")  # или куда хочешь
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})
