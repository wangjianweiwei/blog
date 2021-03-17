## django-admin 下拉框选项过滤(外键字段过滤)

```python
from django.contrib import admin


class BlogArticleAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sort_id":
            kwargs["queryset"] = Tags.objects.filter(user=request.user)
        return super(BlogArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
```

## django-admin 自定义action

```python
from django.contrib import admin


class TestAdmin(admin.ModelAdmin):
    def test_action(self, request, queryset):
        queryset.update(status=False)

    test_action.short_description = "自定义action"

    actions = [test_action]
    list_display = ('id', 'user', 'create_at', 'status')
```

## Django model自定义字段

平常可能用的多的就是json字段了

```python
from django.db.models import TextField
import json


class JsonField(TextField):
    description = "python json 映射 mysql text"

    @staticmethod
    def to_python(value):
        """
        往数据库中存储时会调用这个方法, 数据库中存储的正是该方法的返回值
        """
        return json.dumps(value, ensure_ascii=False)

    @staticmethod
    def from_db_value(value, expression, connection):
        """
        当字段不内置字段时, 会调用get_db_converters获取对应的转换方法, 该方法的返回值就对作为ORM对象对应字段的属性值
        >>>    def get_db_converters(self, connection):
        >>>         if hasattr(self, 'from_db_value'):
        >>>             return [self.from_db_value]
        >>>         return []
        """
        return json.loads(value)
```

## 文件下载时使用中文名称会乱码

```python
from django.view import View
from django.utils.encoding import escape_uri_path
from django.http.response import FileResponse


class TestView(View):

    def post(self, request):
        path = ""
        name = "诺贝尔获奖名单.xlsx"
        return FileResponse(open(path, "rb"), as_attachment=True, filename=escape_uri_path(name))
```
