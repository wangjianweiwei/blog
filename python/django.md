## django-admin 下拉框选项过滤(外键字段过滤)
```python
from django.contrib import admin

class BlogArticleAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sort_id":
            kwargs["queryset"] = Tags.objects.filter(user=request.user)
        return super(BlogArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
```
