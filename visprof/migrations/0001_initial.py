# Generated by Django 3.1 on 2020-09-19 16:22

from django.conf import settings
import django.core.validators
from django.db import migrations
from django.db import models
import django.db.models.deletion

import visprof.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('password',
                 models.CharField(max_length=128, verbose_name='password')),
                ('last_login',
                 models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name='last login')),
                ('is_superuser',
                 models.BooleanField(
                     default=False,
                     help_text=
                     'Designates that this user has all permissions without explicitly assigning them.',
                     verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nome_completo', models.CharField(blank=True, max_length=255)),
                ('is_active',
                 models.BooleanField(
                     default=True,
                     help_text=
                     'Indica se o utilizador deve ser considerado activo. Desseleccione este campo em vez de remover o utilizador.',
                     verbose_name='activo')),
                ('is_staff',
                 models.BooleanField(
                     default=False,
                     help_text=
                     'Designa utilizadores que podem aceder a este painel de adminstração',
                     verbose_name='administrador')),
                ('groups',
                 models.ManyToManyField(
                     blank=True,
                     help_text=
                     'The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                     related_name='user_set',
                     related_query_name='user',
                     to='auth.Group',
                     verbose_name='groups')),
                ('user_permissions',
                 models.ManyToManyField(
                     blank=True,
                     help_text='Specific permissions for this user.',
                     related_name='user_set',
                     related_query_name='user',
                     to='auth.Permission',
                     verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'utilizador',
                'verbose_name_plural': 'utilizadores',
            },
            managers=[
                ('objects', visprof.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Accao',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('destinatarios', models.CharField(blank=True, max_length=255)),
                ('designacao',
                 models.CharField(blank=True,
                                  max_length=255,
                                  verbose_name='designação')),
                ('abertura_pre_inscricao',
                 models.DateTimeField(
                     blank=True,
                     help_text=
                     'Data a partir do qual os docentes se poderão pré-inscrever na acção de formação.',
                     null=True,
                     verbose_name='abertura de pré-inscrições')),
                ('fecho_pre_inscricao',
                 models.DateTimeField(
                     blank=True,
                     help_text=
                     'Data limite para pré-inscrições. O formulário de pré-inscrição não estará disponível aos interessados, a partir desta data.',
                     null=True,
                     verbose_name='fecho de pré-inscrições')),
                ('nome_formador',
                 models.CharField(blank=True,
                                  max_length=255,
                                  verbose_name='nome do(a) formador(a)')),
                ('numero_horas',
                 models.PositiveIntegerField(blank=True,
                                             null=True,
                                             verbose_name='número de horas')),
                ('acreditacao',
                 models.CharField(blank=True,
                                  max_length=255,
                                  verbose_name='acreditação')),
                ('local', models.CharField(blank=True, max_length=255)),
                ('modalidade',
                 models.CharField(blank=True,
                                  choices=[('curso_de_formacao',
                                            'Curso de formação'),
                                           ('oficina_de_formacao',
                                            'Oficina de formação'),
                                           ('accao_de_curta_duracao',
                                            'Acção de curta duração')],
                                  max_length=32)),
                ('etc', models.TextField(blank=True)),
                ('estado',
                 models.CharField(choices=[('rascunho', 'Rascunho'),
                                           ('pre_inscricao', 'Pré-inscrição'),
                                           ('inscricao', 'Inscrição'),
                                           ('terminada', 'Terminada')],
                                  default='rascunho',
                                  max_length=32)),
                ('expiracao_inscricoes', models.DateTimeField(null=True)),
                ('emails_confirmacao_enviados', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'acção de formação',
                'verbose_name_plural': 'acções de formação',
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=255)),
                ('morada', models.CharField(blank=True, max_length=255)),
                ('codigo_postal',
                 models.CharField(
                     blank=True,
                     max_length=8,
                     validators=[
                         django.core.validators.RegexValidator(
                             '^[0-9]{4}-[0-9]{3}$',
                             'O código postal deve seguir o formato XXXX-XXX')
                     ],
                     verbose_name='código postal')),
                ('localidade', models.CharField(blank=True, max_length=255)),
                ('telemovel',
                 models.CharField(blank=True,
                                  max_length=16,
                                  verbose_name='telemóvel')),
                ('telefone', models.CharField(blank=True, max_length=16)),
                ('indice_vencimento',
                 models.CharField(
                     blank=True,
                     max_length=3,
                     validators=[
                         django.core.validators.RegexValidator(
                             '^[0-9]{3}$',
                             'O indice de vencimento é formado por 3 dígitos')
                     ],
                     verbose_name='índice de vencimento')),
                ('escalao',
                 models.IntegerField(
                     null=True,
                     validators=[
                         django.core.validators.MinValueValidator(1),
                         django.core.validators.MaxValueValidator(10)
                     ],
                     verbose_name='escalão')),
                ('data_nascimento',
                 models.DateField(null=True,
                                  verbose_name='data de nascimento')),
                ('id_civil',
                 models.CharField(
                     blank=True,
                     max_length=8,
                     verbose_name='número de identificação civil (CC ou BI)')),
                ('nif',
                 models.CharField(blank=True, max_length=9,
                                  verbose_name='NIF')),
                ('id_sighre',
                 models.CharField(blank=True,
                                  max_length=255,
                                  verbose_name='SIGHRE')),
                ('iban',
                 models.CharField(blank=True,
                                  max_length=21,
                                  verbose_name='IBAN')),
                ('habilitacao_academica',
                 models.CharField(choices=[('licenciatura', 'Licenciatura'),
                                           ('bacharelato', 'Bacharelato'),
                                           ('mestrado', 'Mestrado'),
                                           ('doutoramento', 'Doutoramento'),
                                           ('outra', 'Outra (especifique)')],
                                  default='licenciatura',
                                  max_length=255,
                                  verbose_name='habilitação académica')),
                ('outra_habilitacao_academica',
                 models.CharField(blank=True, max_length=255)),
                ('situacao_profissional',
                 models.CharField(choices=[
                     ('quadro_nomeacao_definitiva',
                      'Professor do quadro de nomeação definitiva'),
                     ('quadro_nomeacao_provisoria',
                      'Professor do quadro de nomeação provisória'),
                     ('quadro_zona_pedagogica',
                      'Professor do quadro de zona pedagógica'),
                     ('contratado_profissionalizado',
                      'Professor contratado profissionalizado'),
                     ('contratado_habilitacao_propria',
                      'Professor contratado com habilitação própria'),
                     ('contratado_habilitacao_suficiente',
                      'Professor contratado com habilitação suficiente'),
                     ('outra', 'Outra (especifique)')
                 ],
                                  default='quadro_nomeacao_definitiva',
                                  max_length=255,
                                  verbose_name='situação profissional')),
                ('outra_situacao_profissional',
                 models.CharField(blank=True, max_length=255)),
                ('nivel_ensino',
                 models.CharField(choices=[
                     ('pre_escolar', 'Pré-escolar'), ('ceb_1', '1º CEB'),
                     ('ceb_2', '2º CEB'), ('ceb_3', '3º CEB'),
                     ('secundario', 'Secundário'),
                     ('educacao_especial', 'Educação especial'),
                     ('ensino_profissional', 'Ensino profissional')
                 ],
                                  default='pre_escolar',
                                  max_length=64,
                                  verbose_name='nível de ensino')),
                ('anos_servico',
                 models.PositiveIntegerField(null=True,
                                             verbose_name='anos de serviço')),
                ('dias_servico',
                 models.PositiveIntegerField(
                     null=True,
                     verbose_name='dias de serviço (em acréscimo aos anos)')),
                ('proxima_mudanca_escalao',
                 models.DateField(blank=True,
                                  null=True,
                                  verbose_name='próxima mudança de escalão')),
            ],
            options={
                'verbose_name': 'docente',
                'verbose_name_plural': 'docentes',
            },
        ),
        migrations.CreateModel(
            name='GrupoDeRecrutamento',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('codigo', models.CharField(max_length=3)),
                ('nome', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'grupo de recrutamento',
                'verbose_name_plural': 'grupos de recrutamento',
                'ordering': ('codigo',),
            },
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('timestamp',
                 models.DateTimeField(auto_now_add=True,
                                      verbose_name='data de inscrição')),
                ('estado',
                 models.CharField(choices=[('nao_seleccionada',
                                            'Não seleccionada'),
                                           ('seleccionada', 'Seleccionada'),
                                           ('preenchida', 'Preenchida'),
                                           ('confirmada', 'Confirmada'),
                                           ('anulada', 'Anulada')],
                                  default='nao_seleccionada',
                                  max_length=16)),
                ('accao',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='visprof.accao',
                                   verbose_name='acção')),
                ('docente',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='visprof.docente')),
            ],
            options={
                'verbose_name': 'inscrição',
                'verbose_name_plural': 'inscrições',
            },
        ),
        migrations.CreateModel(
            name='Escola',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('codigo', models.CharField(max_length=16)),
                ('nome', models.CharField(max_length=255)),
                ('concelho', models.CharField(max_length=255)),
                ('distrito', models.CharField(max_length=255)),
                ('user',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'agrupamento/escola',
                'verbose_name_plural': 'agrupamentos/escolas',
            },
        ),
        migrations.AddField(
            model_name='docente',
            name='escola_funcoes',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='escola_funcoes',
                to='visprof.escola',
                verbose_name='agrupamento/escola em que exerce funções'),
        ),
        migrations.AddField(
            model_name='docente',
            name='escola_vinculado',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='escola_vinculada',
                to='visprof.escola',
                verbose_name='agrupamento/escola a que está vinculado'),
        ),
        migrations.AddField(
            model_name='docente',
            name='grupo_recrutamento',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    to='visprof.grupoderecrutamento',
                                    verbose_name='grupo de recrutamento'),
        ),
        migrations.AddField(
            model_name='docente',
            name='inscricoes',
            field=models.ManyToManyField(related_name='inscritos',
                                         through='visprof.Inscricao',
                                         to='visprof.Accao'),
        ),
        migrations.AddField(
            model_name='docente',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='inscricao',
            constraint=models.UniqueConstraint(fields=('accao', 'docente'),
                                               name='unique_inscricao'),
        ),
    ]
