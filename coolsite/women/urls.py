from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    # path(r'', index, name='home'),
    path(r'', WomenHome.as_view(), name='home'), #cache_page(second*minute/hour)(WomenHome.as_view())
    # path(r'cats/<int:catid>/', categories), #str int slug uuid path
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
    # path(r'about/', about, name='about'),
    path(r'about/', About.as_view(), name='about'),
    # path(r'addpage/', addpage, name='add_page'),
    path(r'addpage/', AddPage.as_view(), name='add_page'),
    # path(r'contact/', contact, name='contact'),
    path(r'contact/', ContactFormView.as_view(), name='contact'),
    # path(r'login/', login, name='login'),
    path(r'login/', LoginUser.as_view(), name='login'),
    path(r'logout/', logout_user, name='logout'),
    # path(r'post/<slug:post_slug>', show_post, name='post'),
    path(r'post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path(r'category/<slug:cat_slug>/', show_category, name='category'),
    path(r'category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path(r'register/', RegisterUser.as_view(), name='register'),
    path(r'not_valid_data/', not_valid_data, name='not_valid_data'),
    # path(r'new', Ajax.as_view(), name='new'),
    path(r'password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path(r'password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path(r'password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path(r'password-reset-complite', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]