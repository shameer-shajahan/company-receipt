"""
URL configuration for dataentry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rcp import views
from rcp.views import ManageItemsView, generate_items_pdf, send_items_email

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("signout/",views.SignOutView.as_view(),name="signout"),
    # path("add/",views.ReciptAddView.as_view(),name="recipt-add"),
    path('receipt/',views.CreateDeliveryReceiptView.as_view(), name='create_receipt'),
    path('manage-items/', ManageItemsView.as_view(), name='manage_items'),
    path('manage-items/pdf/', generate_items_pdf, name='generate_items_pdf'),
    path('manage-items/email/', send_items_email, name='send_items_email'),
    path('data/<int:pk>/remove',views.DataDeleteView.as_view(),name="delete"),

 # Correct usage
    # path('receipt/',views.CreateDeliveryReceiptView.as_view(), name='create_receipt'),  # Correct usage
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)