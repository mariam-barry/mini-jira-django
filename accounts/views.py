from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile') # On redirige vers le profil après l'inscription
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required # Seuls les utilisateurs connectés peuvent voir leur profil
def profile_view(request):
    return render(request, 'accounts/profile.html')