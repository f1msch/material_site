# payments/urls.py
from django.urls import path
from . import views
from .views import MaterialUploadView

urlpatterns = [
    path('upload/', MaterialUploadView.as_view(), name='upload'),
]