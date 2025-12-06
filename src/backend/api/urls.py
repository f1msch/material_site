from django.urls import path, include

urlpatterns = [
    path('auth/', include('users.urls')),
    path('', include('material_site.urls')),
    path('payments/', include('payments.urls')),
    path('storage/', include('storage.urls')),
]
