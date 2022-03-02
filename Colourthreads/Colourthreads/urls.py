"""Colourthreads URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from adminCT import views as admin_views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',include("home.urls")),
    path("orders/<cid>",admin_views.view_orders,name="orders"),
    path("Cart/<cid>",admin_views.view_cart,name="cart"),
    path("login/", include("adminCT.urls")),
    path("wishlist/<cid>",admin_views.view_wishlist,name="Wishlist"),
    path("<CID>/<CAT>",admin_views.Disp_by_Category, name="Display_by_category"),
    path("signup/", admin_views.SignUpView, name="SignUp"),
    path("logout/", admin_views.LogoutView, name="Logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
