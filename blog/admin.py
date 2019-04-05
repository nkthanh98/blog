from django.contrib import admin
from django.utils.html import mark_safe, format_html
from . import models



class CategoryAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'title', 'description', 'image',)
    readonly_fields = ('image_tag',)


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'author', 'image_tag', 'image', 'category',
              'n_views', 'tags')
    readonly_fields = ('image_tag', 'n_views', 'author', )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'image', 'description',)
    readonly_fields = ('image_tag',)


# Register your models here.
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Subscriber)

