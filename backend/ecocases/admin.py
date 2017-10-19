from django.contrib import admin
from .models import EcoCase, ESM, Vote
from django.forms import TextInput, Textarea
from django.db import models
from .forms import EcoCaseForm
# Register your models here.


class ESMInline(admin.TabularInline):
    model = ESM
    extra = 0


class EcoCaseAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    #     models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 40})},
    # }
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Ecocase characters', {'fields': [
         'promise', 'usage', 'organization', 'economic_transaction']}),
        ('Ecocase evaluation', {'fields': ['reference', 'direct_environmental_gain', 'indirect_environmental_gain',
                                           'attractiveness_price', 'proven_cas_or_project']}),
        ('Ecocase images', {'fields': [
         'image_urls', 'images']}),
        ('Date information', {'fields': ['timestamp']})
    ]

    inlines = [ESMInline]
    list_display = ['title', 'timestamp']
    list_filter = ['timestamp']


admin.site.register(EcoCase, EcoCaseAdmin)
admin.site.register(ESM)
admin.site.register(Vote)
