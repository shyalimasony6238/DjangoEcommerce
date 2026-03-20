"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from backend.views import *
from frontend .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    # CATEGORY
    path("c_form/",c_form),
    path("c_save/",c_save,name="c_save"),
    path("c_table/",c_table),
    path("c_delete/<int:dataid>/",c_delete,name="c_delete"),
    path("c_edit/<int:dataid>/",c_edit,name="c_edit"),
    # PRODUCT
       path("p_form/",pro_form),
       path("p_save/",pro_save,name="p_save"),
       path("p_table/",p_table),
       path("p_delete/<int:dataid>/",p_delete,name="p_delete"),
       path("p_edit/<int:dataid>/",p_edit,name="p_edit"),

# FRONTEND

  path("gi",index,name="index"),
  path("about/",about,name="about"),
  path("category/",category,name="category"),
  path('product/<int:cat_id>/', product, name='product'),
  path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
  path('cart/', view_cart, name='view_cart'),
  path('update_cart/', update_cart, name='update_cart'),
  path("login/", login_view, name="login"),


  path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
