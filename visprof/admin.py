from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.utils import html

from visprof import core
from visprof import models


class AdminSite(admin.AdminSite):
    site_header = 'Administração do VisProf'
    site_title = 'Administração do VisProf'
    index_title = 'Administração do VisProf'


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        fields = ('email',)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Permissões', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
            )
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2'),
    }),)
    add_form = UserCreationForm
    list_display = ('email', 'nome_completo', 'is_staff')
    search_fields = ('email', 'nome_completo')
    ordering = ('email',)


class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('accao', 'docente_link', 'estado')
    search_fields = ('accao__designacao', 'docente__nome_completo')
    ordering = ('timestamp',)

    def docente_link(self, inscricao):
        docente = inscricao.docente
        url = core.reverse('admin:visprof_docente_change', args=[docente.pk])
        return html.format_html(f'<a href={url}>{docente.nome_completo}</a>')

    docente_link.short_description = 'Docente'


admin_site = AdminSite()

admin_site.register(models.User, UserAdmin)
admin_site.register(models.Accao)
admin_site.register(models.Escola)
admin_site.register(models.GrupoDeRecrutamento)
admin_site.register(models.Docente)
admin_site.register(models.Inscricao, InscricaoAdmin)
