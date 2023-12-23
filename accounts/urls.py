from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
from .views import (
    favorite_add,
    delete_recipe,
    user_private_recipe_new,
    signup_view,
    login_view,
    logout_view,
    delete_account,
    profile_view,
)

app_name = "accounts"

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')

urlpatterns = [
    path("fav/<int:id>/", favorite_add, name="favorite_add"),
    path("delete/<int:id>/", delete_recipe, name="delete_recipe"),
    path("recipe/new/", user_private_recipe_new, name="user_private_recipe_new"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("delete_account/", delete_account, name="delete_account"),
    path("profile/", profile_view, name="profile"),

    path("password_reset/", 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html', 
             email_template_name = 'registration/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done')),
        name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
]
