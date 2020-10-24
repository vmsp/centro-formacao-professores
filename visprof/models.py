from django.contrib.auth import hashers
from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models
from django.db import transaction
from django.urls import reverse
from django.utils import timezone


class UserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email inválido')
        user = self.model(email=self.normalize_email(email))
        # User.set_password() can't be used in migrations, use
        # django.contrib.auth.hashers.make_password()
        user.password = hashers.make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(unique=True)
    nome_completo = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(
        'activo',
        default=True,
        help_text=('Indica se o utilizador deve ser considerado activo. '
                   'Desseleccione este campo em vez de remover o utilizador.'))
    is_staff = models.BooleanField(
        'administrador',
        default=False,
        help_text=('Designa utilizadores que podem aceder a este painel de '
                   'adminstração'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'utilizador'
        verbose_name_plural = 'utilizadores'

    def get_full_name(self):
        return self.nome_completo

    def get_short_name(self):
        if self.nome_completo:
            return self.nome_completo.split()[0]
        return ''


class Accao(models.Model):

    class Destinatario(models.TextChoices):
        EDUCADORES = 'educadores', 'Educadores'
        ENSINO_BASICO = 'ensino_basico', 'Professores do ensino básico'
        ENSINO_SECUNDARIO = ('ensino_secundario',
                             'Professores do ensino secundário')
        ENSINO_ESPECIAL = 'ensino_especial', 'Professores do ensino especial'

    class Modalidade(models.TextChoices):
        CURSO_DE_FORMACAO = 'curso_de_formacao', 'Curso de formação'
        OFICINA_DE_FORMACAO = 'oficina_de_formacao', 'Oficina de formação'
        ACCAO_DE_CURTA_DURACAO = ('accao_de_curta_duracao',
                                  'Acção de curta duração')

    class Estado(models.TextChoices):
        RASCUNHO = 'rascunho', 'Rascunho'
        PRE_INSCRICAO = 'pre_inscricao', 'Pré-inscrição'
        INSCRICAO = 'inscricao', 'Inscrição'
        TERMINADA = 'terminada', 'Terminada'

    destinatarios = models.CharField(max_length=255, blank=True)
    designacao = models.CharField('designação', max_length=255, blank=True)
    abertura_pre_inscricao = models.DateTimeField(
        'abertura de pré-inscrições',
        help_text=('Data a partir do qual os docentes se poderão pré-inscrever '
                   'na acção de formação.'),
        blank=True,
        null=True)
    fecho_pre_inscricao = models.DateTimeField(
        'fecho de pré-inscrições',
        help_text=(
            'Data limite para pré-inscrições. O formulário de pré-inscrição '
            'não estará disponível aos interessados, a partir desta data.'),
        blank=True,
        null=True)
    nome_formador = models.CharField('nome do(a) formador(a)',
                                     max_length=255,
                                     blank=True)
    numero_horas = models.PositiveIntegerField('número de horas',
                                               blank=True,
                                               null=True)
    acreditacao = models.CharField('acreditação', max_length=255, blank=True)
    local = models.CharField(max_length=255, blank=True)
    modalidade = models.CharField(max_length=32,
                                  choices=Modalidade.choices,
                                  blank=True)
    etc = models.TextField(blank=True)  # Incluí os critérios de selecção

    estado = models.CharField(max_length=32,
                              choices=Estado.choices,
                              default=Estado.RASCUNHO)
    expiracao_inscricoes = models.DateTimeField(null=True)
    emails_confirmacao_enviados = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'acção de formação'
        verbose_name_plural = 'acções de formação'
        ordering = ['-estado', '-abertura_pre_inscricao']

    def __str__(self):
        return self.designacao

    def get_absolute_url(self):
        return reverse('detalhe_accao', args=[self.id])

    def get_destinarios_display(self):
        if not self.destinatarios:
            return []
        return [
            Accao.Destinatario(d).label for d in self.destinatarios.split(',')
        ]

    def pre_inscricoes_abertas(self):
        return (self.estado == Accao.Estado.PRE_INSCRICAO and
                (self.abertura_pre_inscricao <= timezone.now() <
                 self.fecho_pre_inscricao))

    def publicar(self):
        self.estado = Accao.Estado.PRE_INSCRICAO
        self.save()

    def pre_inscrever(self, docente):
        with transaction.atomic():
            docente.save()
            Inscricao.objects.get_or_create(accao=self, docente=docente)


class GrupoDeRecrutamento(models.Model):
    codigo = models.CharField(max_length=3)
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'grupo de recrutamento'
        verbose_name_plural = 'grupos de recrutamento'
        ordering = ('codigo',)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Escola(models.Model):
    codigo = models.CharField(max_length=16)
    nome = models.CharField(max_length=255)
    concelho = models.CharField(max_length=255)
    distrito = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    class Meta:
        verbose_name = 'agrupamento/escola'
        verbose_name_plural = 'agrupamentos/escolas'

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Docente(models.Model):

    class HabilitacaoAcademica(models.TextChoices):
        LICENCIATURA = 'licenciatura', 'Licenciatura'
        BACHARELATO = 'bacharelato', 'Bacharelato'
        MESTRADO = 'mestrado', 'Mestrado'
        DOUTORAMENTO = 'doutoramento', 'Doutoramento'
        OUTRA = 'outra', 'Outra (especifique)'

    class SituacaoProfissional(models.TextChoices):
        QUADRO_NOMEACAO_DEFINITIVA = (
            'quadro_nomeacao_definitiva',
            'Professor do quadro de nomeação definitiva')
        QUADRO_NOMEACAO_PROVISORIA = (
            'quadro_nomeacao_provisoria',
            'Professor do quadro de nomeação provisória')
        QUADRO_ZONA_PADAGOGICA = ('quadro_zona_pedagogica',
                                  'Professor do quadro de zona pedagógica')
        CONTRATADO_PROFISSIONALIZADO = (
            'contratado_profissionalizado',
            'Professor contratado profissionalizado')
        CONTRATADO_HABILITACAO_PROPRIA = (
            'contratado_habilitacao_propria',
            'Professor contratado com habilitação própria')
        CONTRATADO_HABILITICAO_SUFICIENTE = (
            'contratado_habilitacao_suficiente',
            'Professor contratado com habilitação suficiente')
        OUTRA = 'outra', 'Outra (especifique)'

    class NivelDeEnsino(models.TextChoices):
        PRE_ESCOLAR = 'pre_escolar', 'Pré-escolar'
        CEB_1 = 'ceb_1', '1º CEB'
        CEB_2 = 'ceb_2', '2º CEB'
        CEB_3 = 'ceb_3', '3º CEB'
        SECUNDARIO = 'secundario', 'Secundário'
        EDUCACAO_ESPECIAL = 'educacao_especial', 'Educação especial'
        ENSINO_PROFISSIONAL = 'ensino_profissional', 'Ensino profissional'

    nome_completo = models.CharField(max_length=255)
    morada = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(
        'código postal',
        max_length=8,
        validators=[
            validators.RegexValidator(
                '^[0-9]{4}-[0-9]{3}$',
                'O código postal deve seguir o formato XXXX-XXX')
        ],
        blank=True)
    localidade = models.CharField(max_length=255, blank=True)
    telemovel = models.CharField('telemóvel', max_length=16, blank=True)
    telefone = models.CharField(max_length=16, blank=True)
    grupo_recrutamento = models.ForeignKey(GrupoDeRecrutamento,
                                           on_delete=models.CASCADE,
                                           verbose_name='grupo de recrutamento',
                                           null=True)
    indice_vencimento = models.CharField(
        'índice de vencimento',
        max_length=3,
        validators=[
            validators.RegexValidator(
                '^[0-9]{3}$', 'O indice de vencimento é formado por 3 dígitos')
        ],
        blank=True)
    escalao = models.IntegerField('escalão',
                                  validators=[
                                      validators.MinValueValidator(1),
                                      validators.MaxValueValidator(10),
                                  ],
                                  null=True)
    data_nascimento = models.DateField('data de nascimento', null=True)
    id_civil = models.CharField('número de identificação civil (CC ou BI)',
                                max_length=8,
                                blank=True)
    nif = models.CharField('NIF', max_length=9, blank=True)
    id_sighre = models.CharField('SIGHRE', max_length=255, blank=True)
    iban = models.CharField('IBAN', max_length=21, blank=True)
    habilitacao_academica = models.CharField(
        'habilitação académica',
        max_length=255,
        choices=HabilitacaoAcademica.choices,
        default=HabilitacaoAcademica.LICENCIATURA)
    outra_habilitacao_academica = models.CharField(max_length=255, blank=True)
    escola_vinculado = models.ForeignKey(
        Escola,
        on_delete=models.CASCADE,
        related_name='escola_vinculada',
        verbose_name='agrupamento/escola a que está vinculado',
        null=True)
    escola_funcoes = models.ForeignKey(
        Escola,
        on_delete=models.CASCADE,
        related_name='escola_funcoes',
        verbose_name='agrupamento/escola em que exerce funções',
        null=True)
    situacao_profissional = models.CharField(
        'situação profissional',
        max_length=255,
        choices=SituacaoProfissional.choices,
        default=SituacaoProfissional.QUADRO_NOMEACAO_DEFINITIVA)
    outra_situacao_profissional = models.CharField(max_length=255, blank=True)
    nivel_ensino = models.CharField('nível de ensino',
                                    max_length=64,
                                    choices=NivelDeEnsino.choices,
                                    default=NivelDeEnsino.PRE_ESCOLAR)

    anos_servico = models.PositiveIntegerField('anos de serviço', null=True)
    dias_servico = models.PositiveIntegerField(
        'dias de serviço (em acréscimo aos anos)', null=True)
    proxima_mudanca_escalao = models.DateField('próxima mudança de escalão',
                                               blank=True,
                                               null=True)

    inscricoes = models.ManyToManyField(Accao,
                                        through='Inscricao',
                                        related_name='inscritos')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def email(self):
        if self.user:
            return self.user.email
        return None

    class Meta:
        verbose_name = 'docente'
        verbose_name_plural = 'docentes'

    def __str__(self):
        return self.nome_completo


class Inscricao(models.Model):

    class Estado(models.TextChoices):
        NAO_SELECCIONADA = 'nao_seleccionada', 'Não seleccionada'
        SELECCIONADA = 'seleccionada'
        PREENCHIDA = 'preenchida'
        CONFIRMADA = 'confirmada'
        ANULADA = 'anulada'

    accao = models.ForeignKey(Accao,
                              on_delete=models.CASCADE,
                              verbose_name='acção')
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    timestamp = models.DateTimeField('data de inscrição', auto_now_add=True)

    estado = models.CharField(max_length=16,
                              choices=Estado.choices,
                              default=Estado.NAO_SELECCIONADA)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['accao', 'docente'],
                                    name='unique_inscricao')
        ]
        verbose_name = 'inscrição'
        verbose_name_plural = 'inscrições'

    def __str__(self):
        return f'{self.accao} - {self.docente}'
