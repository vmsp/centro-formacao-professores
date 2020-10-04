import django_tables2 as tables
from django_tables2 import RequestConfig  # pylint: disable=unused-import

from visprof import core
from visprof import models


def _link_accao(record):
    view_name = ('editar_accao' if record.estado == models.Accao.Estado.RASCUNHO
                 else 'detalhe_accao')
    return core.reverse(view_name, args=[record.pk])


class AccoesTable(tables.Table):
    designacao = tables.Column(linkify=_link_accao)
    estado = tables.TemplateColumn(template_code="""\
        {% if record.pre_inscricoes_abertas %}
            <span class="text-success">{{ value }}</span>
        {% elif record.estado == "rascunho" %}
            <span class="text-muted">Rascunho</span>
        {% else %}
            <span>Fechado</span>
        {% endif %}
        """)

    class Meta:
        model = models.Accao
        fields = ('designacao', 'nome_formador', 'numero_horas', 'estado')


class PreInscricaoTable(tables.Table):
    escola = tables.Column(accessor='docente.escola_vinculado',
                           verbose_name='Escola')
    seleccionada = tables.TemplateColumn(template_code="""\
        <div class="custom-control custom-switch text-center">
          <input type="checkbox"
                 class="custom-control-input"
                 id="seleccionar_{{ record.id }}"
                 {% if record.estado == "seleccionada" %}checked{% endif %}
                 data-seleccionar>
          <label class="custom-control-label"
                 for="seleccionar_{{ record.id }}">
          </label>
        </div>
        """)

    class Meta:
        model = models.Inscricao
        fields = [
            'docente.user.email', 'docente.grupo_recrutamento', 'escola',
            'timestamp', 'seleccionada'
        ]
        row_attrs = {'data-id': lambda record: record.id}


class InscricoesTable(tables.Table):
    escola = tables.Column(accessor='docente.escola_vinculado',
                           verbose_name='Escola')
    estado = tables.TemplateColumn(template_code="""\
        {% if record.estado == "seleccionada" %}
           <span class="text-danger">✗ Por preencher</span>
        {% elif record.estado == "preenchida" %}
           <span class="text-warning">⍻ Preenchida</span>
        {% elif record.estado == "confirmada" %}
           <span class="text-success">✓ Confirmada</span>
        {% endif %}
        """)

    class Meta:
        model = models.Inscricao
        fields = ('docente.user.email', 'docente.nome_completo', 'escola',
                  'estado')


def confirmar_inscricao_link(record):
    return core.reverse('confirmar_inscricao', args=[record.pk])


class ConfirmarInscricoesTable(tables.Table):
    email = tables.Column(accessor='docente.user.email',
                          linkify=confirmar_inscricao_link)
    estado = tables.TemplateColumn(template_code="""\
        {% if record.estado == "seleccionada" %}
           <span class="text-danger">✗ Por preencher</span>
        {% elif record.estado == "preenchida" %}
           <span class="text-warning">⍻ Preenchida</span>
        {% elif record.estado == "confirmada" %}
           <span class="text-success">✓ Confirmada</span>
        {% endif %}
        """)

    class Meta:
        model = models.Inscricao
        fields = ('email', 'docente.nome_completo', 'estado')
        attrs = {'class': 'table table-hover'}
