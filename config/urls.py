from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("api/products/", views.product_list, name="product-list"),
    path("api/style-ai/", views.style_ai_chat, name="style-ai-chat"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.StoreLoginView.as_view(), name="login"),
    path("accounts/logout/", views.store_logout, name="logout"),
]
