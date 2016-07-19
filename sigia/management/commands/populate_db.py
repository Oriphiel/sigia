# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from sigia.models import Country, Province, Canton, Parish, Career, Period, \
    Course, UserProfile, Student
from django.contrib.auth.models import User
from django.utils import timezone
import codecs
from django.core.files import File
import sigia.settings as settings
import os


class Command(BaseCommand):
    args = '<none>'
    help = 'our help string comes here'

    def _create_user_profile(self, audit):
        user = User.objects.get(username='dariov')
        ec = Country.objects.get(name='Ecuador')

        file_path = os.path.join(settings.BASE_DIR, 'initial_media', 'dario-small.png')
        f = open(file_path, 'r')
        photo = File(f)
        guayas = Province.objects.get(name='Guayas')
        guayaquil = Canton.objects.get(name='Guayaquil')
        urdaneta = Parish.objects.get(name='Urdaneta - Guayaquil')

        user_profile = UserProfile(user=user, photo=photo, id_doc_type='C', id_doc_num='9851258452', gender='M',
                                   birthday=timezone.now(), nationality=ec, birthplace_country=ec,
                                   birthplace_province=guayas,
                                   birthplace_canton=guayaquil, birthplace_parish=urdaneta, address_province=guayas,
                                   address_canton=guayaquil, address_parish=urdaneta, marital_status='S',
                                   address='Urdaneta % Datiles y Monjas', )
        user_profile.save()

    def _create_countries(self, audit):
        Country.objects.bulk_create([Country(name='Ecuador', gentilicio='Ecuatoriana', **audit), ])

    def _create_province(self, audit):
        country = Country.objects.get(name='Ecuador')
        Province.objects.bulk_create([Province(country=country, name='Azuay', **audit),
                                      Province(country=country, name='Bolívar', **audit),
                                      Province(country=country, name='Cañar', **audit),
                                      Province(country=country, name='Carchi', **audit),
                                      Province(country=country, name='Chimborazo', **audit),
                                      Province(country=country, name='Cotopaxi', **audit),
                                      Province(country=country, name='El Oro', **audit),
                                      Province(country=country, name='Esmeraldas', **audit),
                                      Province(country=country, name='Galápagos', **audit),
                                      Province(country=country, name='Guayas', **audit),
                                      Province(country=country, name='Imbabura', **audit),
                                      Province(country=country, name='Loja', **audit),
                                      Province(country=country, name='Los Ríos', **audit),
                                      Province(country=country, name='Manabí', **audit),
                                      Province(country=country, name='Morona Santiago', **audit),
                                      Province(country=country, name='Napo', **audit),
                                      Province(country=country, name='Orellana', **audit),
                                      Province(country=country, name='Pastaza', **audit),
                                      Province(country=country, name='Pichincha', **audit),
                                      Province(country=country, name='Santa Elena', **audit),
                                      Province(country=country, name='Santo Domingo de los Tsáchilas', **audit),
                                      Province(country=country, name='Sucumbíos', **audit),
                                      Province(country=country, name='Tungurahua', **audit),
                                      Province(country=country, name='Zamora Chinchipe', **audit),
                                      ])

    def _create_canton(self, audit):
        canton_array = []
        print 'Opening canton file'
        f = codecs.open('cantones.csv', 'r', 'utf-8')
        print 'Reading canton content'
        for line in f:
            array = line.split(';')
            province_name = array[0].strip()
            canton_name = array[1].strip()
            print 'Adding Canton: %s of Province: %s' % (canton_name, province_name)
            province = Province.objects.get(name=province_name)
            canton_array.append(Canton(province=province, name=canton_name, **audit))
        Canton.objects.bulk_create(canton_array);

    def _create_parish(self, audit):
        parish_array = []
        print 'Opening parish file'
        f = codecs.open('parroquias.csv', 'r', 'utf-8')
        print 'Reading parish content'
        for line in f:
            array = line.split(';')
            province_name = array[0].strip()
            canton_name = array[1].strip()
            parish_name = array[2].strip()
            print 'Adding Parish: %s, of Canton: %s, of Province: %s' % (parish_name, canton_name, province_name)
            province = Province.objects.get(name=province_name)
            canton = Canton.objects.get(province=province, name=canton_name)
            parish_array.append(Parish(canton=canton, name=parish_name, **audit))
        Parish.objects.bulk_create(parish_array)

    def _create_careers(self, audit):
        careers_array = []
        inf = Career(name='Informática', description='Formación integral en sistemas.', **audit)
        admin_emp = Career(name='Administración de Empresas',
                           description='Formación integral en administración de empresas.', **audit)
        careers_array.append(inf)
        careers_array.append(admin_emp)
        Career.objects.bulk_create(careers_array)

    def _create_period(self, audit):
        Period(name="2014-2015", finalized=False, start_notes='Iniciado OK', **audit).save()

    def _create_courses(self, audit):
        period = Period.objects.get(name="2014-2015")
        inf = Career.objects.get(name='Informática')
        adm = Career.objects.get(name='Administración de Empresas')
        courses_array = []
        inf1 = Course(career=inf, description='Primer Nivel Inf.', type='P', period=period,
                      semester='A', level=1, parallel='A', max_quota=20, quota=0, payment_reg=10,
                      payment_ext=20, payment_esp=30, **audit)
        adm1 = Course(career=adm, description='Primer Nivel Adm. Emp.', type='P', period=period,
                      semester='A', level=1, parallel='A', max_quota=20, quota=0, payment_reg=10,
                      payment_ext=20, payment_esp=30, **audit)
        courses_array.append(inf1)
        courses_array.append(adm1)
        Course.objects.bulk_create(courses_array)

    def _create_student(self, audit):
        inf = Career.objects.get(name='Informática')
        ec = Country.objects.get(name='Ecuador')
        user = User(username='pepe.mariony', first_name='pepe', last_name='mariony', email='pepe.mariony@gmail.com')
        user.save()

        file_path = os.path.join(settings.BASE_DIR, 'initial_media', 'Koala.jpg')
        f = open(file_path, 'r')
        photo = File(f)
        guayas = Province.objects.get(name='Guayas')
        guayaquil = Canton.objects.get(name='Guayaquil')
        urdaneta = Parish.objects.get(name='Urdaneta - Guayaquil')

        user_profile = UserProfile(user=user, photo=photo, id_doc_type='C', id_doc_num='9851258452', gender='M',
                                   birthday=timezone.now(), nationality=ec, birthplace_country=ec,
                                   birthplace_province=guayas,
                                   birthplace_canton=guayaquil, birthplace_parish=urdaneta, address_province=guayas,
                                   address_canton=guayaquil, address_parish=urdaneta, marital_status='S',
                                   address='Urdaneta % Datiles y Monjas', )
        user_profile.save()

        student = Student(user=user, career=inf, campus_orig='Makao', campus_city='Forkos',
                          specialization='Técnico de equipos eléctricos', language_know_lvl='B',
                          informatic_know_lvl='B')
        student.save()

    def handle(self, *args, **options):
        user = User.objects.all()[0]
        date = timezone.now()
        audit = {'created_by': user, 'modified_by': user, 'created': date, 'modified': date}

        self._create_countries(audit)
        self._create_province(audit)
        self._create_canton(audit)
        self._create_parish(audit)

# self._create_careers(audit)
#        self._create_period(audit)
#        self._create_courses(audit)
#        self._create_student(audit)
#        self._create_user_profile(audit)
