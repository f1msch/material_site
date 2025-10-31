### 配置
```bash
$ django-admin startproject myblog
$ cd myblog
$ python manage.py startapp blog
```
### 启动
`python manage.py runserver`

http://127.0.0.1:8000/blog/

### Django数据库操作
#### 创建迁移文件（当模型改变时）
python manage.py makemigrations

#### 应用迁移到数据库
python manage.py migrate

#### 检查是否有未应用的迁移
python manage.py showmigrations

#### 查看SQL语句（不实际执行）
python manage.py sqlmigrate myapp 0001

#### 重置数据库（开发时使用）
python manage.py flush

#### 导出数据
python manage.py dumpdata > data.json

#### 导入数据
python manage.py loaddata data.json