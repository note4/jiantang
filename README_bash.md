```bash
python --version

pip --version

# env_jiantang名称可替换
python -m venv env_jiantang


# env_jiantang名称可替换，和前面保持一致
env_jiantang\Scripts\activate

# 安装 django
pip install Django

# 检测当前环境下已安装django
pip list

# 方案一
# 当前目录创建一个 django-admin 项目 路径名称（jiantang）可替换
django-admin startproject jiantang .

# 方案二
# 新目录
django-admin startproject jiantang
cd jiantang

# 创建应用，应用名称（jtapp）不要和项目名称一样
python manage.py startapp jtapp

# 运行开发服务器，运行成功通过 http://127.0.0.1:8000/ 访问
python manage.py runserver



```


## 补充相关文件


## 运行

```bash
# 数据迁移

python manage.py migrate

# 创建管理员（后台）
python manage.py createsuperuser

```


## pip

