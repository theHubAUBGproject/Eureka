from django.contrib import admin
from django.contrib.auth.models import Permission

from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (POS, Dimension, Family, Feature, Genus, Language, Lemma,
                     TagSet, Word, User, Proposal, Notification)

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'is_linguist'
                  
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# Register your models here.
admin.site.register(Word)
admin.site.register(Feature)
admin.site.register(Dimension)
admin.site.register(Language)
admin.site.register(Lemma)
admin.site.register(Family)
admin.site.register(TagSet)
admin.site.register(POS)
admin.site.register(Genus)
admin.site.register(User, UserAdmin)
admin.site.register(Proposal)
admin.site.register(Notification)
