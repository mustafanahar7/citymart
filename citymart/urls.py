"""
URL configuration for citymart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Appone import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SplashPage,name="splashpage"),
    path('home/',views.HomePage,name="homepage"),
    path('search/', views.search_view, name='search'),
    path('registration/',views.RegistrationPage,name="registrationpage"),
    path('login/',views.LoginPage,name="loginpage"),
    path('logout/',views.LogoutPage,name="logoutpage"),
    path('category/',views.CategoryPage,name="categorypage"),
    path('categorywise/<str:category>',views.CategoryWise,name="categorywisepage"),
    path('contact/',views.ContactPage,name="contactpage"),
    path('addcart/',views.Add_to_cart,name="add_to_cart"),
    path('cart/',views.Cart,name="cartpage"),
    path('remove-from-cart/',views.Remove_item_from_cart,name='remove_from_cart'),
    path('adminpage/',views.Admin_navbar,name='adminpage'),
    path('admindashboard/',views.Admin_dashboard,name='admindashboardpage'),
    path('ad_upload_product/',views.Upload_product,name='uploadproduct'),
    path('download_template/', views.download_product_template, name='download_template'),
    path('api/inventory-data/', views.get_inventory_data, name='get_inventory_data'),
    path('product-invenoty/', views.Product_inventory, name='admin_product_inventory'),
    path('admin-order/', views.Admin_orders, name='admin_orders'),
    path('admin-order-items/<str:order_number>', views.Admin_order_items, name='admin_order_items'),
    path('customers/', views.Customers, name='customers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)