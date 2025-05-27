from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CodeReview
from .generation import generate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(response):
    return render(response,"codereview/index.html",{})

def login_view(request):
    if request.method == "POST":
        name = request.POST.get("email")  # username or email
        password = request.POST.get("password")

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, "codereview/login.html", {"error": "Invalid credentials"})

    return render(request, "codereview/login.html", {})

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        con_pass = request.POST.get("con_pass")

        if password != con_pass:
            return render(request, "codereview/signup.html", {'error': "Passwords do not match"})

        if User.objects.filter(username=name).exists():
            return render(request, "codereview/signup.html", {'error': "Username already exists"})

        user = User.objects.create_user(username=name, email=email, password=password)
        login(request, user)  # Log the user in directly after signup
        return redirect('role')  # Send to role selection

    return render(request, "codereview/signup.html")

@login_required
def role_view(request):
    if request.method == "POST":
        selected_role = request.POST.get("role")  # Assuming 'role' is posted in the form
        user = request.user

        # Update the role in the profile model
        user.profile.role = selected_role  # Saves the role in the profile model
        user.profile.save()  # Save the profile

        return redirect('homepage')  # Redirect to any page after saving the role

    return render(request, "codereview/role.html", {})


@login_required
def homepage(request):
    user = request.user
    code_reviews = CodeReview.objects.filter(user=user)
    selected_review = None
    review_text = ""
    code = ""

    if request.method == "POST":
        selected_review_id = request.POST.get("selected_review")
        action = request.POST.get("action")
        code = request.POST.get("code", "")

        if selected_review_id:
            try:
                selected_review = CodeReview.objects.get(id=selected_review_id, user=user)
                code = selected_review.code
                if action == "error":
                    review_text = selected_review.error_response
                elif action == "enhance":
                    review_text = selected_review.enhance_response
                elif action == "optimize":
                    review_text = selected_review.optimize_response
            except CodeReview.DoesNotExist:
                pass

        elif code.strip():  # Handle new code submission
            selected_review = CodeReview.objects.filter(user=user, code=code).first()

            if not selected_review:
                # Generate review
                g = generate(code)

                selected_review = CodeReview.objects.create(
                    user=user,
                    code_name=g[0],
                    code=code,
                    error_response=g[1],
                    enhance_response=g[2],
                    optimize_response=g[3],
                )

            if action == "error":
                review_text = selected_review.error_response
            elif action == "enhance":
                review_text = selected_review.enhance_response
            elif action == "optimize":
                review_text = selected_review.optimize_response

    context = {
        "code_reviews": code_reviews,
        "selected_review": selected_review,
        "review": review_text,
        "code": code,
    }
    return render(request, "codereview/homepage.html", context)


def terms(response):
    return render(response,"codereview/terms.html",{})

def logout_view(request):
    logout(request)
    return redirect('login')

def privacy(request):
    return render(request, 'codereview/privacy.html')