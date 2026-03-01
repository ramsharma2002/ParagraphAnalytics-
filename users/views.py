from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User


# REGISTER VIEW
def register_view(request):
    """Handle user registration."""
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        try:
            User.objects.create_user(
                email=email,
                username=username,
                password=password
            )
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect("register")

    return render(request, "register.html")


# LOGIN VIEW
def login_view(request):
    """Handle user authentication."""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            print("#############", user)
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "login.html")


# LOGOUT VIEW
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect("login")