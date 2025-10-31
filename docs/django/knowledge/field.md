### Django模型中常见的字段类型
* **CharField**

用于存储较短的字符串（如标题、名称等）

必须指定max_length参数，表示最大字符数

对应数据库中的VARCHAR列

* **TextField**

用于存储大段文本，如文章内容、描述等

不需要指定最大长度，适合存储任意长度的文本

对应数据库中的TEXT列

* **SlugField**

用于存储URL友好的标识符（通常由字母、数字、下划线和连字符组成）

通常用于生成URL的一部分

可以设置max_length，也可以使用prepopulated_fields从其他字段自动生成

* **IntegerField**

用于存储整数

可以设置取值范围（通过validators）

* **FloatField**

用于存储浮点数

* **BooleanField**

存储布尔值（True/False）

* **DateTimeField**

存储日期和时间

常用参数：

auto_now_add：当对象第一次创建时自动设置为当前时间

auto_now：每次保存对象时自动更新为当前时间

* **DateField**

存储日期（不含时间）

* **EmailField**

存储电子邮件地址，实际上是CharField，但带有电子邮件验证

* **URLField**

存储URL，实际上是CharField，但带有URL验证

* **FileField**

用于上传文件

需要指定upload_to参数，表示文件保存的路径

* **ImageField**

用于上传图片，是FileField的子类，增加了图片尺寸验证等功能

需要Pillow库支持

* **ForeignKey**

用于定义多对一关系，例如一篇文章属于一个作者，一个作者可以有多篇文章

需要指定关联的模型和on_delete参数（当被关联的对象删除时的行为）

* **ManyToManyField**

用于定义多对多关系，例如一篇文章可以有多个标签，一个标签也可以被多篇文章使用

* **OneToOneField**

用于定义一对一关系，例如一个用户对应一个个人资料

* **DecimalField**

用于存储固定精度的十进制数，适用于货币金额等

必须指定max_digits（总位数）和decimal_places（小数位数）

* **BinaryField**

用于存储原始二进制数据（如图片、文件等），但不常用，通常更推荐使用FileField

* **UUIDField**

用于存储全局唯一标识符（UUID），通常作为主键使用

* **DurationField**

用于存储时间间隔

* **GenericIPAddressField**

用于存储IPv4或IPv6地址
