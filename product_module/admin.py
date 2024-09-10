from django.contrib import admin

from product_module.models import Product, Category, ProductTags, Brand, ProductVisit, ProductGallery


# Register your models here.
class BrandsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']


class ProductAdmin(admin.ModelAdmin):
    # list_display_links = ['title']
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_deleted']
    list_editable = ['price', 'is_active']

    readonly_fields = ['slug']
    # prepopulated_fields = {'slug': ['title']}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title']


class TagsAdmin(admin.ModelAdmin):
    list_display = ['caption', 'product']


class ProductVisitAdmin(admin.ModelAdmin):
    list_display = ['product', 'ip', 'user']


class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVisit, ProductVisitAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductTags, TagsAdmin)
admin.site.register(Brand, BrandsAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
