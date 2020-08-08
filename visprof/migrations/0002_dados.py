# Generated by Django 3.1 on 2020-08-14 22:18

from django.conf import settings
from django.db import migrations


def inserir_dados_iniciais(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Escola = apps.get_model('visprof', 'Escola')
    Grupo = apps.get_model('visprof', 'GrupoDeRecrutamento')

    User.objects.create_superuser('vitor@cfaedeviseu.pt', 'kadavra123')

    pessoal = Group(name='Pessoal')
    pessoal.save()
    pessoal.permissions.set(
        Permission.objects.filter(codename__in=('add_accao', 'change_accao',
                                                'delete_accao',
                                                'change_inscricao')))

    Escola.objects.bulk_create([
        Escola(codigo='400002',
               nome='Escola Secundária Alves Martins',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('alvesmartins@mail.com')),
        Escola(codigo='401626',
               nome='Escola Secundária Emídio Navarro',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('example@emidionavarro.com')),
        Escola(codigo='402977',
               nome='Escola Secundária Viriato',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('example@viriato.com')),
        Escola(codigo='160593',
               nome='Agrupamento Escolas de Mundão',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('example@mundao.pt')),
        Escola(codigo='161871',
               nome='Agrupamento de Escolas do Viso',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('example@viso.com')),
        Escola(codigo='161858',
               nome='Agrupamento de Escolas Grão Vasco',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('example@graovasco.com')),
        Escola(codigo='161860',
               nome='Agrupamento de Escolas Infante D. Henrique',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('example@infantedhenrique.com')),
        Escola(codigo='160635',
               nome='Agrupamento de Escolas Viseu Norte',
               concelho='Viseu',
               distrito='Viseu',
               user=User.objects.create_user('example@viseu_norte.pt')),
    ])

    Grupo.objects.bulk_create([
        Grupo(codigo='100', nome='Educação Pré-Escolar'),
        Grupo(codigo='110', nome='Ensino Básico - 1º Ciclo'),
        Grupo(codigo='120', nome='Inglês'),
        Grupo(codigo='200', nome='Português e Estudos Sociais/História'),
        Grupo(codigo='210', nome='Português e Francês'),
        Grupo(codigo='220', nome='Português e Inglês'),
        Grupo(codigo='230', nome='Matemática e Ciências da Natureza '),
        Grupo(codigo='240', nome='Educação Visual e Tecnológica'),
        Grupo(codigo='250', nome='Educação Musical'),
        Grupo(codigo='260', nome='Educação Física'),
        Grupo(codigo='290', nome='Educação Moral e Religiosa'),
        Grupo(codigo='300', nome='Português'),
        Grupo(codigo='310', nome='Latim e Grego '),
        Grupo(codigo='320', nome='Francês'),
        Grupo(codigo='330', nome='Inglês'),
        Grupo(codigo='340', nome='Alemão'),
        Grupo(codigo='350', nome='Espanhol'),
        Grupo(codigo='400', nome='História'),
        Grupo(codigo='410', nome='Filosofia'),
        Grupo(codigo='420', nome='Geografia'),
        Grupo(codigo='430', nome='Economia e Contabilidade'),
        Grupo(codigo='500', nome='Matemática'),
        Grupo(codigo='510', nome='Física e Química'),
        Grupo(codigo='520', nome='Biologia e Geologia '),
        Grupo(codigo='530', nome='Educação Tecnológica'),
        Grupo(codigo='540', nome='Electrotecnia'),
        Grupo(codigo='550', nome='Informática'),
        Grupo(codigo='560', nome='Ciências Agro-pecuárias '),
        Grupo(codigo='600', nome='Artes Visuais '),
        Grupo(codigo='610', nome='Música'),
        Grupo(codigo='620', nome='Educação Física'),
        Grupo(codigo='360', nome='Língua Gestual Portuguesa '),
        Grupo(codigo='910', nome='Educação Especial'),
        Grupo(codigo='920', nome='Educação Especial'),
        Grupo(codigo='930', nome='Educação Especial'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('visprof', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(inserir_dados_iniciais, migrations.RunPython.noop)
    ]