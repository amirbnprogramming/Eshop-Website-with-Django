from django.contrib import admin

from . import models


# Register your models here.


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_url', 'is_main_setting']
    list_editable = ['is_main_setting']


class FooterLinkBoxAdmin(admin.ModelAdmin):
    list_display = ['title']


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'footer_link_box']
    list_editable = ['footer_link_box']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'url_title', 'is_active']
    list_editable = ['url', 'is_active']


class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_active', 'position']
    list_editable = ['is_active', 'position']


admin.site.register(models.SiteSetting, SiteSettingAdmin)
admin.site.register(models.FooterLinkBox, FooterLinkBoxAdmin)
admin.site.register(models.FooterLink, FooterLinkAdmin)
admin.site.register(models.Slider, SliderAdmin)
admin.site.register(models.SiteBanner, SiteBannerAdmin)
