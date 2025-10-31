## 🏗️ ModelForm 的分类和用途
1. 基础 ModelForm
```python
from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'category', 'price', 'description']
```
2. 带自定义验证的 ModelForm
```python
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'  # 包含所有字段
    
    # 字段级验证
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError("名称至少需要2个字符")
        return name
    
    # 表单级验证（多个字段关系）
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        category = cleaned_data.get('category')
        
        if price and price > 1000 and category == 'cheap':
            raise forms.ValidationError("廉价分类的商品价格不能超过1000")
        
        return cleaned_data
```
3. 自定义字段显示的 ModelForm
```python
class MaterialForm(forms.ModelForm):
    # 重写字段属性
    name = forms.CharField(
        label='材料名称',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入材料名称'
        }),
        help_text='请输入材料的完整名称'
    )
    
    category = forms.ChoiceField(
        choices=[
            ('metal', '金属'),
            ('plastic', '塑料'), 
            ('wood', '木材')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Material
        fields = ['name', 'category', 'price', 'in_stock']
```
4. 排除特定字段的 ModelForm
```python
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude = ['created_at', 'updated_at']  # 排除这些字段
```
5. 部分字段只读的 ModelForm
```python
class MaterialEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置某些字段为只读
        self.fields['sku'].widget.attrs['readonly'] = True
        self.fields['created_by'].disabled = True
    
    class Meta:
        model = Material
        fields = ['sku', 'name', 'category', 'created_by']
```
## 🎯 常用的 forms.Field 类型
### 基础字段类型：
```python
class MaterialForm(forms.Form):
    name = forms.CharField(max_length=100)                    # 文本输入
    description = forms.CharField(widget=forms.Textarea)     # 文本区域
    price = forms.DecimalField(max_digits=10, decimal_places=2)  # 数字
    in_stock = forms.BooleanField(required=False)            # 复选框
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)   # 下拉选择
    tags = forms.MultipleChoiceField(choices=TAG_CHOICES)    # 多选
    image = forms.ImageField()                               # 文件上传
    created_at = forms.DateField(widget=forms.SelectDateWidget)  # 日期选择
```
## 🔧 在视图中的使用
1. 创建数据
```python
from django.shortcuts import render, redirect
from .forms import MaterialForm

def create_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)  # 处理文件上传
        if form.is_valid():
            material = form.save()  # 自动保存到数据库
            return redirect('material_detail', pk=material.pk)
    else:
        form = MaterialForm()
    
    return render(request, 'materials/create.html', {'form': form})
```
2. 更新数据
```python
def update_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('material_detail', pk=material.pk)
    else:
        form = MaterialForm(instance=material)
    
    return render(request, 'materials/update.html', {'form': form})
```
## 🎨 在模板中的渲染
### 基本渲染：
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    <!-- 自动渲染所有字段 -->
    {{ form.as_p }}
    
    <!-- 或者手动渲染每个字段 -->
    <div class="form-group">
        {{ form.name.label_tag }}
        {{ form.name }}
        {{ form.name.errors }}
    </div>
    
    <button type="submit">保存</button>
</form>
```
## 📊 ModelForm 配置选项
### Meta 类常用选项：
```python
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'                    # 所有字段
        # fields = ['name', 'category']       # 指定字段
        # exclude = ['created_at']            # 排除字段
        labels = {                            # 自定义标签
            'name': '材料名称',
            'price': '价格'
        }
        help_texts = {                        # 帮助文本
            'name': '请输入完整的材料名称'
        }
        error_messages = {                    # 错误消息
            'name': {
                'required': '名称是必填字段',
                'max_length': '名称太长'
            }
        }
        widgets = {                           # 自定义控件
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }
```