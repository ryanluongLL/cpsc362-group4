from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import UserAccount, UserProfile


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not email or not password:
            return render(
                request, "accounts/signup.html", {"error": "All fields are required."}
            )

        if UserAccount.objects.filter(username=username).exists():
            return render(
                request, "accounts/signup.html", {"error": "Username already taken."}
            )

        if UserAccount.objects.filter(email=email).exists():
            return render(
                request, "accounts/signup.html", {"error": "Email already in use."}
            )

        # hash the password
        hashed_pw = make_password(password)
        user = UserAccount.objects.create(
            username=username, email=email, password=hashed_pw
        )
        UserProfile.objects.create(user=user)
        request.session["user_id"] = user.id
        return redirect("/")
    return render(request, "accounts/signup.html")


def signin_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        try:
            user = UserAccount.objects.get(username=username)
        except UserAccount.DoesNotExist:
            return render(
                request,
                "accounts/signin.html",
                {"error": "Invalid username or password."},
            )
        if not check_password(password, user.password):
            return render(
                request,
                "accounts/signin.html",
                {"error": "Invalid username or password."},
            )

        request.session["user_id"] = user.id
        return redirect("/")
    return render(request, "accounts/signin.html")


def signout_view(request):
    request.session.flush()  # Clears everything in the session
    return redirect("/")


def profile_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("/accounts/signin/")

    user = UserAccount.objects.filter(id=user_id).first()
    if not user:
        return redirect("/accounts/signin/")

    profile = UserProfile.objects.filter(user=user).first()

    if request.method == "POST":
        profile.first_name = request.POST.get("first_name", "").strip()
        profile.last_name = request.POST.get("last_name", "").strip()
        profile.phone_number = request.POST.get("phone_number", "").strip()
        profile.save()
        return redirect("/accounts/profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "user": user,
            "profile": profile,
        },
    )
