# myblog/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # 原有的博客URL
    path('api/', include('blog.api_urls')),  # DRF API URL
    path('api-auth/', include('rest_framework.urls')),  # DRF 登录视图
    path('', RedirectView.as_view(url='/blog/')),
]