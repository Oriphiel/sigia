# -*- coding: utf-8 -*-
"""
Created on 12/12/2014

@author: Dario
"""

from __future__ import unicode_literals
from django_extensions.db.models import TimeStampedModel
from audit_log.models import AuthStampedModel
from django.db import models
from django.contrib.auth.models import User
from livefield import LiveModel
from django.db.models.fields.related import OneToOneField
from roman import toRoman
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField

SEMESTER_CHOICES = (('A', 'Semestre A'),
                    ('B', 'Semestre B'))

PARALLEL_CHOICES = (('A', 'Paralelo A'),
                    ('B', 'Paralelo B'),
                    ('C', 'Paralelo C'),
                    ('D', 'Paralelo D'),
                    ('E', 'Paralelo E'),
                    ('F', 'Paralelo F'),
                    ('G', 'Paralelo G'),
                    ('H', 'Paralelo H'),
                    ('I', 'Paralelo I'),
                    ('J', 'Paralelo J'),
                    ('K', 'Paralelo K'),
                    ('L', 'Paralelo L'),
                    ('M', 'Paralelo M'),
                    ('N', 'Paralelo N'),
                    ('O', 'Paralelo O'),
                    ('P', 'Paralelo P'),
                    ('Q', 'Paralelo Q'),
                    ('R', 'Paralelo R'),
                    ('S', 'Paralelo S'),
                    ('T', 'Paralelo T'),
                    ('U', 'Paralelo U'),
                    ('V', 'Paralelo V'),
                    ('W', 'Paralelo W'),
                    ('X', 'Paralelo X'),
                    ('Y', 'Paralelo Y'),
                    ('Z', 'Paralelo Z'),)

LEVEL_CHOICES = ((0, 'Pre-Tecnológico'),
                 (1, 'Primer Nivel'),
                 (2, 'Segundo Nivel'),
                 (3, 'Tercer Nivel'),
                 (4, 'Cuarto Nivel'),
                 (5, 'Quinto Nivel'),
                 (6, 'Sexto Nivel'),
                 (7, 'Unidad de Titulación'),
                 (8, 'ENES'),
                 (9, 'Curso de Educación Continua'),
                 (10, 'Ser Bachiller'),
                 (11, 'Certificaciones'),
                 (12, 'Culminación de Estudios'),
                 (13, 'Otros'))

QUALITATIVE_LEVEL_CHOICES = (('B', 'Básico'),
                             ('I', 'Intermedio'),
                             ('A', 'Avanzado'))


class Period(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'período'
        managed = False

    name = models.CharField(max_length=9, unique=True, verbose_name="nombre")
    predecessor = models.ForeignKey("Period", null=True, blank=True, verbose_name="predecessor")
    finalized = models.BooleanField(default=False, verbose_name="finalizado")
    active = models.BooleanField(default=False, verbose_name="activo")
    start_notes = models.TextField(null=True, blank=True, verbose_name="anotaciones de inicio")
    end_notes = models.TextField(null=True, blank=True, verbose_name="anotaciones de fin")

    def __unicode__(self):
        return "%s" % self.name


class Country(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'país'
        verbose_name_plural = 'países'
        managed = False

    name = models.CharField(max_length=50, unique=True, verbose_name="nombre", blank=True)
    gentilicio = models.CharField(max_length=50, verbose_name="nacionalidad", blank=True)

    def __unicode__(self):
        return "%s" % self.name


class Province(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'provincia'
        managed = False

    country = models.ForeignKey(Country, verbose_name="país", blank=True)
    name = models.CharField(max_length=50, verbose_name="nacionalidad", blank=True)

    def __unicode__(self):
        return "%s" % self.name


class Canton(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'cantón'
        verbose_name_plural = 'cantones'
        managed = False

    province = models.ForeignKey(Province, verbose_name="provincia", blank=True)
    name = models.CharField(max_length=50, verbose_name="nombre", blank=True)

    def __unicode__(self):
        return "%s" % self.name


class Parish(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'parroquia'
        managed = False

    canton = models.ForeignKey(Canton, verbose_name="cantón", blank=True)
    name = models.CharField(max_length=50, verbose_name="nombre", blank=True)

    def __unicode__(self):
        return "%s" % self.name


class EthnicGroup(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'grupo étnico'
        managed = False

    name = models.CharField(max_length=50, verbose_name="nombre", blank=True)
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name="descripción")

    def __unicode__(self):
        return "%s" % self.name


class Institution(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'institución educativa'
        managed = False

    name = models.CharField(max_length=100, verbose_name="nombre")
    main = BooleanField(default=False, verbose_name="unidad académica matriz")
    photo = models.ImageField(null=True, upload_to='institution_photos',
                              default='institution_photos/anonymous.jpg',
                              verbose_name="foto")
    logo = models.ImageField(null=True, upload_to='institution_logos',
                             default='institution_logos/anonymous.jpg',
                             verbose_name="logo")
    address = models.TextField(verbose_name="dirección")
    zip_address = models.CharField(max_length=11, verbose_name="dirección postal")
    ruc = models.CharField(max_length=11, verbose_name="RUC")
    active_semester = models.CharField(max_length=1, verbose_name="semestre activo")
    active_period = models.ForeignKey(Period, verbose_name="período activo")
    mission = models.TextField(verbose_name="misión")
    vision = models.TextField(verbose_name="visión")
    phone_one = models.CharField(max_length=12, verbose_name="teléfono 1")
    phone_two = models.CharField(max_length=12, verbose_name="teléfono 2")


class UserProfile(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'perfil de usuario'
        verbose_name_plural = 'perfiles de los usuarios'
        managed = False

    ID_DOC_CHOICES = (('C', 'Cédula'),
                      ('P', 'Pasaporte'))

    GENDER_CHOICES = (('M', 'Masculino'),
                      ('F', 'Femenino'))

    MARITAL_STATUS_CHOICES = (('S', 'Soltero'),
                              ('C', 'Casado'),
                              ('D', 'Divorciado'),
                              ('U', 'Unión Libre'))

    # Personal Information
    user = OneToOneField(User, related_name="profile")
    photo = models.ImageField(null=True, upload_to='user_photos',
                              default='user_photos/anonymous.jpg',
                              verbose_name="foto")
    id_doc_type = models.CharField(null=True, max_length=1, choices=ID_DOC_CHOICES, verbose_name="tipo de documento")
    id_doc_num = models.CharField(null=True, max_length=20, verbose_name="número de identidad")
    gender = models.CharField(null=True, max_length=1, choices=GENDER_CHOICES, verbose_name="género")
    birthday = models.DateField(null=True, verbose_name="fecha de nacimiento")
    nationality = models.ForeignKey(Country, null=True, related_name='nationality', verbose_name="nacionalidad",
                                    blank=True)
    birthplace_country = models.ForeignKey(Country, null=True, related_name='birthplace_country',
                                           verbose_name="país de nacimiento", blank=True)
    birthplace_province = models.ForeignKey(Province, null=True, related_name='birthplace_province',
                                            verbose_name="provincia de nacimiento", blank=True)
    birthplace_canton = models.ForeignKey(Canton, null=True, related_name='birthplace_canton',
                                          verbose_name="cantón de nacimiento", blank=True)
    birthplace_parish = models.ForeignKey(Parish, null=True, related_name='birthplace_parish',
                                          verbose_name="parroquia de nacimiento", blank=True)
    address_province = models.ForeignKey(Province, null=True, related_name='address_province',
                                         verbose_name="provincia de residencia", blank=True)
    address_canton = models.ForeignKey(Canton, null=True, related_name='address_canton',
                                       verbose_name="cantón de residencia", blank=True)
    address_parish = models.ForeignKey(Parish, null=True, related_name='address_parish',
                                       verbose_name="parroquia de residencia", blank=True)
    marital_status = models.CharField(null=True, max_length=1, choices=MARITAL_STATUS_CHOICES,
                                      verbose_name="estado civil")
    address = models.TextField(null=True, verbose_name="dirección personal")
    telephone = models.CharField(max_length=30, null=True, blank=True, verbose_name="teléfono")
    cellphone = models.CharField(max_length=30, null=True, blank=True, verbose_name="celular")
    handed_id_doc = models.NullBooleanField(default=False, null=True, verbose_name="entregó documento de identidad")
    id_doc_img = models.ImageField(upload_to='id_doc_img', null=True, blank=True, verbose_name="documento de identidad")
    handed_voting_cert = models.NullBooleanField(default=False, null=True,
                                                 verbose_name="entregó certificado de votación")
    voting_cert_img = models.ImageField(upload_to='voting_cert_img', null=True, blank=True,
                                        verbose_name="certificado de votación")
    handed_degree = models.NullBooleanField(default=False, null=True,
                                            verbose_name="entregó copia de título/acta de grado notariada")
    handed_degree_img = models.ImageField(upload_to='handed_degree_img', null=True, blank=True,
                                          verbose_name="copia de título/acta de grado notariada")
    handed_medical_cert = models.NullBooleanField(default=False, null=True, verbose_name="entregó certificado médico")
    medical_cert_img = models.ImageField(upload_to='medical_cert_img', null=True, blank=True,
                                         verbose_name="certificado médico")
    handed_birth_cert = models.NullBooleanField(default=False, null=True, verbose_name="entregó partida de nacimiento")
    birth_cert_img = models.ImageField(upload_to='birth_cert_img', null=True, blank=True,
                                       verbose_name="partida de nacimiento")
    disability = models.NullBooleanField(default=False, null=True, verbose_name="discapacidad")
    disability_percent = models.IntegerField(default=0, null=True, verbose_name="porcentaje de discapacidad")
    disability_id = models.CharField(max_length=20, null=True, blank=True, verbose_name="no. de carnet")
    ethnic_group = models.ForeignKey(EthnicGroup, null=True, related_name='ethnic_group', verbose_name="grupo étnico")
    email_confirmed = models.NullBooleanField(default=False, null=True, verbose_name="correo electrónico confirmado")

    def __unicode__(self):
        return "%s" % self.user


class Teacher(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'profesor'
        verbose_name_plural = 'profesores'
        managed = False

    CONTRACT_TYPE_CHOICES = (('TC', 'Tiempo Completo'),
                             ('TP', 'Tiempo Parcial'),
                             ('MT', 'Medio Tiempo'))

    user = models.ForeignKey(User, unique=True, verbose_name="usuario")
    institutional_email = models.EmailField(null=True, blank=True, verbose_name="correo institucional")
    academic_category = models.CharField(null=True, blank=True, max_length=30,
                                         verbose_name="categoría personal académico")
    contract_type = models.CharField(null=True, max_length=2, choices=CONTRACT_TYPE_CHOICES,
                                     verbose_name="tipo de contrato")
    academic_unity = models.CharField(null=True, max_length=30, blank=True, verbose_name="unidad académica")
    hours_to_pedagogy = models.IntegerField(null=True, blank=True, verbose_name="horas de pedagogía")
    hours_to_research = models.IntegerField(null=True, blank=True, verbose_name="horas de investigación")
    hours_to_society = models.IntegerField(null=True, blank=True, verbose_name="horas de vinculación con la comunidad")
    hours_to_other = models.IntegerField(null=True, blank=True, verbose_name="horas de otras actividades")
    other_activities = models.CharField(null=True, max_length=50, blank=True, verbose_name="otras actividades")
    studying = models.BooleanField(default=False, verbose_name="cursando estudios")

    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)


class Charge(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'cargo'
        managed = False

    nombre = models.CharField(max_length=30, verbose_name="nombre cargo")
    teacher = models.ForeignKey(User, verbose_name="persona")
    date_start_charge = models.TimeField(null=True, blank=True, verbose_name="fecha inicio cargo")
    date_end_charge = models.TimeField(null=True, blank=True, verbose_name="fecha fin cargo")
    no_doc_charge = models.IntegerField(null=True, blank=True, verbose_name="no. documento cargo")

    def __unicode__(self):
        return "%s" % self.nombre


class Career(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'carrera'
        managed = False

    name = models.CharField(max_length=100, unique=True, verbose_name="nombre")
    description = models.CharField(max_length=250, verbose_name="descripción")

    def __unicode__(self):
        return "%s" % self.name[:26]


class Course(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'curso'
        managed = False

    COURSE_TYPE_CHOICES = (('S', 'Semipresencial'),
                           ('P', 'Presencial'),
                           ('C', 'Educación Contínua'))

    career = models.ForeignKey(Career, null=True, blank=True, verbose_name="carrera")
    description = models.CharField(max_length=30, verbose_name="descripción")
    type = models.CharField(max_length=1, choices=COURSE_TYPE_CHOICES, verbose_name="modalidad de ingreso")
    period = models.ForeignKey(Period, verbose_name="período")
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, verbose_name="semestre")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="nivel")
    parallel = models.CharField(max_length=1, choices=PARALLEL_CHOICES, verbose_name="paralelo")
    max_quota = models.IntegerField(verbose_name="cantidad máxima de alumnos")

    payment_reg = models.FloatField(verbose_name="costo matrícula ordinaria")
    payment_ext = models.FloatField(verbose_name="costo matrícula extraordinaria")
    payment_esp = models.FloatField(verbose_name="costo matrícula especial")

    amount_payments = models.IntegerField(verbose_name="cantidad de pagos")
    value_payments = models.FloatField(verbose_name="valor de pagos")
    applied_scholarship_from = models.IntegerField(verbose_name="beca aplicada a partir de")

    def quota_payout(self):
        return Enrollment.objects.filter(course=self, student__live=True, live=True, payment_order__payout=True).count()

    def quota(self):
        return Enrollment.objects.filter(course=self, student__live=True, live=True).count()

    def __unicode__(self):
        if self.type != "C":
            if self.level == 7:
                return "%s-%s: %s-%s-%s" % (self.period, self.semester, self.career, "UTE", self.parallel)
            if self.level == 0:
                return "%s-%s: %s-%s-%s" % (self.period, self.semester, self.career, "PRE", self.parallel)
            if self.level == 12:
                return "%s-%s: %s-%s-%s" % (self.period, self.semester, self.career, "CE", self.parallel)
            return "%s-%s: %s-%s-%s" % (self.period, self.semester, self.career, toRoman(self.level), self.parallel)
        else:
            return "%s-%s: %s-%s-%s" % (
                self.period, self.semester, self.description[:20], toRoman(self.level), self.parallel)


class Matter(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'materia'
        managed = False

    career = models.ForeignKey(Career, verbose_name="carrera")
    description = models.CharField(max_length=30, verbose_name="descripción")
    period = models.ForeignKey(Period, verbose_name="período")
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, verbose_name="semestre")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="nivel")
    parallel = models.CharField(max_length=1, choices=PARALLEL_CHOICES, verbose_name="paralelo")
    credit = models.IntegerField(verbose_name="créditos")

    def __unicode__(self):
        return "%s" % self.description


class Studies(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'estudio'
        managed = False

    teacher = models.ForeignKey(Teacher, verbose_name="profesor")
    academic_level = models.IntegerField(verbose_name="nivel académico")
    institute = models.CharField(max_length=50, verbose_name="institución")
    title = models.CharField(max_length=50, verbose_name="título")
    title_img = models.ImageField(null=True, blank=True, upload_to='title_img', verbose_name="título escaneado")
    date_award = models.DateField(verbose_name="fecha de obtención")
    country = models.ForeignKey(Country, verbose_name="país")
    senescyt_id = models.CharField(max_length=200, blank=True, verbose_name="registo del SENESCYT")

    def __unicode__(self):
        return "%s - %s" % (self.teacher, self.title)


class Student(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'estudiante'
        managed = False

    INCOME_SYS_CHOICES = (('NIV', 'Curso de Nivelación'),
                          ('HOM', 'Homologación'),
                          ('SEN', 'SENESCYT'),
                          ('SNN', 'SNNA'),
                          ('OTR', 'Otros'),)

    STUDENT_TYPE_CHOICES = (('PRE', 'Pre-Tecnológico'),
                            ('EST', 'Estudiando'),
                            ('EGR', 'Egresado'),
                            ('TIT', 'Titulado'),
                            ('BAJ', 'Baja'),
                            ('ENE', 'ENES'),
                            ('SBA', 'Ser Bachiller'),
                            ('CON', 'Educación Continua'))

    user = models.ForeignKey(User, unique=True, verbose_name="usuario")
    career = models.ForeignKey(Career, null=True, blank=True, verbose_name="carrera")

    # Work Info
    working = models.NullBooleanField(default=False, null=True, verbose_name="trabaja")
    company_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="nombre de la empresa")
    company_address = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección de la empresa")
    charge = models.CharField(max_length=50, null=True, blank=True, verbose_name="cargo")
    work_telephone = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono del trabajo")
    work_email = models.EmailField(null=True, blank=True, verbose_name="correo electrónico del trabajo")
    type = models.CharField(null=True, max_length=3, choices=STUDENT_TYPE_CHOICES, verbose_name="tipo")
    # Academic Info
    campus_orig = models.CharField(null=True, max_length=50, verbose_name="plantel de procedencia")
    campus_city = models.CharField(null=True, max_length=50, verbose_name="ciudad")
    specialization = models.CharField(null=True, max_length=50, verbose_name="especialización")
    language_know_lvl = models.CharField(null=True, max_length=1, choices=QUALITATIVE_LEVEL_CHOICES,
                                         verbose_name="nivel de conocimiento en idioma Inglés")
    informatic_know_lvl = models.CharField(null=True, max_length=1, choices=QUALITATIVE_LEVEL_CHOICES,
                                           verbose_name="nivel de conocimiento en informática")

    income_sys = models.CharField(null=True, max_length=3, choices=INCOME_SYS_CHOICES,
                                  verbose_name="sistema de ingreso")
    first_time_ingress = models.DateField(null=True, blank=True, verbose_name="fecha de ingreso por primera vez")
    decline = models.NullBooleanField(null=True, default=False, verbose_name="baja")
    cohort_period = models.ForeignKey(Period, null=True, blank=True, verbose_name="cohorte (período)")
    cohort_semester = models.CharField(null=True, blank=True, max_length=1, choices=SEMESTER_CHOICES,
                                       verbose_name="cohorte (semestre)")
    date_graduation = models.DateField(null=True, blank=True, verbose_name="fecha de egreso")
    date_thesis_defense = models.DateField(null=True, blank=True,
                                           verbose_name="fecha de discusión del trabajo de graduación")
    act_number = models.IntegerField(null=True, blank=True, verbose_name="número de acta")
    senescyt_number = models.IntegerField(null=True, blank=True, verbose_name="número de registro senescyt")
    approved = models.NullBooleanField(verbose_name="datos aprobados")

    events_groups = models.ManyToManyField("EventsGroup", through='StudentEventsGroupRelation',
                                           verbose_name="grupos de eventos")
    motivo_elimina = models.TextField(max_length=200, null=True, blank=True, verbose_name="Motivo de Eliminacion")

    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)

    def isStudentEnabled(self):
        return self.modified_by is not None


class StudentEventsGroupRelation(TimeStampedModel, AuthStampedModel):
    class Meta:
        auto_created = False
        managed = False

    student = models.ForeignKey(Student)
    event_group = models.ForeignKey("EventsGroup")
    order = models.IntegerField(null=True, blank=True, verbose_name="orden")


class StudentNotes(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'notas sobre estudiante'
        managed = False

    student = models.ForeignKey(Student, related_name='notes', verbose_name="estudiante")
    note = models.TextField(verbose_name="nota")

    def __unicode__(self):
        return "%s" % self.user


class EventType(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'tipo de evento'
        verbose_name_plural = 'tipos de eventos'
        managed = False

    EVENT_STUDENT_TYPE_CHOICES = (('TOD', 'Todos'),
                                  ('PRE', 'Pre-Tecnológico'),
                                  ('EST', 'Estudiando'),
                                  ('EGR', 'Egresado'),
                                  ('TIT', 'Titulado'),
                                  ('BAJ', 'Baja'),
                                  ('ENE', 'ENES'),
                                  ('SBA', 'Ser Bachiller'),
                                  ('CON', 'Educación Continua'))

    name = models.CharField(max_length=50, verbose_name="nombre")
    description = models.TextField(verbose_name="descripción")
    student_type = models.CharField(null=True, max_length=3, choices=EVENT_STUDENT_TYPE_CHOICES,
                                    verbose_name="tipo de estudiante")

    def __unicode__(self):
        return "%s" % self.name


class EventsGroup(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'grupo de tipos de evento'
        verbose_name_plural = 'grupos de tipos de evento'
        managed = False

    name = models.CharField(max_length=50, verbose_name="nombre")
    description = models.TextField(verbose_name="descripción")
    student_type = models.CharField(null=True, max_length=3, choices=Student.STUDENT_TYPE_CHOICES,
                                    verbose_name="tipo de estudiante")
    events = models.ManyToManyField(EventType, through='EventsGroupRelation', verbose_name="eventos")

    def __unicode__(self):
        return "%s" % self.name


class EventsGroupRelation(TimeStampedModel, AuthStampedModel):
    class Meta:
        auto_created = False
        managed = False

    event_type = models.ForeignKey(EventType)
    event_group = models.ForeignKey(EventsGroup)
    order = models.IntegerField(null=True, blank=True, verbose_name="orden")


class StudentEvent(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'evento de estudiante'
        managed = False

    EVENT_STATE_CHOICES = (('ESP', 'En Espera'),
                           ('ENC', 'En Curso'),
                           ('ABO', 'Abortada'),
                           ('CON', 'Concluida'))

    type = models.ForeignKey(EventType, verbose_name="tipo de evento")
    student = models.ForeignKey(Student, verbose_name="estudiante")
    start_date = models.DateField(null=True, verbose_name="fecha de inicio")
    end_date = models.DateField(null=True, verbose_name="fecha de finalización")
    ini_obs = models.TextField(null=True, blank=True, verbose_name="observaciones iniciales")
    end_obs = models.TextField(null=True, blank=True, verbose_name="observaciones finales")
    tutor = models.ForeignKey(Teacher, null=True, blank=True, verbose_name="tutor/supervisor")
    manager = models.ForeignKey(User, null=True, verbose_name="administrativo")
    state = models.CharField(max_length=3, choices=EVENT_STATE_CHOICES, verbose_name="estado")

    def __unicode__(self):
        return "%s: %s" % (self.type, self.student)


class BugReport(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'reporte de error'
        managed = False

    GRAVITY_CHOICES = (('H', 'Alta'),
                       ('M', 'Media'),
                       ('L', 'Baja'))

    STATE_CHOICES = (('R', 'Reportado'),
                     ('A', 'Aceptado'),
                     ('S', 'Solucionado'),
                     ('C', 'Cerrado'))

    gravity = models.CharField(max_length=3, choices=GRAVITY_CHOICES, verbose_name="gravedad")
    name = models.CharField(max_length=50, verbose_name="nombre")
    description = models.TextField(verbose_name="descripción")
    snapshot = models.ImageField(upload_to='bugs', null=True, blank=True, verbose_name="instantánea")
    state = models.CharField(max_length=1, choices=STATE_CHOICES, verbose_name="estado")


class Enrollment(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'matrícula'
        managed = False

    ENROLLMENT_CHOICES = (('ORD', 'Ordinaria'),
                          ('EXT', 'Extraordinaria'),
                          ('ESP', 'Especial'),
                          ('PRE', 'Pre-Tecnológico'),
                          ('ENE', 'ENES'),
                          ('SBA', 'Ser Bachiller'),
                          ('ECO', 'Educación Continua'))

    FINANCING_SYS_CHOICES = (('DIRE', 'Crédito Directo'),
                             ('IECE', 'Crédito IECE'))

    CONDITION_CHOICES = (('R', 'Regular'),
                         ('C', 'Caso Especial'),
                         ('H', 'Homologado'))

    student = models.ForeignKey(Student, verbose_name="estudiante")
    course = models.ForeignKey(Course, verbose_name="curso")
    type = models.CharField(max_length=3, choices=ENROLLMENT_CHOICES, verbose_name="tipo de matrícula")
    date = models.DateField(verbose_name="fecha de matrícula")
    financing_sys = models.CharField(max_length=4, choices=FINANCING_SYS_CHOICES,
                                     verbose_name="sistema de financiamiento")
    condition = models.CharField(max_length=1, choices=CONDITION_CHOICES, verbose_name="condición")
    scholarship = models.IntegerField(default=0, verbose_name="porcentaje de beca")
    payment_order = models.ForeignKey("PaymentOrder", null=True, blank=True, related_name='payment_order',
                                      on_delete=CASCADE, verbose_name="orden de pago")

    def __unicode__(self):
        return "%s : %s" % (self.student, self.course)


class PaymentOrder(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'Orden de Pago'
        managed = False

    PAYMENT_CONCEPT_CHOICES = (('MORD', 'Matrícula Ordinaria'),
                               ('MEXT', 'Matrícula Extraordinaria'),
                               ('MESP', 'Matrícula Especial'),
                               ('TASI', 'Toma de Asignatura'),
                               ('ESUF', 'Examen de Suficiencia'),
                               ('CNOT', 'Certificado de Notas'),
                               ('HOMO', 'Homologación'),
                               ('REVA', 'Revalidación'),
                               ('CMAT', 'Certificado de Materias (Plan de Estudios)'),
                               ('SBAC', 'Curso de Nivelación (Ser Bachiller)'),
                               ('ENES', 'Curso de Nivelación (ENES)'),
                               ('PRET', 'Curso de Nivelación (AITEC)'),
                               ('EDCO', 'Curso de Educación Continua'),
                               ('EPER', 'Período Académico Extraordinario'),
                               ('UNTE', 'Unidad de Titulación Especial'),
                               ('PGRA', 'Proceso de Graduación'),
                               ('QUOT', 'Cuota'),)

    user = models.ForeignKey(User, verbose_name="usuario")
    date_issue = models.DateField(verbose_name="fecha de emisión")
    payout = models.BooleanField(default=False, verbose_name="pagado")
    date_payment = models.DateField(null=True, blank=True, verbose_name="fecha de pago")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="nivel")
    period = models.ForeignKey(Period, verbose_name="período")
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, verbose_name="semestre")
    value = models.FloatField(verbose_name="valor a pagar")
    payment_concept = models.CharField(max_length=4, choices=PAYMENT_CONCEPT_CHOICES, verbose_name="concepto de pago")
    number = models.IntegerField(default=0, verbose_name="número")
    enrollment = models.ForeignKey(Enrollment, null=True, blank=True, related_name='payment_related',
                                   verbose_name="matricula")

    def __unicode__(self):
        return "%s %s: %s" % (self.date_issue, self.user, self.get_payment_concept_display())


class EmailLog(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'registro de mensaje'
        managed = False

    sender = models.ForeignKey(User, verbose_name="remitente")
    to = models.ManyToManyField(User, related_name="emails_to", verbose_name="para")
    cc = models.ManyToManyField(User, related_name="emails_cc", verbose_name="copia")
    cco = models.ManyToManyField(User, related_name="emails_cco", verbose_name="copia oculta")
    subject = models.CharField(max_length=255, verbose_name="asunto")
    body = models.TextField(verbose_name="cuerpo")
    send_success = models.BooleanField(default=False, verbose_name="enviado exitosamente")
    send_date = models.DateTimeField(verbose_name="fecha de envío")

    def __unicode__(self):
        return "%s %s: %s" % (self.sender, self.to, self.subject)


class Contact(LiveModel, TimeStampedModel, AuthStampedModel):
    class Meta:
        verbose_name = 'Contacto'
        managed = False

    user = models.ForeignKey(User, verbose_name="usuario")
    first_name = models.CharField(max_length=30, verbose_name="nombre")
    last_name = models.CharField(max_length=30, verbose_name="apellidos")
    id_doc_num = models.CharField(max_length=30, verbose_name="Cédula/RUC")
    email = models.EmailField(blank=True, null=True, verbose_name="correo electrónico")
    address = models.TextField(null=True, verbose_name="dirección personal")
    telephone = models.CharField(max_length=30, null=True, blank=True, verbose_name="teléfono")
    cellphone = models.CharField(max_length=30, null=True, blank=True, verbose_name="celular")


########################################################################################################################
#
# Arturo Medic class
#
class SigiaMedicFamilyBackgroundDetail(LiveModel, TimeStampedModel, AuthStampedModel):
    detail = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sigia_medic_family_background_detail'

    def __unicode__(self):
        return "%s" % self.detail


class SigiaMedicPersonalBackgroundDetail(LiveModel, TimeStampedModel, AuthStampedModel):
    detail = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True, default='0')

    class Meta:
        managed = True
        db_table = 'sigia_medic_personal_background_detail'

    def __unicode__(self):
        return "%s" % self.detail


class SigiaMedicrecord(LiveModel, TimeStampedModel, AuthStampedModel):
    id_patient = models.ForeignKey(User, models.DO_NOTHING, db_column='id_patient', blank=False, null=False)
    blood_type_by = models.IntegerField(blank=True, null=True, verbose_name="Tipo de sangre")
    blood_type = models.CharField(max_length=4, blank=True, null=True, verbose_name="Grupo sanguíneo")
    form_arrival = models.CharField(max_length=40, blank=False, null=False, verbose_name="Forma de llegada")
    source_information = models.CharField(max_length=40, blank=False, null=False)
    delivery_patient = models.CharField(max_length=40, blank=False, null=False)
    phone_delivery = models.CharField(max_length=12, blank=False, null=False)
    actual_problem = models.CharField(max_length=1000, default="Campo sin usar", verbose_name="Detalle")
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False,
                                         verbose_name="Presión arterial")
    heart_rate = models.IntegerField(blank=False, null=False, verbose_name="Frecuencia cardiaca")
    breathing_frequency = models.IntegerField(blank=False, null=False, verbose_name="Frecuencia respiratoria")
    oral_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False,
                                           verbose_name="Temperatural Bucal")
    asolar_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False,
                                             verbose_name="Temperatura Asolar")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, verbose_name="Peso")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, verbose_name="Talla")
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, verbose_name="I.M.C.")
    p_cephalico = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="P. Cefalico")
    date = models.DateTimeField(null=True, verbose_name="fecha de consulta")

    class Meta:
        managed = True
        db_table = 'sigia_medic_record'


class SigiaMedicConsulta(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicrecord, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="medic_consulta")
    actual_problem = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Detalle")

    class Meta:
        managed = True
        verbose_name = "Consultas Paciente"
        db_table = 'sigia_medical_consulta'


class SigiaMedicPersonalBackground(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicrecord, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="personal_background")
    type_background = models.ForeignKey(SigiaMedicPersonalBackgroundDetail, models.DO_NOTHING,
                                        db_column='type_background', blank=False, null=False)
    detail_background = models.CharField(max_length=200, blank=True, null=True, verbose_name="Detalle")

    class Meta:
        managed = True
        db_table = 'sigia_medic_personal_background'

    def __unicode__(self):
        return "%s" % self.type_background.detail


class SigiaMedicFamilyBackground(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicrecord, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="family_background")
    type_background = models.ForeignKey(SigiaMedicFamilyBackgroundDetail, models.DO_NOTHING,
                                        db_column='type_background', blank=False, null=False)
    detail_background = models.CharField(max_length=200, blank=True, null=True, verbose_name="Detalle")

    class Meta:
        managed = True
        db_table = 'sigia_medic_family_background'


class SigiaMedicContact(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicrecord, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="medic_contact")
    relationship_type = models.CharField(max_length=40, blank=False, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sigia_medic_contact'


class SigiaMedicPhysicalExamDetail(LiveModel, TimeStampedModel, AuthStampedModel):
    detail = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True, default='0')

    class Meta:
        managed = True
        db_table = 'sigia_medic_physical_detail'

    def __unicode__(self):
        return "%s" % self.detail


class SigiaMedicPhysicalExam(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicConsulta, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="physical_exam")
    type_background = models.ForeignKey(SigiaMedicPhysicalExamDetail, models.DO_NOTHING,
                                        db_column='type_background', blank=False, null=False)
    detail_background = models.CharField(max_length=200, blank=True, null=True, verbose_name="Detalle")
    typed = models.CharField(max_length=10, blank=False, null=False, verbose_name="Tipo", db_column='type')
    cp = models.BooleanField(default=False, verbose_name="Con evidencia de patología")
    sp = models.BooleanField(default=False, verbose_name="Sin evidencia de patología")

    class Meta:
        managed = True
        db_table = 'sigia_medic_physical'


class SigiaMedicDiagnosticPlanDetail(LiveModel, TimeStampedModel, AuthStampedModel):
    detail = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True, default='0')

    class Meta:
        managed = True
        db_table = 'sigia_medic_diagnostic_plan_detail'

    def __unicode__(self):
        return "%s" % self.detail


class SigiaMedicDiagnosticPlan(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicConsulta, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="diagnostic_plan")
    type_background = models.ForeignKey(SigiaMedicDiagnosticPlanDetail, models.DO_NOTHING,
                                        db_column='type_background', blank=False, null=False)
    detail_background = models.CharField(max_length=200, blank=False, null=False, verbose_name="Detalle")

    class Meta:
        managed = True
        db_table = 'sigia_medic_diagnostic_plan'


class SigiaMedicCie10(LiveModel, TimeStampedModel, AuthStampedModel):
    id = models.CharField(max_length=10, primary_key=True)
    detail = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sigia_medic_cie10'


class SigiaMedicDiagnosticPresumptive(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicConsulta, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="diagnostic_presumptive")
    detail_background = models.CharField(max_length=200, blank=False, null=False, verbose_name="Detalle")
    cie = models.ForeignKey(SigiaMedicCie10, models.DO_NOTHING, db_column="cie", verbose_name="CIE-10")

    class Meta:
        managed = True
        db_table = 'sigia_medic_diagnostic_presumptive'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/medicCenter_<id>/<filename>
    return 'medicCenter_{0}/{1}'.format(instance.id, filename)


class SigiaMedicalCenter(LiveModel, TimeStampedModel, AuthStampedModel):
    centerName = models.CharField(max_length=200, blank=True, null=True, verbose_name="Centro Médico")
    id_medic = models.ForeignKey(User, models.DO_NOTHING, db_column='id_medic', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección")
    phone_number = models.CharField(max_length=12, blank=True, null=True, verbose_name="Teléfono")
    report_image = models.ImageField(null=True, upload_to=user_directory_path,
                                     default='institution_logos/anonymous.jpg',
                                     verbose_name="logo")

    class Meta:
        managed = True
        verbose_name = "Centro medico"
        db_table = 'sigia_medical_center'


class SigiaMedicAppointment(LiveModel, TimeStampedModel, AuthStampedModel):
    id_patient = models.ForeignKey(User, models.DO_NOTHING, db_column='id_patient', blank=False, null=False)
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción")
    date = models.DateTimeField(null=True, verbose_name="fecha de consulta")
    done = models.BooleanField(default=False, verbose_name="Realizada")

    class Meta:
        managed = True
        verbose_name = "Cita medica"
        db_table = 'sigia_medical_appointment'


class SigiaMedicPrescription(LiveModel, TimeStampedModel, AuthStampedModel):
    id_sigia_medic_record = models.ForeignKey(SigiaMedicConsulta, models.DO_NOTHING, db_column='id_sigiamedicrecord',
                                              related_name="receta_medicas")
    active_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Principio Activo")
    detail_background = models.CharField(max_length=200, blank=False, null=False, verbose_name="Prescripción",
                                         db_column='prescription', )
    quantity = models.IntegerField(blank=True, null=True, verbose_name="Cantidad")

    class Meta:
        managed = True
        verbose_name = "Receta medica"
        db_table = 'sigia_medic_prescription'
