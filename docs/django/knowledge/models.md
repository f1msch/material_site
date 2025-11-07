Django models 模块详解
📋 Model 相似的类及作用
Django 的 models 模块提供了多种类来定义数据库结构和字段类型：

1. 核心模型类
类名	作用	示例
Model	所有模型的基类	class User(models.Model):
Manager	模型的数据库查询管理器	objects = models.Manager()
QuerySet	表示数据库查询的结果集	User.objects.filter(is_active=True)
2. 字段类型类
类别	类名	作用
字符相关	CharField, TextField, SlugField, EmailField, URLField	存储文本数据
数值相关	IntegerField, BigIntegerField, FloatField, DecimalField, AutoField	存储数值数据
日期时间	DateField, DateTimeField, TimeField, DurationField	存储时间数据
布尔相关	BooleanField, NullBooleanField	存储布尔值
文件相关	FileField, ImageField, FilePathField	处理文件上传
关系相关	ForeignKey, OneToOneField, ManyToManyField	处理模型关系
3. 元数据相关类
类名	作用
Options	模型的元数据配置（对应 class Meta）
BaseConstraint	数据库约束的基类
UniqueConstraint	唯一约束
CheckConstraint	检查约束
Index	数据库索引
4. 查询相关类
类名	作用
Q	构建复杂查询条件
F	引用模型字段值
Expression	查询表达式的基类
Case, When	条件表达式
Value	字面值表达式
