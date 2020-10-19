from django.conf import settings
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.core import mail
from django.utils import timezone
from sesame import utils as sesame

from visprof import core
from visprof import forms
from visprof import models
from visprof import tables


class LoginView(auth_views.LoginView):

    def get(self, request, *args, **kwargs):
        request.session['next'] = request.GET.get('next')
        return super().get(request, *args, **kwargs)


def handle_authorize(request, remote, token, user_info):
    user = auth.authenticate(request,
                             email=user_info['email'],
                             access_token=token['access_token'])
    if user is None:
        return core.HttpResponse(status=401)
    auth.login(request, user)
    return core.redirect(request.session.pop('next', 'index'))


def lista_accoes(request):
    if request.user.has_perm('visprof.change_accao'):
        accoes = models.Accao.objects.all()
    else:
        accoes = models.Accao.objects.filter(
            estado__in=(models.Accao.Estado.PRE_INSCRICAO,
                        models.Accao.Estado.INSCRICAO,
                        models.Accao.Estado.TERMINADA))
    table = tables.AccoesTable(accoes, order_by='-estado')
    tables.RequestConfig(request, paginate={'per_page': 50}).configure(table)
    return core.render(request, 'visprof/lista_accoes.html', {'table': table})


def detalhe_accao(request, accao_id):
    accao = models.Accao.objects.get(pk=accao_id)
    inscricao = models.Inscricao.objects.filter(
        accao=accao, docente__user_id=request.user.id).first()
    return core.render(request, 'visprof/detalhe_accao.html', {
        'accao': accao,
        'agora': timezone.now(),
        'inscricao': inscricao,
    })


@core.permission_required(('visprof.add_accao', 'visprof.change_accao'))
def editar_accao(request,
                 accao_id=None,
                 template_name='visprof/editar_accao.html'):
    accao = (core.get_object_or_404(models.Accao, pk=accao_id)
             if accao_id else None)
    if (accao is not None and
            accao.estado not in (models.Accao.Estado.RASCUNHO,
                                 models.Accao.Estado.PRE_INSCRICAO)):
        raise core.Http404()
    form = forms.AccaoForm(request.POST if request.method == 'POST' else None,
                           instance=accao)
    if request.method == 'POST' and form.is_valid():
        accao = form.save(commit=False)
        if request.POST['submit'] == 'Publicar':
            messages.success(request, 'Acção publicada com sucesso.')
            accao.publicar()
            return core.redirect(accao)
        # TODO(vitor): Só permitir depois dos dados todos inseridos.
        accao.save()
        return core.redirect('editar_accao', accao_id=accao.pk)
    return core.render(request, template_name, {'accao': accao, 'form': form})


@core.login_required
def pre_inscricao(request, accao_id):
    accao = core.get_object_or_404(models.Accao,
                                   pk=accao_id,
                                   estado=models.Accao.Estado.PRE_INSCRICAO,
                                   fecho_pre_inscricao__gt=timezone.now())
    docente, _ = models.Docente.objects.get_or_create(
        user_id=request.user.pk, defaults={'user': request.user})
    if models.Inscricao.objects.filter(accao=accao, docente=docente).exists():
        return core.redirect(accao)
    form = forms.PreInscricaoForm(
        request.POST if request.method == 'POST' else None,
        instance=docente,
        initial={'email': request.user.email})
    if request.method == 'POST' and form.is_valid():
        docente = form.save(commit=False)
        accao.pre_inscrever(docente)
        messages.success(request, 'Registado na acção de formação com sucesso!')
        return core.redirect(accao)
    return core.render(request, 'visprof/pre_inscricao.html', {
        'accao': accao,
        'form': form,
    })


@core.permission_required('visprof.change_inscricao')
def lista_pre_inscricoes(request, accao_id):
    accao = core.get_object_or_404(models.Accao,
                                   pk=accao_id,
                                   estado=models.Accao.Estado.PRE_INSCRICAO)
    inscricoes = models.Inscricao.objects.filter(accao=accao)
    table = tables.PreInscricaoTable(inscricoes)
    tables.RequestConfig(request, paginate={'per_page': 100}).configure(table)
    form = forms.EnviarInscricoesForm(
        (request.POST if request.method == 'POST' else None))
    if request.method == 'POST' and form.is_valid():
        inscricoes_seleccionadas = inscricoes.filter(
            estado=models.Inscricao.Estado.SELECCIONADA)
        accao.expiracao_inscricoes = request.POST['expiracao']
        accao.estado = models.Accao.Estado.INSCRICAO
        accao.save()
        mails = []
        for inscricao in inscricoes_seleccionadas:
            url = request.build_absolute_uri(
                core.reverse(submeter_inscricao, args=[inscricao.pk]))
            conteudo = core.render_to_string('visprof/mail_seleccionado.txt', {
                'accao': accao,
                'docente': inscricao.docente,
                'url': url,
            })
            mails.append(
                (f'Inscrição "{accao.designacao}"', conteudo,
                 settings.DEFAULT_FROM_EMAIL, [inscricao.docente.email]))
        mail.send_mass_mail(mails)
        return core.redirect(accao)
    total_seleccionadas = models.Inscricao.objects.filter(
        accao=accao, estado=models.Inscricao.Estado.SELECCIONADA).count()
    return core.render(
        request, 'visprof/lista_pre_inscricoes.html', {
            'accao': accao,
            'table': table,
            'form': form,
            'total_seleccionadas': total_seleccionadas,
        })


@core.permission_required('visprof.change_inscricao')
def alterar_seleccionado(request, inscricao_id):
    estado = (models.Inscricao.Estado.SELECCIONADA
              if request.POST.get('seleccionada') == 'true' else
              models.Inscricao.Estado.NAO_SELECCIONADA)
    inscricao = models.Inscricao.objects.get(pk=inscricao_id)
    inscricao.estado = estado
    inscricao.save()
    total_seleccionadas = models.Inscricao.objects.filter(
        accao=inscricao.accao,
        estado=models.Inscricao.Estado.SELECCIONADA).count()
    return core.JsonResponse({'total_seleccionadas': total_seleccionadas})


@core.login_required
def submeter_inscricao(request, inscricao_id):
    inscricao = models.Inscricao.objects.select_related(
        'accao', 'docente', 'docente__user').get(pk=inscricao_id)
    # TODO(vitor): Testar esta lógica.
    if timezone.now() >= inscricao.accao.expiracao_inscricoes:
        raise core.Http404()
    if (not inscricao.estado in (models.Inscricao.Estado.SELECCIONADA,
                                 models.Inscricao.Estado.PREENCHIDA) or
            request.user != inscricao.docente.user):
        raise core.Http404()
    form = forms.InscricaoForm(
        request.POST if request.method == 'POST' else None,
        instance=inscricao.docente,
        initial={'email': request.user.email})
    if request.method == 'POST' and form.is_valid():
        with core.transaction.atomic():
            inscricao.docente.save()
            inscricao.estado = models.Inscricao.Estado.PREENCHIDA
            inscricao.save()
        messages.success(request, 'Inscrição submetida com sucesso.')
        return core.redirect(inscricao.accao)
    return core.render(request, 'visprof/submeter_inscricao.html', {
        'accao': inscricao.accao,
        'form': form
    })


@core.permission_required('visprof.change_inscricao')
def lista_inscricoes(request, accao_id):
    """Lista de inscrições seleccionadas.

    Mostra inscrições por preencher, preenchidas e confirmadas. Um POST envia
    links para as escolas a pedir a confirmação dos dados inseridos pelos
    docentes.
    """
    accao = core.get_object_or_404(models.Accao,
                                   pk=accao_id,
                                   estado=models.Accao.Estado.INSCRICAO)
    inscricoes = models.Inscricao.objects.select_related(
        'docente', 'docente__user').filter(
            accao=accao,
            estado__in=(models.Inscricao.Estado.SELECCIONADA,
                        models.Inscricao.Estado.PREENCHIDA,
                        models.Inscricao.Estado.CONFIRMADA))
    table = tables.InscricoesTable(inscricoes)
    tables.RequestConfig(request, paginate={'per_page': 100}).configure(table)
    if request.method == 'POST':
        escola_ids = inscricoes.values('docente__escola_vinculado').distinct()
        escolas = models.Escola.objects.filter(pk__in=escola_ids)
        mails = []
        for escola in escolas:
            # Este link inclui um parâmetro especial que faz automaticamente
            # login com o utilizador da escola.
            url = (request.build_absolute_uri(
                core.reverse(lista_confirmar_inscricoes, args=[accao_id])) +
                   sesame.get_query_string(escola.user))
            mails.append(
                (f'Confirmar dados de inscrição para {accao.designacao}',
                 core.render_to_string(
                     'visprof/mail_confirmar.txt', {
                         'accao': accao,
                         'escola': escola,
                         'url': url,
                         'is_agrupamento': escola.nome[0] == 'A',
                     }), settings.DEFAULT_FROM_EMAIL, [escola.user.email]))
        mail.send_mass_mail(mails)
        accao.emails_confirmacao_enviados += 1
        accao.save()
        messages.success(request, 'Emails de confirmação enviados')
    return core.render(request, 'visprof/lista_inscricoes.html', {
        'accao': accao,
        'table': table
    })


def lista_confirmar_inscricoes(request, accao_id):
    user = sesame.get_user(request, update_last_login=True)
    if user is None:
        raise core.Http404()
    accao = models.Accao.objects.get(id=accao_id)
    inscricoes = models.Inscricao.objects.filter(
        accao_id=accao_id, docente__escola_vinculado=user.escola)
    table = tables.ConfirmarInscricoesTable(inscricoes, order_by='-estado')
    tables.RequestConfig(request).configure(table)
    return core.render(request, 'visprof/lista_confirmar_inscricoes.html', {
        'accao': accao,
        'table': table
    })


def confirmar_inscricao(request, inscricao_id):
    user = sesame.get_user(request, update_last_login=True)
    if user is None:
        raise core.Http404()
    inscricao = core.get_object_or_404(
        models.Inscricao,
        pk=inscricao_id,
        estado__in=(models.Inscricao.Estado.PREENCHIDA,
                    models.Inscricao.Estado.CONFIRMADA))
    if user.pk != inscricao.docente.escola_vinculado.user.pk:
        raise core.Http404()
    docente = inscricao.docente
    form = forms.InscricaoForm(read_only=True,
                               instance=docente,
                               initial={'email': docente.email})
    if request.method == 'POST':
        inscricao.estado = models.Inscricao.Estado.CONFIRMADA
        inscricao.save()
        messages.success(
            request,
            f'Informação do docente {docente.nome_completo} confirmada.')
        return core.redirect(
            core.reverse('lista_confirmar_inscricoes',
                         args=[inscricao.accao.pk]) + '?sesame=' +
            request.GET['sesame'])
    return core.render(request, 'visprof/confirmar_inscricao.html', {
        'inscricao': inscricao,
        'docente': docente,
        'form': form
    })
