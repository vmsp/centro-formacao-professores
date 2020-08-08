import loginpass
from django import urls
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import base as generic_views

from visprof import oauth, views

urlpatterns = [
    urls.path('gestão/', admin.site.urls),
    # Acção
    urls.path('',
              generic_views.RedirectView.as_view(pattern_name='lista_accoes',
                                                 permanent=True),
              name='index'),
    urls.path('accoes/', views.lista_accoes, name='lista_accoes'),
    urls.path('accoes/<int:accao_id>/',
              views.detalhe_accao,
              name='detalhe_accao'),
    urls.path('accoes/nova/', views.editar_accao, name='editar_accao'),
    urls.path('accoes/<int:accao_id>/editar/',
              views.editar_accao,
              name='editar_accao'),
    urls.path('accoes/<int:accao_id>/pre-inscricoes/',
              views.lista_pre_inscricoes,
              name='lista_pre_inscricoes'),
    urls.path('accoes/<int:accao_id>/pre-inscricoes/nova/',
              views.pre_inscricao,
              name='nova_pre_inscricao'),
    urls.path('alterar_seleccionado/<int:inscricao_id>/',
              views.alterar_seleccionado,
              name='alterar_seleccionado'),
    urls.path('accoes/<int:accao_id>/inscricoes/',
              views.lista_inscricoes,
              name='lista_inscricoes'),
    urls.path('inscricoes/<int:inscricao_id>/',
              views.submeter_inscricao,
              name='submeter_inscricao'),
    # Confirmação
    urls.path('accao/<int:accao_id>/confirmar-inscricoes/',
              views.lista_confirmar_inscricoes,
              name='lista_confirmar_inscricoes'),
    urls.path('inscricoes/<int:inscricao_id>/confirmar/',
              views.confirmar_inscricao,
              name='confirmar_inscricao'),
    # Autenticação
    urls.path('accounts/login/', views.LoginView.as_view(), name='login'),
    urls.path('accounts/logout/',
              auth_views.LogoutView.as_view(next_page='lista_accoes'),
              name='logout'),
]

for backend in oauth.BACKENDS:
    oauth_urls = loginpass.create_django_urlpatterns(backend, oauth.OAUTH,
                                                     views.handle_authorize)
    urlpatterns.append(
        urls.path('accounts/' + backend.NAME + '/', urls.include(oauth_urls)))
