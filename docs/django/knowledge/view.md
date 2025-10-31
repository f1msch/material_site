## Django 和 DRF 视图类完整指南
### Django 内置通用视图类
* 基础视图类

|  类名	|  作用	|  主要方法  |
|  ----  |  ----  |  ----  |
|View	|所有类视图的基类	|get(), post(), put(), delete()
|TemplateView	|渲染模板的视图	|get_context_data()
|RedirectView	|重定向到其他URL	|get_redirect_url()
```python
from django.views.generic import View, TemplateView, RedirectView

class HomeView(TemplateView):
    template_name = 'home.html'

class OldUrlRedirect(RedirectView):
    url = '/new-url/'
```

* 显示视图 (Display Views)

| 类名	| 作用	| 主要属性
|  ----  |  ----  |  ----  |
|ListView	|显示对象列表	|model, queryset, template_name
|DetailView	|显示单个对象详情	|model, queryset, template_name
|ArchiveIndexView	|日期归档索引	|model, date_field
|YearArchiveView	|按年份归档	|model, date_field, year
|MonthArchiveView	|按月归档	|model, date_field, year, month
|DayArchiveView	|按日归档	|model, date_field, year, month, day
|TodayArchiveView	|今日归档	|model, date_field
|DateDetailView	|日期详情视图	|model, date_field
```python
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView

class ArticleListView(ListView):
    model = Article
    paginate_by = 10

class ArticleDetailView(DetailView):
    model = Article

class ArticleArchiveView(ArchiveIndexView):
    model = Article
    date_field = 'pub_date'
```

* 编辑视图 (Editing Views)

|类名	|作用	|主要方法
|  ----  |  ----  |  ----  |
|FormView	|显示和处理表单	|form_valid(), form_invalid()
|CreateView	|创建新对象	|form_valid(), get_success_url()
|UpdateView	|更新现有对象	|form_valid(), get_success_url()
|DeleteView	|删除对象	|delete(), get_success_url()
```python
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content', 'author']
    
class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content']
    
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = '/articles/'
```

## Django REST Framework 视图集
* 基础视图类*
*
|类名	|作用	|父类
|  ----  |  ----  |  ----  |
|APIView	|DRF 所有视图的基类	|Django View
|GenericAPIView	|通用 API 视图基类	|APIView
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        return Response({'users': users})
```

* 混合类 (Mixins)

|类名	|作用	|提供的方法
|  ----  |  ----  |  ----  |
|ListModelMixin	|列表操作	|.list(request, *args, **kwargs)
|CreateModelMixin	|创建操作	|.create(request, *args, **kwargs)
|RetrieveModelMixin	|详情操作	|.retrieve(request, *args, **kwargs)
|UpdateModelMixin	|更新操作	|.update(request, *args, **kwargs)
|DestroyModelMixin	|删除操作	|.destroy(request, *args, **kwargs)
```python
from rest_framework import mixins

class ListCreateMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    pass
```
* 通用视图类 (Generic Views)

|类名	|作用	|包含的 Mixins
|  ----  |  ----  |  ----  |
|ListAPIView	|只读列表	|ListModelMixin + GenericAPIView
|CreateAPIView	|只创建	|CreateModelMixin + GenericAPIView
|RetrieveAPIView	|只读详情	|RetrieveModelMixin + GenericAPIView
|UpdateAPIView	|只更新	|UpdateModelMixin + GenericAPIView
|DestroyAPIView	|只删除	|DestroyModelMixin + GenericAPIView
|ListCreateAPIView	|列表 + 创建	|ListModelMixin + CreateModelMixin
|RetrieveUpdateAPIView	|详情 + 更新	|RetrieveModelMixin + UpdateModelMixin
|RetrieveDestroyAPIView	|详情 + 删除	|RetrieveModelMixin + DestroyModelMixin
|RetrieveUpdateDestroyAPIView	|详情 + 更新 + 删除	|Retrieve + Update + Destroy Mixins
```python
from rest_framework import generics

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

* 视图集 (ViewSets)

|类名	|作用	|包含的操作
|  ----  |  ----  |  ----  |
|ViewSet	|基础视图集	|无默认操作
|GenericViewSet	|通用视图集	|无默认操作，使用 mixins
|ReadOnlyModelViewSet	|只读模型视图集	|list(), retrieve()
|ModelViewSet	|完整模型视图集	|list(), create(), retrieve(), update(), partial_update(), destroy()
```python
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```
* 自定义混合视图集

|组合方式	|作用	|包含的操作
|  ----  |  ----  |  ----  |
|ListModelMixin + GenericViewSet	|仅列表	|list()
|CreateModelMixin + GenericViewSet	|仅创建	|create()
|RetrieveModelMixin + GenericViewSet	|仅详情	|retrieve()
|ListModelMixin + CreateModelMixin	|列表 + 创建	|list(), create()
|RetrieveModelMixin + UpdateModelMixin	|详情 + 更新	|retrieve(), update(), partial_update()
|ListModelMixin + RetrieveModelMixin	|列表 + 详情	|list(), retrieve()
```python
from rest_framework import viewsets, mixins

class ListCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass

class RetrieveUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    pass
```

## 完整示例对比
### Django ListView 示例
```python 
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 20
    
    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user
        ).select_related('category')
```
### DRF ReadOnlyModelViewSet 示例
```python 
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    
    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user
        ).select_related('category')
```

## 选择指南
**使用 Django 通用视图的场景：**
* 传统的服务端渲染应用

* 需要返回 HTML 模板

* 简单的 CRUD 操作

* 与 Django 模板系统紧密集成

**使用 DRF 视图集的场景：**
* 构建 RESTful API

* 前后端分离架构

* 需要 JSON/XML 响应

* 复杂的序列化需求

* API 版本控制、认证、限流等高级功能

**性能考虑：**
* Django 视图：适合页面缓存、CDN 缓存

* DRF 视图：适合 API 缓存、数据库查询优化

通过理解这些视图类的特性和适用场景，你可以根据项目需求选择最合适的工具来构建高效、可维护的 Web 应用。