from django.urls import path
from . import views

urlpatterns = [path("", views.index, name="index"),
               path("codereview/login.html", views.login_view, name="login"),
               path("codereview/signup.html", views.signup_view, name="signup"),
               path("codereview/role.html", views.role_view, name="role"),
               path("codereview/privacy.html", views.privacy, name="privacy"),
               path("codereview/index.html", views.index, name = "index"),
               path("codereview/homepage.html",views.homepage, name = "homepage"),
               path("codereview/terms.html",views.terms, name = "terms"),
               path("codereview/login.html", views.logout_view, name="logout"),
               ]