from crispy_forms.helper import FormHelper
from crispy_forms.helper import Layout
from crispy_forms.layout import Button
from crispy_forms.layout import Column
from crispy_forms.layout import Div
from crispy_forms.layout import Field
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Row
from crispy_forms.layout import Submit
from django import forms

from visprof.custom_layout import RadioWithOther
from visprof import models


class AccaoForm(forms.ModelForm):
    destinatarios = forms.MultipleChoiceField(
        label='Destinatários',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=models.Accao.Destinatario.choices)

    class Meta:
        model = models.Accao
        fields = ('destinatarios', 'designacao', 'abertura_pre_inscricao',
                  'fecho_pre_inscricao', 'nome_formador', 'numero_horas',
                  'acreditacao', 'local', 'modalidade', 'etc', 'estado')
        widgets = {'estado': forms.HiddenInput()}

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = 'accao_form'
        helper.layout = Layout(
            'estado',
            Row(
                Column('designacao', 'nome_formador', 'numero_horas',
                       'acreditacao', 'local', 'modalidade'),
                Column(
                    'destinatarios',
                    Field('abertura_pre_inscricao',
                          placeholder='YYYY-MM-DD HH:MM'),
                    Field('fecho_pre_inscricao',
                          placeholder='YYYY-MM-DD HH:MM'))),
            Row(Column('etc')),
            Div(
                # Button('cancelar',
                #        'Cancelar',
                #        css_class='btn btn-danger mr-auto',
                #        data_toggle='modal',
                #        data_target='#cancelar-modal'),
                (Submit('submit', 'Guardar', css_class='btn-secondary')
                 if self.instance.pk is None or
                 self.instance.estado == models.Accao.Estado.RASCUNHO else None
                ),
                Button('publicar',
                       'Publicar',
                       css_class='btn btn-primary ml-2',
                       data_toggle='modal',
                       data_target='#publicar-modal'),
                css_class='d-flex justify-content-end'))
        return helper

    def clean_destinatarios(self):
        # TODO(vitor): Mover esta lógica para um CommaSeparatedStringField.
        return ','.join(self.cleaned_data['destinatarios'])


class PreInscricaoForm(forms.ModelForm):
    email = forms.EmailField(required=False, disabled=True)
    confirmo = forms.BooleanField(label=(
        'Aceito que os meus dados pessoais sejam conservados pelo período '
        'de tempo necessário ao cumprimento da sua finalidade. A recolha de '
        'dados pessoais, integrados no presente formulário, tem como '
        'finalidade exclusiva a inscrição na presente acção de formação e a '
        'posterior emissão do respectivo certificado de participação.'),
                                  required=True)

    class Meta:
        model = models.Docente
        fields = ('email', 'nome_completo', 'nif', 'id_sighre',
                  'grupo_recrutamento', 'escola_vinculado', 'telemovel')
        widgets = {'nivel_ensino': forms.RadioSelect()}

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            'email',
            Row(Column('nome_completo', css_class='col-md-8'),
                Column('telemovel')),
            Row(Column('nif'),
                Column('id_sighre'), Column('grupo_recrutamento')),
            Row(Column('escola_vinculado')), 'confirmo',
            Div(Submit('submit', 'Pré-inscrever'),
                css_class='d-flex flex-row-reverse'))
        return helper

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def validate_unique(self):
        pass


class InscricaoForm(PreInscricaoForm):
    email = forms.EmailField(required=False, disabled=True)

    class Meta(PreInscricaoForm.Meta):
        fields = ('email', 'nome_completo', 'morada', 'codigo_postal',
                  'localidade', 'telemovel', 'telefone', 'grupo_recrutamento',
                  'indice_vencimento', 'escalao', 'data_nascimento', 'id_civil',
                  'nif', 'id_sighre', 'iban', 'habilitacao_academica',
                  'outra_habilitacao_academica', 'escola_vinculado',
                  'escola_funcoes', 'situacao_profissional',
                  'outra_situacao_profissional', 'nivel_ensino', 'anos_servico',
                  'dias_servico', 'proxima_mudanca_escalao')

    def __init__(self, *args, read_only=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._read_only = read_only
        if read_only:
            for field in self.fields.values():
                field.disabled = True
        self.fields['outra_habilitacao_academica'].label = ''
        self.fields['outra_habilitacao_academica'].required = False
        self.fields['outra_situacao_profissional'].label = ''
        self.fields['outra_situacao_profissional'].required = False

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_class = 'mt-3'
        submit_div = (Div(Submit('submit', 'Inscrever'),
                          css_class='d-flex flex-row-reverse')
                      if not self._read_only else None)
        nivel_ensino = (Column(Field('nivel_ensino', disabled=True))
                        if self._read_only else Column(Field('nivel_ensino')))
        helper.layout = Layout(
            Fieldset(
                'Dados pessoais', 'email', 'nome_completo',
                Row(Column('morada', css_class='col-md-7'),
                    Column(Field('codigo_postal', placeholder='XXXX-XXX')),
                    Column('localidade')),
                Row(Column('telemovel'), Column('telefone'),
                    Column(Field('data_nascimento', placeholder='YYYY-MM-DD'))),
                Row(Column('id_civil'), Column('nif'), Column('iban'))),
            Fieldset(
                'Dados profissionais',
                Row(Column('id_sighre'), Column('grupo_recrutamento'),
                    Column('indice_vencimento'), Column('escalao')),
                Row(Column('escola_vinculado'), Column('escola_funcoes')),
                Row(
                    Column(
                        RadioWithOther('habilitacao_academica',
                                       'outra_habilitacao_academica')),
                    nivel_ensino,
                    Column(RadioWithOther('situacao_profissional',
                                          'outra_situacao_profissional'),
                           css_class='col-md-5'))),
            Fieldset(
                'Antiguidade',
                Row(
                    Column('anos_servico'), Column('dias_servico'),
                    Column(
                        Field('proxima_mudanca_escalao',
                              placeholder='YYYY-MM-DD')))),
            ('confirmo' if not self._read_only else None), submit_div)
        return helper

    def clean(self):
        cleaned_data = super().clean()
        habilitacao_academica = cleaned_data.get('habilitacao_academica')
        outra_habilitacao_academica = cleaned_data.get(
            'outra_habilitacao_academica')
        situacao_profissional = cleaned_data.get('situacao_profissional')
        outra_situacao_profissional = cleaned_data.get(
            'outra_situacao_profissional')

        if (habilitacao_academica
                == models.Docente.HabilitacaoAcademica.OUTRA.value and  # pylint: disable=no-member
                not outra_habilitacao_academica):
            self.add_error('outra_habilitacao_academica',
                           'Especifique a "outra" habilitação académica.')

        if (situacao_profissional
                == models.Docente.SituacaoProfissional.OUTRA.value and  # pylint: disable=no-member
                not outra_situacao_profissional):
            self.add_error('outra_situacao_profissional',
                           'Especifique a "outra" situação profissional.')


class EnviarInscricoesForm(forms.Form):
    expiracao = forms.DateTimeField(
        label='Data de expiração',
        help_text=('Os docentes seleccionados não se poderão inscrever a '
                   'partir desta data.'))

    @property
    def helper(self):
        helper = FormHelper()
        helper.label_class = 'col-sm-4 col-form-label'
        helper.field_class = 'col-sm'
        helper.layout = Layout(
            Field('expiracao',
                  placeholder='YYYY-MM-DD HH:MM',
                  wrapper_class='row'),
            Submit('submit', 'Enviar inscrições', css_class='float-right'))
        return helper
