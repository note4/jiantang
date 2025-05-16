

## 检查版本或是否安装 python

```bash
python --version

```

```bash
pip --version
# 升级pip
## windows
pip install --upgrade pip
## macOS
# ???

```

## WIndows 11 安装 python


## macOS 安装 python


## 已安装 python

### 设置环境

```bash

# 设置环境 env_jiantang名称可替换
python -m venv env_jiantang


# 激活环境env_jiantang名称可替换，和前面保持一致
## WIndows
env_jiantang\Scripts\activate
## macOS
source env_jiantang/bin/activate

```

### 安装 django

```bash
# 安装 django

# 检测当前环境下已安装django
pip list
## macOS 查询
pip3 list

## WIndows 安装
pip install Django
## macOS 安装，有pip可以直接用pip没有就用pip3
pip3 install Django
## 使用 大陆镜像
pip3 install django -i https://mirrors.ustc.edu.cn/pypi/web/simple



# 方案一
# 当前目录创建一个 django-admin 项目 路径名称（jiantang）可替换
django-admin startproject jiantang .

# 方案二
# 新目录
django-admin startproject jiantang
cd jiantang

# 创建应用，应用名称（jtapp）不要和项目名称一样
python manage.py startapp jtapp


```

运行环境

```bash
# 运行开发服务器，运行成功通过 http://127.0.0.1:8000/ 访问
python manage.py runserver
# 如果迁移系统需要重新安装 django 和 django-admin

```


## 补充相关文件


## 数据迁移和创建后台管理员账号

```bash
# 数据迁移

python manage.py migrate

# 创建管理员（后台）
python manage.py createsuperuser

```
