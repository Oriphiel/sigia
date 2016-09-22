# -*- coding: utf-8 -*-

"""
Created on: 13/12/2014
@autor: Dario
"""
import os

from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory

from sigia.models import UserProfile, Teacher, Career, Course, Matter, Studies, \
    Student, Enrollment, Period, PaymentOrder, SEMESTER_CHOICES, Country, \
    EthnicGroup, BugReport, Province, Canton, Parish, Contact, EventType, \
    StudentEvent, EventsGroup, Institution, SigiaMedicContact, SigiaMedicFamilyBackground, \
    SigiaMedicFamilyBackgroundDetail, SigiaMedicPersonalBackground, SigiaMedicPersonalBackgroundDetail, \
    SigiaMedicrecord, \
    SigiaMedicPhysicalExam, SigiaMedicPhysicalExamDetail, SigiaMedicDiagnosticPlan, SigiaMedicDiagnosticPlanDetail, \
    SigiaMedicDiagnosticPresumptive, SigiaMedicCie10, SigiaMedicalCenter, SigiaMedicAppointment
from django.contrib.auth.models import User, Group
from captcha.fields import CaptchaField
from django.forms.widgets import TextInput, EmailInput, \
    Select, CheckboxInput, Textarea, NumberInput, DateInput, SelectMultiple, RadioSelect, DateTimeInput
from django.forms.models import ModelChoiceField
from floppyforms import ClearableFileInput
from sigia.utils import cedula_valida
import json


class ImageThumbnailFileInput(ClearableFileInput):
    template_name = 'includes/image_thumbnail.djhtml'


class EmailForm(forms.Form):
    to = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), label='Para')
    cc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}), required=False,
                         label='Copia')
    cco = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}), required=False,
                          label='Copia Oculta')
    to_ids = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False,
                             label='Para (ids)')
    cc_ids = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}), required=False,
                             label='Copia (ids)')
    cco_ids = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}), required=False,
                              label='Copia Oculta (ids)')
    subject = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}), label='Asunto')
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 15}), label='Cuerpo')


class LoginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), max_length=30, label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }), label='Contraseña')
    not_expire = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control', }), required=False,
                                    label='No caduca la sesión')


class ReducedStudentForm(forms.Form):
    GENDER_CHOICES = (('M', 'Masculino'),
                      ('F', 'Femenino'))

    STUDENT_TYPE_CHOICES = (('ENE', 'ENES'),
                            ('SBA', 'Ser Bachiller'),
                            ('CON', 'Educación Continua'))

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Usuario')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Nombres')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Apellidos')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', }), required=False, label='Email')
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), label='Dirección')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control', }),
                               label='Género')
    campus_orig = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }),
                                  label='Plantel de procedencia')
    specialization = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label='Especialización')
    cellphone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), required=False,
                                label='Celular')
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), required=False,
                                label='Teléfono')
    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', }), choices=STUDENT_TYPE_CHOICES,
                             required=True, label="Tipo")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Este campo es obligatorio.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con este identificador.")
        return username


class GenEnrollmentBookForm(forms.Form):
    period = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                    queryset=Period.objects.all(), label='Período')
    semester = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                 choices=SEMESTER_CHOICES, required=True, label="Semestre")


class NationalityModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.gentilicio


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s, %s" % (obj.last_name, obj.first_name)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'id_doc_num', 'email', 'address', 'telephone', 'cellphone']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', }),
            'last_name': TextInput(attrs={'class': 'form-control', }),
            'id_doc_num': TextInput(attrs={'class': 'form-control', }),
            'email': EmailInput(attrs={'class': 'form-control', }),
            'address': Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'telephone': TextInput(attrs={'class': 'form-control', }),
            'cellphone': TextInput(attrs={'class': 'form-control', })
        }


class EventGroupForm(forms.ModelForm):
    class Meta:
        model = EventsGroup
        fields = ['name', 'description', 'student_type', 'events']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'student_type': Select(attrs={'class': 'form-control', }),
        }


class UserPersonalInfoForm(forms.ModelForm):
    nationality = NationalityModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                              queryset=Country.objects.all(), label="Nacionalidad")
    birthplace_province = ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                           queryset=Province.objects.all())
    birthplace_canton = ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                         queryset=Canton.objects.all())
    birthplace_parish = ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                         queryset=Parish.objects.all())
    address_canton = ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                      queryset=Canton.objects.all())
    address_parish = ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                      queryset=Parish.objects.all())

    class Meta:
        model = UserProfile
        fields = ['photo', 'id_doc_type', 'id_doc_num', 'gender', 'birthday', 'nationality', 'birthplace_country',
                  'birthplace_province', 'birthplace_canton', 'birthplace_parish', 'marital_status', 'address',
                  'telephone', 'cellphone',
                  'address_province', 'address_canton', 'address_parish', 'id_doc_img', 'voting_cert_img',
                  'handed_degree_img', 'medical_cert_img', 'birth_cert_img',
                  'disability', 'disability_percent', 'disability_id', 'ethnic_group', 'handed_id_doc',
                  'handed_voting_cert', 'handed_degree', 'handed_medical_cert',
                  'handed_birth_cert']

        widgets = {
            'photo': ImageThumbnailFileInput(attrs={'style': 'width:100%', }),
            'id_doc_type': Select(attrs={'class': 'form-control', }),
            'id_doc_num': TextInput(attrs={'class': 'form-control', }),
            'gender': Select(attrs={'class': 'form-control', }),
            'birthday': DateInput(attrs={'class': 'form-control', }),
            'nationality': Select(attrs={'class': 'form-control', }),
            'birthplace_country': Select(attrs={'class': 'form-control', }),
            'birthplace_province': Select(attrs={'class': 'form-control', }),
            'birthplace_canton': Select(attrs={'class': 'form-control', }),
            'birthplace_parish': Select(attrs={'class': 'form-control', }),
            'address_province': Select(attrs={'class': 'form-control', }),
            'address_canton': Select(attrs={'class': 'form-control', }),
            'address_parish': Select(attrs={'class': 'form-control', }),
            'marital_status': Select(attrs={'class': 'form-control', }),
            'address': Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'telephone': TextInput(attrs={'class': 'form-control', }),
            'cellphone': TextInput(attrs={'class': 'form-control', }),

            'ethnic_group': Select(attrs={'class': 'form-control', }),

            'disability': CheckboxInput(attrs={'class': 'form-control', }),
            'disability_percent': NumberInput(attrs={'class': 'form-control', }),
            'disability_id': TextInput(attrs={'class': 'form-control', }),

            'handed_id_doc': CheckboxInput(attrs={'class': 'form-control', }),
            'id_doc_img': ImageThumbnailFileInput(attrs={'style': 'width:100%', }),
            'handed_voting_cert': CheckboxInput(attrs={'class': 'form-control', }),
            'voting_cert_img': ImageThumbnailFileInput(attrs={'style': 'width:100%', }),
            'handed_degree': CheckboxInput(attrs={'class': 'form-control', }),
            'handed_degree_img': ImageThumbnailFileInput(attrs={'style': 'width:100%', }),
            'handed_medical_cert': CheckboxInput(attrs={'class': 'form-control', }),
            'medical_cert_img': ImageThumbnailFileInput(attrs={'style': 'width:100%', }),
            'handed_birth_cert': CheckboxInput(attrs={'class': 'form-control', }),
            'birth_cert_img': ImageThumbnailFileInput(attrs={'style': 'width:100%', }),

        }

    def clean_id_doc_num(self):
        id_doc_type = self.cleaned_data['id_doc_type']
        id_doc_num = self.cleaned_data['id_doc_num']
        if id_doc_type == "C":
            if not cedula_valida(id_doc_num):
                raise forms.ValidationError("Cédula de identidad ecuatoriana inválida.")
        return id_doc_num

    def clean_id_doc_type(self):
        id_doc_type = self.cleaned_data['id_doc_type']
        if not id_doc_type:
            raise forms.ValidationError("Este campo es obligatorio.")
        return id_doc_type


class CaptchaForm(forms.Form):
    captcha = CaptchaField()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', }),
            'last_name': TextInput(attrs={'class': 'form-control', }),
            'username': TextInput(attrs={'class': 'form-control', }),
            'email': EmailInput(attrs={'class': 'form-control', }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError("Este campo es obligatorio.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError("Este campo es obligatorio.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Este campo es obligatorio.")
        return email


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['institutional_email', 'academic_category', 'contract_type', 'academic_unity', 'hours_to_pedagogy',
                  'hours_to_research', 'hours_to_society', 'hours_to_other', 'other_activities', 'studying']

        widgets = {
            'institutional_email': EmailInput(attrs={'class': 'form-control', }),
            'academic_category': TextInput(attrs={'class': 'form-control', }),
            'contract_type': Select(attrs={'class': 'form-control', }),
            'academic_unity': TextInput(attrs={'class': 'form-control', }),
            'hours_to_pedagogy': NumberInput(attrs={'class': 'form-control', }),
            'hours_to_research': NumberInput(attrs={'class': 'form-control', }),
            'hours_to_society': NumberInput(attrs={'class': 'form-control', }),
            'hours_to_other': NumberInput(attrs={'class': 'form-control', }),
            'other_activities': TextInput(attrs={'class': 'form-control', }),
            'studying': CheckboxInput(attrs={'class': 'form-control', }),
        }


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['name', 'description', 'student_type']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'description': Textarea(attrs={'class': 'form-control', }),
            'student_type': Select(attrs={'class': 'form-control', }),
        }


class StudentEventForm(forms.ModelForm):
    student = ModelChoiceField(label='Estudiante', widget=forms.Select(attrs={'class': 'form-control', }),
                               queryset=Student.objects.all().order_by("user__last_name", "user__first_name"))
    tutor = ModelChoiceField(label='Tutor/Supervisor', required=False,
                             widget=forms.Select(attrs={'class': 'form-control', }),
                             queryset=Teacher.objects.all().order_by("user__last_name", "user__first_name"))
    manager = UserModelChoiceField(label='Administrativo', widget=forms.Select(attrs={'class': 'form-control', }),
                                   queryset=Group.objects.get(name="secretary").user_set.all().
                                   order_by("last_name", "first_name"))

    class Meta:
        model = StudentEvent
        fields = ['type', 'student', 'start_date', 'end_date', 'end_date', 'ini_obs', 'tutor', 'manager']

        widgets = {
            'type': Select(attrs={'class': 'form-control', }),
            'student': Select(attrs={'class': 'form-control', }),
            'start_date': DateInput(attrs={'class': 'form-control', }),
            'end_date': DateInput(attrs={'class': 'form-control', }),
            'ini_obs': Textarea(attrs={'class': 'form-control', }),
            'tutor': Select(attrs={'class': 'form-control', }),
            'manager': Select(attrs={'class': 'form-control', }),
        }


class EthnicGroupForm(forms.ModelForm):
    class Meta:
        model = EthnicGroup
        fields = ['name', 'description']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'description': TextInput(attrs={'class': 'form-control', }),
        }


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ['name', 'description']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'description': TextInput(attrs={'class': 'form-control', }),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['career', 'description', 'type', 'period', 'semester', 'level', 'parallel', 'max_quota',
                  'payment_reg', 'payment_ext', 'payment_esp', 'amount_payments', 'value_payments',
                  'applied_scholarship_from']

        widgets = {
            'career': Select(attrs={'class': 'form-control', }),
            'description': TextInput(attrs={'class': 'form-control', }),
            'type': Select(attrs={'class': 'form-control', }),
            'period': Select(attrs={'class': 'form-control', }),
            'semester': Select(attrs={'class': 'form-control', }),
            'parallel': Select(attrs={'class': 'form-control', }),
            'level': Select(attrs={'class': 'form-control', }),
            'max_quota': TextInput(attrs={'class': 'form-control', }),
            'payment_reg': TextInput(attrs={'class': 'form-control', }),
            'payment_ext': TextInput(attrs={'class': 'form-control', }),
            'payment_esp': TextInput(attrs={'class': 'form-control', }),
            'amount_payments': NumberInput(attrs={'class': 'form-control', }),
            'value_payments': TextInput(attrs={'class': 'form-control', }),
            'applied_scholarship_from': NumberInput(attrs={'class': 'form-control', }),
        }


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'main', 'photo', 'logo', 'address', 'zip_address', 'ruc', 'active_semester', 'active_period',
                  'mission', 'vision', 'phone_one', 'phone_two']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'main': TextInput(attrs={'class': 'form-control', }),
            'photo': ImageThumbnailFileInput(attrs={'class': 'form-control', }),
            'logo': ImageThumbnailFileInput(attrs={'class': 'form-control', }),
            'address': TextInput(attrs={'class': 'form-control', }),
            'zip_address': TextInput(attrs={'class': 'form-control', }),
            'ruc': TextInput(attrs={'class': 'form-control', }),
            'active_semester': TextInput(attrs={'class': 'form-control', }),
            'active_period': TextInput(attrs={'class': 'form-control', }),
            'mission': TextInput(attrs={'class': 'form-control', }),
            'vision': TextInput(attrs={'class': 'form-control', }),
            'phone_one': TextInput(attrs={'class': 'form-control', }),
            'phone_two': TextInput(attrs={'class': 'form-control', }),
        }


class PeriodCreateForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['name', 'predecessor', 'start_notes']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'predecessor': Select(attrs={'class': 'form-control', }),
            'start_notes': TextInput(attrs={'class': 'form-control', }),
        }


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['name', 'gravity', 'description', 'snapshot']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'gravity': Select(attrs={'class': 'form-control', }),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'snapshot': ImageThumbnailFileInput(attrs={'style': 'width:100%', }),
        }


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'gentilicio', ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'gentilicio': TextInput(attrs={'class': 'form-control', }),
        }


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['name', 'country', ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'country': Select(attrs={'class': 'form-control', }),
        }


class CantonForm(forms.ModelForm):
    class Meta:
        model = Canton
        fields = ['name', 'province', ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'province': Select(attrs={'class': 'form-control', }),
        }


class ParishForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = ['name', 'canton', ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', }),
            'canton': Select(attrs={'class': 'form-control', }),
        }


class PaymentOrderForm(forms.ModelForm):
    user = UserModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                                queryset=User.objects.all().order_by("last_name", "first_name"))

    class Meta:
        model = PaymentOrder
        fields = ['user', 'date_issue', 'payout', 'date_payment', 'level', 'period', 'semester', 'value',
                  'payment_concept']

        widgets = {
            'user': Select(attrs={'class': 'form-control', }),
            'date_issue': TextInput(attrs={'class': 'form-control', }),
            'payout': CheckboxInput(attrs={'class': 'form-control', }),
            'date_payment': TextInput(attrs={'class': 'form-control', }),
            'level': Select(attrs={'class': 'form-control', }),
            'period': Select(attrs={'class': 'form-control', }),
            'semester': Select(attrs={'class': 'form-control', }),
            'value': TextInput(attrs={'class': 'form-control', }),
            'payment_concept': Select(attrs={'class': 'form-control', }),
        }


class MatterForm(forms.ModelForm):
    class Meta:
        model = Matter
        exclude = []


class StudiesForm(forms.ModelForm):
    class Meta:
        model = Studies
        fields = ['teacher', 'academic_level', 'institute', 'title', 'title_img',
                  'date_award', 'country', 'senescyt_id']

        widgets = {
            'teacher': Select(attrs={'class': 'form-control', }),
            'academic_level': NumberInput(attrs={'class': 'form-control', }),
            'institute': TextInput(attrs={'class': 'form-control', }),
            'title': TextInput(attrs={'class': 'form-control', }),
            'title_img': ImageThumbnailFileInput(attrs={'class': 'form-control', }),
            'date_award': DateInput(attrs={'class': 'form-control', }),
            'country': Select(attrs={'class': 'form-control', }),
            'senescyt_id': TextInput(attrs={'class': 'form-control', }),
        }


class StudentAcademicInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['career', 'campus_orig', 'campus_city', 'specialization', 'language_know_lvl',
                  'informatic_know_lvl', 'first_time_ingress', 'income_sys', 'type', 'cohort_period',
                  'cohort_semester', 'date_graduation', 'date_thesis_defense', 'act_number', 'senescyt_number']

        widgets = {
            'career': Select(attrs={'class': 'form-control', }),
            'campus_orig': TextInput(attrs={'class': 'form-control', }),
            'campus_city': TextInput(attrs={'class': 'form-control', }),
            'specialization': TextInput(attrs={'class': 'form-control', }),
            'language_know_lvl': Select(attrs={'class': 'form-control', }),
            'informatic_know_lvl': Select(attrs={'class': 'form-control', }),
            'first_time_ingress': DateInput(attrs={'class': 'form-control', }),
            'income_sys': Select(attrs={'class': 'form-control', }),
            'type': Select(attrs={'class': 'form-control', }),
            'cohort_period': Select(attrs={'class': 'form-control', }),
            'cohort_semester': Select(attrs={'class': 'form-control', }),
            'date_graduation': TextInput(attrs={'class': 'form-control', }),
            'date_thesis_defense': TextInput(attrs={'class': 'form-control', }),
            'act_number': TextInput(attrs={'class': 'form-control', }),
            'senescyt_number': TextInput(attrs={'class': 'form-control', }),
        }


class StudentWorkInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['working', 'company_name', 'company_address', 'charge', 'work_telephone', 'work_email']

        widgets = {
            'working': CheckboxInput(attrs={'class': 'form-control', }),
            'company_name': TextInput(attrs={'class': 'form-control', }),
            'company_address': Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'charge': TextInput(attrs={'class': 'form-control', }),
            'work_telephone': TextInput(attrs={'class': 'form-control', }),
            'work_email': EmailInput(attrs={'class': 'form-control', }),
        }

    def clean_company_name(self):
        working = self.cleaned_data['working']
        company_name = self.cleaned_data['company_name']
        if working:
            if not company_name:
                raise forms.ValidationError("Este campo es obligatorio.")
        return company_name

    def clean_company_address(self):
        working = self.cleaned_data['working']
        company_address = self.cleaned_data['company_address']
        if working:
            if not company_address:
                raise forms.ValidationError("Este campo es obligatorio.")
        return company_address

    def clean_charge(self):
        working = self.cleaned_data['charge']
        charge = self.cleaned_data['charge']
        if working:
            if not charge:
                raise forms.ValidationError("Este campo es obligatorio.")
        return charge


class CreateEnrollmentForm(forms.ModelForm):
    # period = ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control',}), queryset=Period.objects.all().order_by('name'))
    course = ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', }),
                              queryset=Course.objects.all().order_by('career', 'level'))

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'type', 'date', 'financing_sys', 'condition', 'scholarship']

        widgets = {
            'student': Select(attrs={'class': 'form-control', }),
            'course': Select(attrs={'class': 'form-control', }),
            'type': Select(attrs={'class': 'form-control', }),
            'date': Select(attrs={'class': 'form-control', }),
            'financing_sys': Select(attrs={'class': 'form-control', }),
            'condition': Select(attrs={'class': 'form-control', }),
            'scholarship': NumberInput(attrs={'class': 'form-control', }),
        }

    def clean_student(self):
        student_id = self.data['student']
        course_id = self.data['course']
        if not student_id:
            return student_id
        if not course_id:
            raise forms.ValidationError("Se debe seleccionar el curso para validar al estudiante.")
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        enrollment = Enrollment.objects.filter(student=student, course=course)
        if len(enrollment) > 0:
            raise forms.ValidationError("El estudiante seleccionado ya se encuentra matriculado en ese curso.")
        return student

    def clean_course(self):
        course = self.cleaned_data['course']
        student = Student.objects.get(id=self.data['student'])
        if course.quota() >= course.max_quota:
            raise forms.ValidationError("Ya el curso: %s está agotado." % course)
        if course.career != None and course.career != student.career:
            raise forms.ValidationError("El curso seleccionado no pertenece al programa del estudiante.")
        return course

    def clean_type(self):
        enrollment_type = self.data['type']
        if self.data['course'] and self.data['student']:
            course = Course.objects.get(id=self.data['course'])
            student = Student.objects.get(id=self.data['student'])
            if student.type == "PRE" and (course.level != 0 or enrollment_type != 'PRE'):
                raise forms.ValidationError(
                    "Los estudiantes de Pre-Tecnológico solo pueden ser matriculados con matrículas del tipo Pre-Tecnológico.")
            if student.type == "ENE" and (course.level != 8 or enrollment_type != 'ENE'):
                raise forms.ValidationError(
                    "Los estudiantes del ENES solo pueden ser matriculados con matrículas del tipo ENES.")
            if student.type == "SBA" and (course.level != 10 or enrollment_type != 'SBA'):
                raise forms.ValidationError(
                    "Los estudiantes de Ser Bachiller solo pueden ser matriculados con matrículas del tipo Ser Bachiller.")
            if student.type == "EST" and (course.level == 0 or course.level == 8 or course.level == 10 or
                                                  enrollment_type == 'PRE' or enrollment_type == 'SBA' or
                                                  enrollment_type == 'ENE'):
                raise forms.ValidationError(
                    "Los estudiantes regulares no se pueden matricular con una matrícula de ese tipo.")
            return enrollment_type
        else:
            raise forms.ValidationError(
                "Para validar el tipo de matrícula primero hay que seleccionar al estudiante y al curso.")


class UpdateEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'type', 'date', 'financing_sys', 'condition', 'scholarship']

        widgets = {
            'student': Select(attrs={'class': 'form-control', }),
            'course': Select(attrs={'class': 'form-control', }),
            'type': Select(attrs={'class': 'form-control', }),
            'date': Select(attrs={'class': 'form-control', }),
            'financing_sys': Select(attrs={'class': 'form-control', }),
            'condition': Select(attrs={'class': 'form-control', }),
            'scholarship': NumberInput(attrs={'class': 'form-control', }),
        }

    def clean_course(self):
        course = self.cleaned_data['course']
        student = Student.objects.get(id=self.data['student'])
        if course.career != student.career:
            raise forms.ValidationError("El curso seleccionado no pertenece al programa del estudiante.")
        return course


#######################################################
#
# Arturo Model Forms
#
class CreateMedicRecordForm(forms.ModelForm):
    id_patient = UserModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control selectpicker id_paciente', 'data-live-search': "true"}),
        queryset=Group.objects.get(name="paciente").user_set.filter(is_active=True).all().order_by("last_name",
                                                                                                   "first_name"),
        label="Paciente")

    class Meta:
        model = SigiaMedicrecord
        blood_type_by = (('1', 'IESS'),
                         ('2', 'OTRO'),)
        blood_type = (('A+', 'A+'),
                      ('A-', 'A-'),
                      ('B+', 'B+'),
                      ('B-', 'B-'),
                      ('AB+', 'AB+'),
                      ('AB-', 'AB-'),
                      ('O+', 'O+'),
                      ('O-', 'O-'),)
        form_arrival_choice = (('Ambulatorio', 'Ambulatorio'),
                               ('Silla de ruedas', 'Silla de ruedas'),
                               ('Camilla', 'Camilla'))
        exclude = []
        widgets = {
            'id_patient': Select(attrs={'class': 'form-control'}),
            'blood_type_by': Select(attrs={'class': 'form-control'}, choices=blood_type_by),
            'blood_type': Select(attrs={'class': 'form-control'}, choices=blood_type),
            'form_arrival': Select(attrs={'class': 'form-control'}, choices=form_arrival_choice),
            'source_information': TextInput(attrs={'class': 'form-control', 'placeholder': 'Fuente de información'}),
            'delivery_patient': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Institución o persona que entrega al paciente'}),
            'phone_delivery': TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'actual_problem': Textarea(attrs={'class': 'form-control', 'rows': '6',
                                              'placeholder': 'Cronología, Localización, Características, Intensidad, '
                                                             'Causas Aparentes, Factores que agravan o mejoran,'
                                                             'Síntomas asociados, Evolución, Medicamentos que reciben, '
                                                             'Resultados de Exámenes Anteriores, Condición actual'}),
            'blood_pressure': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'heart_rate': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'min'}),
            'breathing_frequency': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'min'}),
            'oral_temperature': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'C'}),
            'asolar_temperature': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'C'}),
            'weight': TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'KG', 'step': "0.01", 'min': '0'}),
            'height': TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'm', 'step': "0.01", 'min': '0'}),
            'imc': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'p_cephalico': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_id_patient(self):
        id_patient = self.cleaned_data['id_patient']
        if id_patient:
            return id_patient
        else:
            raise forms.ValidationError("Este campo es obligatorio")


class PersonalMedicBackground(forms.ModelForm):
    type_background = ModelChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-live-search': "true", 'autocomplete': 'off'}),
        queryset=SigiaMedicPersonalBackgroundDetail.objects.filter(id__range=[1, 24]), label="General")

    class Meta:
        model = SigiaMedicPersonalBackground
        exclude = ["id_sigia_medic_record", 'live']
        widgets = {
            'detail_background': Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'style': "resize: none", 'cols': '50',
                       'placeholder': 'Escriba el detalle...'}),
            'type_background': Select(attrs={'class': 'form-control'})
        }


class PersonalFemMedicBackground(forms.ModelForm):
    type_background = ModelChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-live-search': "true", 'autocomplete': 'off'}),
        queryset=SigiaMedicPersonalBackgroundDetail.objects.filter(id__range=[25, 41]), label="General Femenino")

    class Meta:
        model = SigiaMedicPersonalBackground
        exclude = ["id_sigia_medic_record", 'live']
        widgets = {
            'detail_background': Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'style': "resize: none", 'cols': '50',
                       'placeholder': 'Escriba el detalle...'}),
            'type_background': Select(attrs={'class': 'form-control'})
        }


class FamilyMedicBackground(forms.ModelForm):
    type_background = ModelChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-live-search': "true", 'autocomplete': 'off'}),
        queryset=SigiaMedicFamilyBackgroundDetail.objects.filter(id__range=[1, 11]), label="General")

    class Meta:
        model = SigiaMedicFamilyBackground
        exclude = ["id_sigia_medic_record", 'live']
        widgets = {
            'detail_background': Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'style': "resize: none", 'cols': '50',
                       'placeholder': 'Escriba el detalle...'}),
            'type_background': Select(attrs={'class': 'form-control'})
        }


class MedicContact(forms.ModelForm):
    class Meta:
        model = SigiaMedicContact
        exclude = ["id_sigia_medic_record", 'live']
        widgets = {
            'relationship_type': TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de relación'}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre persona'}),
            'phone_number': TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'})
        }

    def __init__(self, *arg, **kwarg):
        super(MedicContact, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


class PhysicalExam(forms.ModelForm):
    type_background = ModelChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-live-search': "true", 'autocomplete': 'off'}),
        queryset=SigiaMedicPhysicalExamDetail.objects.filter(id__range=[1, 25]), label="General")
    cp = forms.BooleanField(widget=RadioSelect(choices=[(True, 'Si'),
                                                        (False, 'No')]), label="Con evidencia de patología",
                            initial=False, required=False)
    sp = forms.BooleanField(widget=RadioSelect(choices=[(True, 'Si'),
                                                        (False, 'No')]), label="Sin evidencia de patología",
                            initial=False, required=False)

    class Meta:
        model = SigiaMedicPhysicalExam
        tipos = (('R', 'REGIONAL'),
                 ('S', 'SISTÉMICO'),)
        exclude = ["id_sigia_medic_record", 'live']
        widgets = {
            'detail_background': Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'style': "resize: none", 'cols': '50',
                       'placeholder': 'Escriba el detalle...'}),
            'typed': Select(attrs={'class': 'form-control'}, choices=tipos),
            'cp': Select(attrs={'class': 'form-control'}),
            'sp': Select(attrs={'class': 'form-control'}),
            'type_background': Select(attrs={'class': 'form-control'})
        }


class DiagnosticPlan(forms.ModelForm):
    type_background = ModelChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'data-live-search': "true", 'autocomplete': 'off'}),
        queryset=SigiaMedicDiagnosticPlanDetail.objects.filter(id__range=[1, 17]), label="General")

    class Meta:
        model = SigiaMedicDiagnosticPlan
        exclude = ["id_sigia_medic_record", 'live']
        widgets = {
            'detail_background': Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'style': "resize: none", 'cols': '50',
                       'placeholder': 'Escriba el detalle...'}),
            'type_background': Select(attrs={'class': 'form-control'})
        }


class DiagnosticPresumptive(forms.ModelForm):
    class Meta:
        model = SigiaMedicDiagnosticPresumptive
        exclude = ["id_sigia_medic_record", 'live']
        widgets = {
            'detail_background': TextInput(attrs={'class': 'form-control llenar', 'placeholder': 'Enfermedad'}),
            'cie': TextInput(
                attrs={'class': 'form-control cie10 autocomplete-me',
                       'placeholder': 'Escriba el CIE-10 o la enfermedad...'})
        }


class MedicalCenter(forms.ModelForm):
    class Meta:
        model = SigiaMedicalCenter
        exclude = ['live']
        widgets = {
            'report_image': ImageThumbnailFileInput(attrs={'class': 'form-control'})
        }


class PatientAppointment(forms.ModelForm):
    id_patient = UserModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control selectpicker id_paciente', 'data-live-search': "true"}),
        queryset=Group.objects.get(name="paciente").user_set.filter(is_active=True).all().order_by("last_name",
                                                                                                   "first_name"),
        label="Paciente")
    done = forms.BooleanField(widget=RadioSelect(choices=[(True, 'Si'),
                                                          (False, 'No')]), label="Cita realizada",
                              initial=False, required=False)

    class Meta:
        model = SigiaMedicAppointment
        exclude = ['live']
        widgets = {
            'id_patient': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': '2', 'style': "resize: none",
                                           'placeholder': 'Escriba una breve descripción de la cita'}),
            'date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'done': Select(attrs={'class': 'form-control'}),
        }


personal = inlineformset_factory(parent_model=SigiaMedicrecord, model=SigiaMedicPersonalBackground,
                                 form=PersonalMedicBackground, min_num=0, max_num=24, can_delete=True, can_order=True,
                                 validate_min=0, extra=1)
personal_fem = inlineformset_factory(parent_model=SigiaMedicrecord, model=SigiaMedicPersonalBackground,
                                     form=PersonalFemMedicBackground, min_num=0, max_num=24, can_delete=True,
                                     can_order=True, validate_min=0, extra=1)
family = inlineformset_factory(parent_model=SigiaMedicrecord, model=SigiaMedicFamilyBackground,
                               form=FamilyMedicBackground, min_num=0, max_num=11, can_delete=True, can_order=True,
                               validate_min=0, extra=1)
contacto = inlineformset_factory(parent_model=SigiaMedicrecord, model=SigiaMedicContact, form=MedicContact, min_num=0,
                                 max_num=5, can_delete=True, can_order=True, validate_min=0, extra=1)
fisico = inlineformset_factory(parent_model=SigiaMedicrecord, model=SigiaMedicPhysicalExam, form=PhysicalExam,
                               min_num=0, max_num=20, can_delete=True, can_order=True, validate_min=0, extra=1)
diagnostic = inlineformset_factory(parent_model=SigiaMedicrecord, model=SigiaMedicDiagnosticPlan, form=DiagnosticPlan,
                                   min_num=0, max_num=20, can_delete=True, can_order=True, validate_min=0, extra=1)
presumptive = inlineformset_factory(parent_model=SigiaMedicrecord, model=SigiaMedicDiagnosticPresumptive,
                                    form=DiagnosticPresumptive, min_num=0, max_num=20, can_delete=True, can_order=True,
                                    validate_min=0, extra=1)
