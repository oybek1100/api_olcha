from django.contrib import admin
from .models import Category , SubCategory , Product , Comment, Attribute , AttributeKey , AttributeValue , CustomUser
from django.contrib.auth.models import Group


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.unregister(Group)
admin.site.register(AttributeKey)
admin.site.register(AttributeValue)
admin.site.register(Attribute)
admin.site.register(CustomUser)


