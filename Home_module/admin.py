from django.contrib import admin
from .models import FooterLink, FooterBox, SiteSetting, MainBanner, Slides, FooterLinkValue, SuggestedProductSection


# Register your models here.

class FooterBoxAdmin(admin.ModelAdmin):
    pass


class FooterLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(FooterBox)
admin.site.register(FooterLink)
admin.site.register(FooterLinkValue)
admin.site.register(SiteSetting)
admin.site.register(MainBanner)
admin.site.register(Slides)
admin.site.register(SuggestedProductSection)
