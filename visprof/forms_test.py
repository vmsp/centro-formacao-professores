import datetime

from django import test

from visprof import forms
from visprof import models


def preencher_formulario(
        codigo_postal='3500-218',
        habilitacao_academica=models.Docente.HabilitacaoAcademica.LICENCIATURA,
        outra_habilitacao_academica='',
        situacao_profissional=(
            models.Docente.SituacaoProfissional.CONTRATADO_HABILITACAO_PROPRIA),
        outra_situacao_profissional=''):
    return forms.InscricaoForm(
        initial={'email': 'mail@mail.pt'},
        data={
            'nome_completo': 'Vitor Sousa',
            'morada': 'Rua do Coiso',
            'codigo_postal': codigo_postal,
            'localidade': 'Viseu',
            'telemovel': '123456789',
            'telefone': '123456789',
            'grupo_recrutamento': 1,
            'indice_vencimento': '123',
            'escalao': 1,
            'data_nascimento': datetime.date(2020, 1, 1),
            'id_civil': '12345678',
            'nif': '123456789',
            'id_sighre': '123456789',
            'iban': 'PT5000000000000',
            'habilitacao_academica': habilitacao_academica,
            'outra_habilitacao_academica': outra_habilitacao_academica,
            'escola_vinculado': 1,
            'escola_funcoes': 1,
            'situacao_profissional': situacao_profissional,
            'outra_situacao_profissional': outra_situacao_profissional,
            'nivel_ensino': models.Docente.NivelDeEnsino.CEB_1,
            'anos_servico': 12,
            'dias_servico': 13,
            'proxima_mudanca_escalao': datetime.date(2020, 4, 4),
            'confirmo': True,
        })


class InscricaoFormTest(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        user = models.User.objects.create_user('exemplo@graovasco.pt')
        models.Escola.objects.create(codigo='123456',
                                     nome='AE Grão Vasco',
                                     concelho='Viseu',
                                     distrito='Viseu',
                                     user=user)
        models.GrupoDeRecrutamento.objects.create(codigo='100',
                                                  nome='Educação Pré-Escolar')

    def test_preenchimento_normal(self):
        form = preencher_formulario()
        self.assertEqual(len(form.errors), 0)

    def test_formato_codigo_postal(self):
        form = preencher_formulario(codigo_postal='1233')
        self.assertEqual(form.errors['codigo_postal'],
                         ['O código postal deve seguir o formato XXXX-XXX'])

    def test_outra_habilitacao_academica_preenchida(self):
        form = preencher_formulario(
            habilitacao_academica=models.Docente.HabilitacaoAcademica.OUTRA,
            outra_habilitacao_academica='Habilitação académica XPTO')
        self.assertEqual(len(form.errors), 0)

    def test_outra_habilitacao_academica_por_preencher(self):
        form = preencher_formulario(
            habilitacao_academica=models.Docente.HabilitacaoAcademica.OUTRA,
            outra_habilitacao_academica='')
        self.assertEqual(form.errors['outra_habilitacao_academica'],
                         ['Especifique a "outra" habilitação académica.'])

    def test_outra_situacao_profissional_preenchida(self):
        form = preencher_formulario(
            situacao_profissional=models.Docente.SituacaoProfissional.OUTRA,
            outra_situacao_profissional='Situação profissional XPTO')
        self.assertEqual(len(form.errors), 0)

    def test_outra_situacao_profissional_por_preencher(self):
        form = preencher_formulario(
            situacao_profissional=models.Docente.SituacaoProfissional.OUTRA,
            outra_situacao_profissional='')
        self.assertEqual(form.errors['outra_situacao_profissional'],
                         ['Especifique a "outra" situação profissional.'])
