在Django中，admin.py用于配置Django自带的后台管理系统。以下是一些基础类和属性，用于自定义Admin界面。

1. ModelAdmin类：这是最常用的类，用于定义模型在Admin界面中的展示和行为。

常用属性：

* list_display：指定在列表页面显示的字段。

* list_filter：指定列表页面右侧的过滤器字段。

* search_fields：指定可以搜索的字段。

* ordering：指定默认排序字段。

* readonly_fields：指定只读字段。

* fields 或 fieldsets：控制表单页面的布局。

* exclude：排除表单中的某些字段。

示例：

```python
from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at']
    fieldsets = [
        (None, {'fields': ['name', 'category']}),
        ('详细信息', {'fields': ['price', 'description']}),
    ]
```
1. InlineModelAdmin：用于在同一个页面编辑关联模型（如ForeignKey关联的模型）。有两种主要类型：TabularInline和StackedInline。

TabularInline：以表格形式显示内联模型。

StackedInline：以堆叠形式显示内联模型。

示例：

```python
class MaterialTagInline(admin.TabularInline):
    model = MaterialTag
    extra = 1  # 额外空行数

class MaterialAdmin(admin.ModelAdmin):
    inlines = [MaterialTagInline]
```
admin.site.register：如果不想使用装饰器，可以用这个函数注册模型和对应的ModelAdmin。

示例：

```python
admin.site.register(Material, MaterialAdmin)
```
自定义Action：在Admin列表页面可以执行批量操作。

示例：

```python
class MaterialAdmin(admin.ModelAdmin):
    actions = ['make_expensive']

    def make_expensive(self, request, queryset):
        queryset.update(price=1000)
    make_expensive.short_description = "将所选材料价格设为1000"
```
自定义表单验证：通过重写clean方法或使用自定义表单类。

示例：

```python
from django import forms

class MaterialAdminForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("价格不能为负数")
        return price

class MaterialAdmin(admin.ModelAdmin):
    form = MaterialAdminForm
```
自定义模板：可以通过重写change_list_template、change_form_template等属性来自定义Admin模板。

示例：

```python
class MaterialAdmin(admin.ModelAdmin):
    change_list_template = 'admin/materials_change_list.html'
```
权限控制：可以通过重写has_add_permission、has_change_permission等方法控制权限。

示例：

```python
class MaterialAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser
```
日期层次结构：对于DateField或DateTimeField，可以设置date_hierarchy。

示例：

```python
class MaterialAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
```
列表页每页显示数量：使用list_per_page属性。

示例：

```python
class MaterialAdmin(admin.ModelAdmin):
    list_per_page = 20
```
空值显示：使用empty_value_display属性。

示例：

```python
class MaterialAdmin(admin.ModelAdmin):
    empty_value_display = '（空）'
```
这些是开发admin.py时常用的基础类和属性。通过它们，你可以高度自定义Admin界面的外观和行为。

以下是 Django Admin 开发中常用的基础类和属性，让你能快速上手并自定义强大的后台管理系统：

## 🏗️ 核心基础类
1. ModelAdmin - 最核心的类
```python
from django.contrib import admin
from .models import Material, Category

@admin.register(Material)  # 装饰器注册方式
class MaterialAdmin(admin.ModelAdmin):
    pass

# 或者使用 admin.site.register
admin.site.register(Category)
```
2. InlineModelAdmin - 内联编辑
```python
from django.contrib import admin

# 堆叠内联
class MaterialTagInline(admin.StackedInline):
    model = MaterialTag
    extra = 1  # 默认显示的空行数

# 表格内联（更紧凑）
class MaterialTagTabularInline(admin.TabularInline):
    model = MaterialTag
    extra = 1
```
## 📊 显示控制属性
1. 列表页显示控制
```python
class MaterialAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ['id', 'name', 'category', 'price', 'created_at', 'is_available']
    
    # 可点击的字段（链接到编辑页）
    list_display_links = ['name', 'id']
    
    # 可编辑的字段（直接在列表页修改）
    list_editable = ['price', 'is_available']
    
    # 每页显示数量
    list_per_page = 50
    
    # 最大显示数量（带显示全部链接）
    list_max_show_all = 200
```
2. 筛选和搜索
```python
class MaterialAdmin(admin.ModelAdmin):
    # 右侧筛选器
    list_filter = [
        'category',           # 直接使用字段
        'created_at',         # 日期字段会自动提供日期筛选
        'is_available',       # 布尔字段
        ('price', admin.RangeFilter)  # 范围筛选
    ]
    
    # 搜索字段
    search_fields = [
        'name',               # 简单搜索
        'name__icontains',    # 包含搜索（不区分大小写）
        'description__icontains',
        'category__name'      # 关联字段搜索
    ]
    
    # 搜索提示
    search_help_text = "可以根据名称、描述或分类搜索"
```

3. 详细页面布局
```python
class MaterialAdmin(admin.ModelAdmin):
    # 字段分组显示
    fieldsets = [
        ('基本信息', {
            'fields': ['name', 'category', 'price'],
            'description': '材料的基本信息'
        }),
        ('详细描述', {
            'fields': ['description', 'specifications'],
            'classes': ['collapse'],  # 可折叠
        }),
        ('状态信息', {
            'fields': ['is_available', 'created_at', 'updated_at'],
            'classes': ['wide'],
        })
    ]
    
    # 或者简单字段列表
    fields = ['name', 'category', 'price', 'description']
    
    # 只读字段
    readonly_fields = ['created_at', 'updated_at']
```
## 🔧 功能增强属性
1. 关联对象处理
```python
class MaterialAdmin(admin.ModelAdmin):
    # 在材料编辑页内联显示标签
    inlines = [MaterialTagInline]
    
    # 原始ID显示（用于调试）
    raw_id_fields = ['category']  # 对于ForeignKey字段
    
    # 自动完成字段
    autocomplete_fields = ['category']
    
    # 过滤器水平显示（用于多对多字段）
    filter_horizontal = ['tags']
    
    # 或者垂直显示
    filter_vertical = ['tags']
```
2. 日期相关配置
```python
class MaterialAdmin(admin.ModelAdmin):
    # 日期层次导航
    date_hierarchy = 'created_at'
    
    # 保存时自动处理日期
    def save_model(self, request, obj, form, change):
        if not change:  # 新建对象
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
```
## 🎨 自定义显示方法
1. 自定义列表列
```python
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'price_with_tax', 'availability_status']
    
    def price_with_tax(self, obj):
        """计算含税价格"""
        return f"¥{obj.price * 1.13:.2f}"
    price_with_tax.short_description = '含税价格'  # 列标题
    price_with_tax.admin_order_field = 'price'    # 允许排序
    
    def availability_status(self, obj):
        """库存状态显示"""
        if obj.is_available:
            return '✅ 有货'
        return '❌ 缺货'
    availability_status.short_description = '库存状态'
```
2. 自定义筛选器
```python
# 自定义筛选器
class PriceRangeFilter(admin.SimpleListFilter):
    title = '价格范围'  # 筛选器标题
    parameter_name = 'price_range'  # URL参数名
    
    def lookups(self, request, model_admin):
        """定义筛选选项"""
        return [
            ('0-100', '0-100元'),
            ('100-500', '100-500元'),
            ('500-1000', '500-1000元'),
            ('1000+', '1000元以上'),
        ]
    
    def queryset(self, request, queryset):
        """应用筛选逻辑"""
        if self.value() == '0-100':
            return queryset.filter(price__range=(0, 100))
        elif self.value() == '100-500':
            return queryset.filter(price__range=(100, 500))
        # ... 其他范围

class MaterialAdmin(admin.ModelAdmin):
    list_filter = [PriceRangeFilter, 'category', 'is_available']
```
## ⚡ 性能优化属性
1. 查询优化
```python
class MaterialAdmin(admin.ModelAdmin):
    # 选择关联字段时优化查询
    autocomplete_fields = ['category']
    
    # 在列表页优化关联字段查询
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
    
    # 在列表页优化多对多字段查询
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
```
2. 批量操作
```python
class MaterialAdmin(admin.ModelAdmin):
    # 自定义Admin Action
    actions = ['make_available', 'make_unavailable']
    
    def make_available(self, request, queryset):
        """批量设置为有货"""
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated}个材料已设置为有货')
    make_available.short_description = "设置为有货"
    
    def make_unavailable(self, request, queryset):
        """批量设置为缺货"""
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated}个材料已设置为缺货')
    make_unavailable.short_description = "设置为缺货"
```
## 🔒 权限控制
1. 基础权限控制
```python
class MaterialAdmin(admin.ModelAdmin):
    # 根据用户权限控制显示
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['price', 'category']  # 非管理员只读
        return []
    
    # 控制可编辑字段
    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['name', 'category', 'price', 'description', 'is_available']
        return ['name', 'description']
    
    # 控制查询集
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_available=True)
```
## 🎯 完整示例
```python
from django.contrib import admin
from .models import Material, Category, MaterialTag

class MaterialTagInline(admin.TabularInline):
    model = MaterialTag
    extra = 1

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    # 显示控制
    list_display = ['id', 'name', 'category', 'price_with_tax', 'availability_status', 'created_at']
    list_display_links = ['id', 'name']
    list_editable = ['price']
    list_per_page = 25
    
    # 筛选搜索
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name__icontains', 'description__icontains']
    
    # 详细页面
    fieldsets = [
        ('基本信息', {'fields': ['name', 'category', 'price']}),
        ('详细内容', {'fields': ['description', 'specifications'], 'classes': ['collapse']}),
        ('状态', {'fields': ['is_available']}),
    ]
    inlines = [MaterialTagInline]
    readonly_fields = ['created_at', 'updated_at']
    
    # 自定义方法
    def price_with_tax(self, obj):
        return f"¥{obj.price * 1.13:.2f}"
    price_with_tax.short_description = '含税价'
    
    def availability_status(self, obj):
        return '✅ 有货' if obj.is_available else '❌ 缺货'
    availability_status.short_description = '状态'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'material_count']
    search_fields = ['name']
    
    def material_count(self, obj):
        return obj.material_set.count()
    material_count.short_description = '材料数量'
```