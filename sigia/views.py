# -*- coding: utf-8 -*-
"""
Created on 12/12/2014

@author: Dario
"""

from __future__ import unicode_literals

import locale

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.shortcuts import render
from django.views.generic import View
from django.core import serializers
from sigia.forms import LoginForm, UserForm, UserPersonalInfoForm, \
    StudentAcademicInfoForm, StudentWorkInfoForm, CareerForm, \
    CourseForm, CaptchaForm, PeriodCreateForm, PaymentOrderForm, \
    GenEnrollmentBookForm, UpdateEnrollmentForm, CreateEnrollmentForm, \
    EthnicGroupForm, BugReportForm, CountryForm, ProvinceForm, CantonForm, \
    ParishForm, ReducedStudentForm, ContactForm, TeacherForm, EventTypeForm, \
    StudentEventForm, StudiesForm, EventGroupForm, EmailForm, InstitutionForm, CreateMedicRecordForm, personal, \
    personal_fem, family, contacto, fisico, diagnostic, presumptive, PatientAppointment, ConsultaForm, prescription
from django.contrib.auth.models import Group
from django.views.generic.base import TemplateView
from sigia.models import Student, UserProfile, Career, Course, Enrollment, \
    Period, PaymentOrder, Province, Canton, Parish, EthnicGroup, BugReport, \
    Country, Teacher, EventType, StudentEvent, Studies, EventsGroup, \
    EventsGroupRelation, StudentEventsGroupRelation, EmailLog, Institution, SigiaMedicCie10, SigiaMedicrecord, \
    SigiaMedicPersonalBackground, SigiaMedicFamilyBackground, SigiaMedicContact, SigiaMedicPhysicalExam, \
    SigiaMedicDiagnosticPlan, SigiaMedicDiagnosticPresumptive, SigiaMedicAppointment, SigiaMedicConsulta, \
    SigiaMedicPrescription
from django.http.response import JsonResponse, HttpResponse, \
    HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json
from django.contrib.auth.decorators import login_required
from django.conf import settings
import base64
from sigia.utils import BreadCrumb, convert_enrrollment_type_to_payment_concept, \
    chunks, send_emails, control_save, control_save_update
from roman import fromRoman, toRoman
from django.db.models import Q
from django.views.decorators.gzip import gzip_page
import pytz
from django.db import connections
from django.core.mail import get_connection, EmailMultiAlternatives, \
    send_mass_mail
import re
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
import threading

empty_over_none = lambda x: x == None and '' or x

ecu_tz = pytz.timezone("America/Guayaquil")


def redirect_view(view_class, request):
    return view_class(request=request).get(request)


class RootView(TemplateView):
    title = 'SIGIA'
    template_name = 'base.djhtml'

    def get_context_data(self, **kwargs):
        context = super(RootView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class OnlineEnrollmentSuccessView(TemplateView):
    title = 'Registrado exitosamente'
    template_name = 'online_enrollment_success.djhtml'

    def get_context_data(self, **kwargs):
        context = super(OnlineEnrollmentSuccessView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class WelcomeView(TemplateView):
    title = 'Bienvenido'
    template_name = 'welcome.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"),)

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class ReportView(TemplateView):
    title = 'Reportes'
    template_name = 'reports.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Reportes", "/reports/"),)

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class SendEmailView(View):
    def get(self, request, *args, **kwargs):
        return "SIIIII"


class SendWelcomeEmailView(View):
    def get(self, request, *args, **kwargs):
        sigia = User.objects.get(username="sigia")
        subject = "Bienvenidos a SIGIA-AITEC."
        from_email = 'SIGIA-AITEC <sigia@aitec.edu.ec>'
        emails = []
        to = []

        for student in Student.objects.filter(career__isnull=False):
            try:
                enrollment = \
                    Enrollment.objects.filter(student=student, course__career=student.career).order_by('-date')[0]
                ctx = {
                    'user_full_name': "%s %s " % (student.user.first_name, student.user.last_name),
                    'course_full_name': enrollment.course
                }

                message = render_to_string('emails/welcome_student.djhtml', ctx)
                email = (subject, message, from_email, (student.user.email,))
                to.append(student.user)
                emails.append(email)
            except:
                pass

        log = EmailLog(sender=sigia, subject=subject, body=message, send_date=timezone.now(), send_success=True)
        log.to_set = to
        log.save()

        try:
            t = threading.Thread(target=send_emails,
                                 args=[emails, log])
            t.setDaemon(True)
            t.start()
        except Exception as ex:
            print ex

        return HttpResponse("OK")


class ReducedStudentCreateView(View):
    title = 'Estudiante Transitorio'
    form_class = ReducedStudentForm
    initial = {}
    template_name = 'reduced_student_form.djhtml'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ReducedStudentCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        student_form = self.form_class(prefix="student", initial=self.initial)
        contactForm = ContactForm(prefix="contact")
        context = {'student_form': student_form, 'contactForm': contactForm, 'title': self.title}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student_form = self.form_class(request.POST, prefix="student")
        contactForm = ContactForm(request.POST, prefix="contact")
        if not student_form.is_valid() or not contactForm.is_valid():
            message = 'Por favor corrija los errores en el formulario.'
            messages.add_message(request, messages.ERROR, message)
            context = {'student_form': student_form, 'contactForm': contactForm, 'title': self.title}
            return render_to_response(self.template_name, RequestContext(request, context))
        user = User()
        user.first_name = student_form.cleaned_data['first_name']
        user.last_name = student_form.cleaned_data['last_name']
        user.username = student_form.cleaned_data['username']
        email = student_form.cleaned_data['email']
        if not email:
            email = "noemail@nodomain.com"
        user.email = email
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.cellphone = student_form.cleaned_data['cellphone']
        profile.telephone = student_form.cleaned_data['telephone']
        profile.address = student_form.cleaned_data['address']
        profile.save()
        student = Student()
        student.user = user
        student.campus_orig = student_form.cleaned_data['campus_orig']
        student.specialization = student_form.cleaned_data['specialization']
        student.type = student_form.cleaned_data['type']
        student.approved = True
        student.save()

        contact = contactForm.save(commit=False)
        contact.user = user
        contact.save()

        message = 'Se ha creado correctamente al estudiante temporal %s %s.' % (user.first_name, user.last_name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(StudentsListView, request)


class LoginView(View):
    title = 'Iniciar Sesión'
    form_class = LoginForm
    initial = {}
    template_name = 'login.djhtml'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {'form': form, 'title': self.title}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            # no_expire = form.cleaned_data['not_expire']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/#/welcome/')
                else:
                    message = 'Su usuario ha sido desactivado, consulte a la secretaría docente.'
                    messages.add_message(request, messages.ERROR, message)
                    context = {'form': form, 'title': self.title}
                    return render_to_response(self.template_name, RequestContext(request, context))
            else:
                message = 'Usuario o contraseña inválidos.'
                messages.add_message(request, messages.ERROR, message)
                context = {'form': form, 'title': self.title}
                return render_to_response(self.template_name, RequestContext(request, context))

        message = 'Debe introducir un usuario y una contraseña válidas.'
        messages.add_message(request, messages.ERROR, message)
        context = {'form': form, 'title': self.title}
        return render_to_response(self.template_name, RequestContext(request, context))


class LogoutView(View):
    url_after_logout = '/#/welcome/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(self.url_after_logout)


class GetProvincesByCountry(View):
    def get(self, request, *args, **kwargs):
        country_id = kwargs['pk']
        array = []
        provinces = Province.objects.filter(country__id=country_id).order_by('id')
        for province in provinces:
            std = {'id': province.id,
                   'name': "%s" % province.name, }
            array.append(std)
        return JsonResponse(array, safe=False)


class GetCantonByProvince(View):
    def get(self, request, *args, **kwargs):
        province_id = kwargs['pk']
        array = []
        cantons = Canton.objects.filter(province__id=province_id).order_by('id')
        for canton in cantons:
            std = {'id': canton.id,
                   'name': "%s" % canton.name, }
            array.append(std)
        return JsonResponse(array, safe=False)


class GetParishByCanton(View):
    def get(self, request, *args, **kwargs):
        canton_id = kwargs['pk']
        array = []
        parishes = Parish.objects.filter(canton__id=canton_id).order_by('id')
        for parish in parishes:
            std = {'id': parish.id,
                   'name': "%s" % parish.name, }
            array.append(std)
        return JsonResponse(array, safe=False)


class CareerListView(TemplateView):
    title = 'Listado de Carreras'
    template_name = 'career_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Carreras", "/career/"),)

    def get_context_data(self, **kwargs):
        context = super(CareerListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class CareerListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        careers = Career.objects.all().order_by('id')
        for career in careers:
            std = {'id': career.id,
                   'name': "%s" % (career.name),
                   'description': career.description, }
            array.append(std)
        return JsonResponse(array, safe=False)


class CareerCreateView(View):
    title = 'Registrar Carrera'
    template_name = 'career_form.djhtml'
    action = 'CREATE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Carreras", "/career/"),
                         BreadCrumb("Nueva Carrera", "/career/new/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CareerCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        career_form = CareerForm()
        context = {'title': self.title, 'action': self.action, 'career_form': career_form,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        career_form = CareerForm(request.POST)

        if career_form.is_valid():
            career_form.save()
            message = 'Se ha añadido correctamente la carrera %s.' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CareerListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'career_form': career_form,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class CareerUpdateView(View):
    title = 'Actualizar Carrera'
    template_name = 'career_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Carreras", "/career/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CareerUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        career_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Carrera", "/career/%s/upgrade/" % career_id),)
        career = Career.objects.get(id=career_id)
        career_form = CareerForm(instance=career)
        context = {'title': self.title, 'action': self.action, 'career_form': career_form, 'career_id': career.id,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        career_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Carrera", "/career/%s/upgrade/" % career_id),)
        career = Career.objects.get(id=career_id)
        career_form = CareerForm(request.POST, instance=career)

        if career_form.is_valid():
            career_form.save()
            message = 'Se ha actualizado correctamente la carrera %s.' % career.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CareerListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'career_form': career_form, 'career_id': career.id,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class CareerDeleteView(View):
    redirect_url = '/career/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CareerDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_career = kwargs['pk']
        career = Career.objects.get(id=id_career)
        career_name = career.name
        career.delete()
        message = 'Se ha eliminado correctamente el curso: : %s.' % career_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(CareerListView, request)


class EmailBulkListView(View):
    title = 'Enviar Correos a Estudiantes'
    template_name = 'bulk_email.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Enviar Correos a Estudiantes", "/email/students/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EmailBulkListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        email_form = EmailForm()
        context = {'title': self.title, 'email_form': email_form, 'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        email_form = EmailForm(request.POST, request.FILES)
        pattern = '<(.*?)>'

        if email_form.is_valid():
            to_send = re.findall(pattern, email_form.cleaned_data["to"])
            emaillog = EmailLog(sender=request.user, subject=email_form.cleaned_data["subject"],
                                body=email_form.cleaned_data["body"])
            to_ids = [int(x) for x in email_form.cleaned_data["to_ids"].split(",")]
            to = [Student.objects.get(id=student_id).user for student_id in to_ids]
            emaillog.send_date = timezone.now()
            emaillog.save()
            emaillog.to.add(*to)
            emaillog.save()

            try:
                connection = get_connection()
                connection.open()

                html_content = emaillog.body
                soup = BeautifulSoup(html_content, "html5lib")
                text_content = soup.findAll(text=True)
                msg = EmailMultiAlternatives(emaillog.subject, text_content, 'SIGIA-AITEC<sigia@aitec.edu.ec>', to_send,
                                             connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                connection.close()
            except:
                emaillog.send_success = False
                message = 'El mensaje no se ha enviado.'
                messages.add_message(request, messages.ERROR, message)
                context = {'title': self.title, 'email_form': email_form, 'breadCrumbEntries': self.breadCrumbEntries}
                return render_to_response(self.template_name, RequestContext(request, context))

            emaillog.send_success = True
            emaillog.save()
            message = 'El mensaje se ha enviado exitosamente'
            messages.add_message(request, messages.SUCCESS, message)
        else:
            context = {'title': self.title, 'email_form': email_form, 'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))

        return redirect_view(StudentsListView, request)


class StudentsListView(TemplateView):
    title = 'Listado de Estudiantes'
    template_name = 'students_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Estudiantes", "/students/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentsListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(StudentsListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class UserUpdateView(View):
    title = 'Actualizar Perfil'
    template_name = 'userprofile_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(UserUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_user = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Perfil", "/user/%s/upgrade/" % id_user),)
        user = User.objects.get(id=id_user)
        profile = UserProfile.objects.get(user=user)

        user_form = UserForm(instance=user)
        personal_info_form = UserPersonalInfoForm(instance=profile)

        context = {'action': self.action, 'user_form': user_form, 'id_user': user.id,
                   'personal_info_form': personal_info_form,
                   'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries, }

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_user = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Perfil", "/user/%s/upgrade/" % id_user),)
        user = User.objects.get(id=id_user)
        profile = UserProfile.objects.get(user=user)

        user_form = UserForm(request.POST, instance=user)
        personal_info_form = UserPersonalInfoForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and personal_info_form.is_valid():
            user_form.save()
            personal_info_form.save()

            message = 'Se ha actualizado correctamente al estudiante %s %s.' % (user.first_name, user.last_name)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(WelcomeView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'user_form': user_form, 'user_id': user.id,
                       'personal_info_form': personal_info_form,
                       'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries, }

            return render_to_response(self.template_name, RequestContext(request, context))


class StudentsListData(View):
    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(t)))
        FROM (
            SELECT
                 
                 created_user."username" AS created_by,
                 modified_user."username" AS modified_by,
                 to_char("public"."sigia_student"."created", 'DD/MM/YY HH24:MI') AS created,
                 to_char("public"."sigia_student"."modified", 'DD/MM/YY HH24:MI') AS modified,
                 student_user."first_name" AS first_name,
                 student_user."last_name" AS last_name,
                 student_user.email,
                 "public"."sigia_student"."id",
                 "public"."sigia_career"."name" AS career,
                 "public"."sigia_student"."working",
                 "public"."sigia_student"."approved",
                 "public"."sigia_student"."type" AS student_type,
                 "public"."sigia_student"."campus_orig"
            FROM
                 "public"."auth_user" created_user RIGHT OUTER JOIN "public"."sigia_student" ON created_user."id" = "public"."sigia_student"."created_by_id"
                 LEFT OUTER JOIN "public"."auth_user" modified_user ON "public"."sigia_student"."modified_by_id" = modified_user."id"
                 LEFT OUTER JOIN "public"."auth_user" student_user ON "public"."sigia_student"."user_id" = student_user."id"
                 LEFT OUTER JOIN "public"."sigia_career" ON "public"."sigia_student"."career_id" = "public"."sigia_career"."id"
            WHERE
                 "public"."sigia_student"."live" = TRUE
            ORDER BY
                "public"."sigia_student"."id"
        ) t
        """)

        return JsonResponse(cursor.fetchall()[0][0], safe=False)


class TeachersAndAdminsListData(View):
    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(t)))
        FROM (
            SELECT 
                id, first_name, last_name, email
            FROM
                auth_user 
            WHERE
                auth_user.id NOT IN (SELECT user_id FROM sigia_student)
            ORDER BY
                last_name,
                first_name
        ) t
        """)

        return JsonResponse(cursor.fetchall()[0][0], safe=False)


class UserListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        users = User.objects.all().order_by('id')
        for user in users:
            std = {'id': user.id,
                   'last_name': "%s" % user.last_name,
                   'first_name': "%s" % user.first_name,
                   'email': user.email
                   }
            array.append(std)
        return JsonResponse(array, safe=False)


class StudentDeleteView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_student = kwargs['pk']
        motivo_elimina = request.POST['comenta']
        student = Student.objects.get(id=id_student)
        user = student.user
        student_name = "%s %s" % (user.first_name, user.last_name)
        student.motivo_elimina = motivo_elimina
        student.save()
        student.delete()
        profile = UserProfile.objects.get(user=user)
        profile.delete()
        user.is_active = False
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Se ha eliminado correctamente al usuario: %s.' % student_name)
        return redirect_view(StudentsListView, request)


class StudentUpdateView(View):
    title = 'Actualizar Estudiante'
    template_name = 'student_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Estudiantes", "/students/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_student = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Estudiante", "/students/%s/upgrade/" % id_student),)
        student = Student.objects.get(id=id_student)
        user = student.user
        profile = user.profile

        user_form = UserForm(instance=user)
        personal_info_form = UserPersonalInfoForm(instance=profile)
        academic_info_form = StudentAcademicInfoForm(instance=student)
        work_info_form = StudentWorkInfoForm(instance=student)

        context = {'action': self.action, 'user_form': user_form, 'id_student': student.id,
                   'personal_info_form': personal_info_form,
                   'academic_info_form': academic_info_form, 'work_info_form': work_info_form, 'title': self.title,
                   'student': student, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_student = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Estudiante", "/students/%s/upgrade/" % id_student),)
        student = Student.objects.get(id=id_student)
        user = student.user
        profile = user.profile

        user_form = UserForm(request.POST, instance=user)
        personal_info_form = UserPersonalInfoForm(request.POST, request.FILES, instance=profile)
        academic_info_form = StudentAcademicInfoForm(request.POST, instance=student)
        work_info_form = StudentWorkInfoForm(request.POST, instance=student)

        if user_form.is_valid() and personal_info_form.is_valid() and academic_info_form.is_valid() and work_info_form.is_valid():
            user_form.save()
            personal_info_form.save()
            academic_info = academic_info_form.save(commit=False)
            academic_info.approved = True
            academic_info.save()
            work_info_form.save()

            message = 'Se ha actualizado correctamente al estudiante %s %s.' % (user.first_name, user.last_name)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(StudentsListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'user_form': user_form, 'id_student': student.id,
                       'personal_info_form': personal_info_form,
                       'academic_info_form': academic_info_form, 'work_info_form': work_info_form, 'title': self.title,
                       'student': student, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))


class ReloadCaptchaView(View):
    def get(self, request, *args, **kwargs):
        to_json_response = dict()
        to_json_response['status'] = 0

        to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
        to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])

        return HttpResponse(json.dumps(to_json_response), content_type='application/json')


class StudentCreateView(View):
    title = 'Registrar Estudiante'
    template_name = 'student_form.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Estudiantes", "/students/"),
                         BreadCrumb("Registrar Estudiante", "/students/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        personal_info_form = UserPersonalInfoForm()
        academic_info_form = StudentAcademicInfoForm()
        work_info_form = StudentWorkInfoForm()
        captcha_form = CaptchaForm()
        context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                   'academic_info_form': academic_info_form, 'work_info_form': work_info_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}

        if not request.user.is_authenticated():
            captcha_form = CaptchaForm()
            context['captcha_form'] = captcha_form

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        personal_info_form = UserPersonalInfoForm(request.POST, request.FILES)
        academic_info_form = StudentAcademicInfoForm(request.POST)
        work_info_form = StudentWorkInfoForm(request.POST)
        captcha_form = CaptchaForm(request.POST)

        if user_form.is_valid() and personal_info_form.is_valid() \
                and academic_info_form.is_valid() and work_info_form.is_valid():
            if not request.user.is_authenticated():
                if not captcha_form.is_valid():
                    message = 'Corrija el captcha antes de enviar el formulario.'
                    messages.add_message(request, messages.ERROR, message)

                    context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                               'academic_info_form': academic_info_form, 'work_info_form': work_info_form,
                               'captcha_form': captcha_form, 'title': self.title,
                               'breadCrumbEntries': self.breadCrumbEntries}

                    return render_to_response(self.template_name, RequestContext(request, context))
            user = user_form.save()

            userprofile = personal_info_form.save(commit=False)
            userprofile.user = user

            academic_info = academic_info_form.save(commit=False)
            academic_info.user = user

            work_info = work_info_form.save(commit=False)
            academic_info.working = work_info.working
            academic_info.company_name = work_info.company_name
            academic_info.company_address = work_info.company_address
            academic_info.charge = work_info.charge
            academic_info.work_telephone = work_info.work_telephone
            academic_info.work_email = work_info.work_email

            if not request.user.is_authenticated():
                user.is_active = False
            else:
                user.is_active = True
            userprofile.live = True

            user.save()
            userprofile.save()
            academic_info.approved = True
            academic_info.save()

            if request.user.is_authenticated():
                message = 'Se ha añadido correctamente al estudiante %s %s.' % (user.first_name, user.last_name)
                messages.add_message(request, messages.SUCCESS, message)
                return redirect_view(StudentsListView, request)
            else:
                return redirect_view(OnlineEnrollmentSuccessView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                       'academic_info_form': academic_info_form, 'work_info_form': work_info_form,
                       'captcha_form': captcha_form, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

            return render_to_response(self.template_name, RequestContext(request, context))


class CourseListView(TemplateView):
    title = 'Listado de Cursos'
    template_name = 'course_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cursos", "/course/"),)

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class CourseListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        courses = Course.objects.all().order_by('id')
        for course in courses:
            level = ""
            if course.level > 0 and course.level < 7:
                level = toRoman(course.level)
            elif course.level == 7:
                level = "UTE"
            elif course.level == 0:
                level = "PRE"
            elif course.level == 12:
                level = "CE"
            std = {'id': course.id,
                   'career': "%s" % course.career,
                   'type': "%s" % course.get_type_display(),
                   'description': course.description,
                   'period': "%s" % course.period,
                   'semester': course.semester,
                   'level': level,
                   'parallel': course.parallel,
                   'quota': course.quota(),
                   'quota_payout': course.quota_payout(),
                   'max_quota': course.max_quota, }
            array.append(std)
        return JsonResponse(array, safe=False)


class CourseCreateView(View):
    title = 'Registrar Curso'
    template_name = 'course_form.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cursos", "/course/"),
                         BreadCrumb("Crear Curso", "/course/new/"),)
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CourseCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        course_form = CourseForm()
        context = {'action': self.action, 'course_form': course_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        course_form = CourseForm(request.POST)

        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.save()
            message = 'Se ha añadido correctamente el curso: %s-%s' % (request.POST['level'], request.POST['parallel'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CourseListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'course_form': course_form, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class CourseUpdateView(View):
    title = 'Actualizar Curso'
    template_name = 'course_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cursos", "/course/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CourseUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        course_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Curso", "/course/%s/upgrade/" % course_id),)
        course = Course.objects.get(id=course_id)
        course_form = CourseForm(instance=course)
        context = {'action': self.action, 'course_form': course_form, 'course_id': course.id, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        course_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Curso", "/course/%s/upgrade/" % course_id),)
        course = Course.objects.get(id=course_id)
        course_form = CourseForm(request.POST, instance=course)

        if course_form.is_valid():
            course_form.save()
            message = 'Se ha actualizado correctamente el curso: %s-%s' % (course.level, course.parallel)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CourseListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'course_form': course_form, 'course_id': course.id, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class CourseDeleteView(View):
    redirect_url = '/course/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CourseDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_course = kwargs['pk']
        course = Course.objects.get(id=id_course)
        course_name = "%s" % course
        course.delete()
        message = 'Se ha eliminado correctamente el curso: %s.' % course_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(CourseListView, request)


class EnrollmentListView(TemplateView):
    title = 'Listado de Matrículas'
    template_name = 'enrollment_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Matrículas", "/enrollment/"),)

    def get_context_data(self, **kwargs):
        context = super(EnrollmentListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id', None)
        if student_id:
            student = Student.objects.get(id=student_id)
            message = base64.b64encode(("""
                    $search = $("th[data-field='name'] input");
                    $search.val("%s, %s");
                    $search.trigger('keyup');
                    """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
            messages.add_message(request, settings.JS_MESSAGE, message)
        return super(EnrollmentListView, self).get(request, *args, **kwargs)


class EnrollmentListData(View):
    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(t)))
        FROM (
            SELECT
                 student_user.last_name||', '||student_user.first_name AS name,
                 to_char("public"."sigia_enrollment"."created",'DD/MM/YY HH24:MI') AS created,
                 to_char("public"."sigia_enrollment"."modified",'DD/MM/YY HH24:MI') AS modified,
                 "public"."sigia_enrollment"."id",
                 created_user."username" AS created_by,
                 modified_user."username" AS modified_by,
                 "public"."sigia_course"."semester",
                 "public"."sigia_course"."level",
                 "public"."sigia_course"."parallel",
                 "public"."sigia_career"."name" AS career,
                 "public"."sigia_period"."name" AS period,
                 "public"."sigia_enrollment"."date",
                 "public"."sigia_enrollment"."scholarship",
                 "public"."sigia_enrollment"."type",
                 "public"."sigia_enrollment"."financing_sys",
                 "public"."sigia_paymentorder"."payout"
            FROM
                 "public"."sigia_student" LEFT OUTER JOIN "public"."auth_user" student_user ON "public"."sigia_student"."user_id" = student_user."id"
                 RIGHT OUTER JOIN "public"."sigia_enrollment" ON "public"."sigia_student"."id" = "public"."sigia_enrollment"."student_id"
                 LEFT OUTER JOIN "public"."sigia_course" ON "public"."sigia_enrollment"."course_id" = "public"."sigia_course"."id"
                 LEFT OUTER JOIN "public"."auth_user" modified_user ON "public"."sigia_enrollment"."modified_by_id" = modified_user."id"
                 LEFT OUTER JOIN "public"."auth_user" created_user ON "public"."sigia_enrollment"."created_by_id" = created_user."id"
                 LEFT OUTER JOIN "public"."sigia_paymentorder" ON "public"."sigia_enrollment"."payment_order_id" = "public"."sigia_paymentorder"."id"
                 LEFT OUTER JOIN "public"."sigia_career" ON "public"."sigia_course"."career_id" = "public"."sigia_career"."id"
                 LEFT OUTER JOIN "public"."sigia_period" ON "public"."sigia_course"."period_id" = "public"."sigia_period"."id"
            WHERE
                 "public"."sigia_enrollment"."live" = TRUE
             AND "public"."sigia_student"."live" = TRUE
            ORDER BY
                 student_user."last_name" ASC,
                 student_user."first_name" ASC
        ) t
        """)

        return JsonResponse(cursor.fetchall()[0][0], safe=False)


class EnrollmentCreateView(View):
    title = 'Registrar Matrícula'
    template_name = 'enrollment_form.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Matrículas", "/enrollment/"),
                         BreadCrumb("Registrar Matrícula", "/enrollment/new/"),)
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EnrollmentCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        enrollment_form = CreateEnrollmentForm(initial={'date': timezone.now()})
        enrollment_form.fields["student"].queryset = Student.objects.filter().exclude(modified_by=None).order_by('id')
        enrollment_form.fields["course"].queryset = Course.objects.filter(period__active=True).order_by('period',
                                                                                                        'semester',
                                                                                                        'career',
                                                                                                        'level')

        if kwargs.has_key('pk'):
            student = Student.objects.get(id=kwargs['pk'])
            enrollment_form = CreateEnrollmentForm(initial={'student': student, 'date': timezone.now()})
            enrollment_form.fields["course"].queryset = Course.objects.filter(Q(career=student.career) | Q(career=None),
                                                                              period__active=True).order_by('period',
                                                                                                            'semester',
                                                                                                            'career',
                                                                                                            'level')
            enrollment_form.fields["student"].queryset = Student.objects.filter(id=kwargs['pk']).order_by('id')
        context = {'action': self.action, 'enrollment_form': enrollment_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):

        enrollment_form = CreateEnrollmentForm(request.POST)
        if enrollment_form.is_valid():
            enrollment = enrollment_form.save(commit=False)
            cursor = connections['default'].cursor()
            # print (""" select count(id) from sigia_paymentorder where  payout != true and live = true and user_id = %s """,(enrollment.student.user_id,))
            cursor.execute(
                """ SELECT count(id) FROM sigia_paymentorder WHERE  payout != TRUE AND live = TRUE AND user_id = %s """,
                (enrollment.student.user_id,))
            contador = cursor.fetchone()[0]
            # print contador

            if (contador == 0):
                enrollment.save()

                payment = PaymentOrder()
                payment.user = enrollment.student.user

                course = enrollment.course

                payment.payment_concept = convert_enrrollment_type_to_payment_concept(enrollment.type)
                if enrollment.type == 'EXT':
                    payment.value = course.payment_ext
                elif enrollment.type == 'ESP':
                    payment.value = course.payment_esp
                else:
                    payment.value = course.payment_reg

                if payment.value == 0:
                    payment.payout = True
                else:
                    payment.payout = False
                    payment.date_issue = timezone.now()
                    payment.level = course.level
                    payment.period = course.period
                    payment.semester = course.semester
                    payment.enrollment = enrollment
                    payment.save()

                enrollment.payment_order = payment
                enrollment.save()

                for i in range(1, course.amount_payments + 1):
                    payment_quota = PaymentOrder()
                    payment_quota.user = enrollment.student.user
                    payment_quota.enrollment = enrollment

                    course = enrollment.course

                    payment_quota.payment_concept = 'QUOT'
                    payment_quota.value = course.value_payments
                    payment_quota.date_issue = timezone.now()
                    payment_quota.payout = False
                    payment_quota.level = course.level
                    payment_quota.period = course.period
                    payment_quota.semester = course.semester
                    payment_quota.number = i
                    payment_quota.enrollment = enrollment
                    payment_quota.save()

                    course.save()

                message = 'Se ha añadido correctamente la matrícula: %s' % enrollment
                messages.add_message(request, messages.SUCCESS, message)

                if payment.value != 0:
                    message = base64.b64encode("""
                    var url = "http://%s/pentaho/api/repos/%%3Aaitec%%3Apaymentorder_by_id.prpt/generatedContent?userid=admin&password=password&output-type=pageable/pdf&paymentorder_id=" + %d;
                        
                        $.jsPanel({
                              title: 'Orden de Pago: ',
                              bootstrap: true,
                              position: "center",
                              size:     { width:  800, height: 600 },
                              content: '<embed src="' + url + '" width="100%%" height="100%%">',
                            }).show();
                    """ % (settings.REPORT_SERVER, payment.id))
                    # messages.add_message(request, settings.JS_MESSAGE, message)

                    return redirect_view(EnrollmentListView, request)
            else:
                message = 'El estudiante tiene Deuda, no se puede matricular'
                messages.add_message(request, messages.ERROR, message)
                context = {'action': self.action, 'enrollment_form': enrollment_form, 'title': self.title,
                           'breadCrumbEntries': self.breadCrumbEntries}
                return render_to_response(self.template_name, RequestContext(request, context))
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'enrollment_form': enrollment_form, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class EnrollmentUpdateView(View):
    title = 'Actualizar Matrícula'
    template_name = 'enrollment_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Matrículas", "/enrollment/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EnrollmentUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        enrollment_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Listado de Matrículas", "/enrollment/%s/upgrade/" % enrollment_id),)
        enrollment = Enrollment.objects.get(id=enrollment_id)
        enrollment_form = UpdateEnrollmentForm(instance=enrollment)
        context = {'action': self.action, 'enrollment_form': enrollment_form, 'enrollment_id': enrollment.id,
                   'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        enrollment_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Listado de Matrículas", "/enrollment/%s/upgrade/" % enrollment_id),)
        enrollment = Enrollment.objects.get(id=enrollment_id)
        enrollment_form = UpdateEnrollmentForm(request.POST, instance=enrollment)

        if enrollment_form.is_valid():
            enrollment = enrollment_form.save()
            message = 'Se ha actualizado correctamente el curso: %s' % enrollment
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(EnrollmentListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'enrollment_form': enrollment_form, 'enrollment_id': enrollment.id,
                       'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class EnrollmentDeleteView(View):
    redirect_url = '/enrollment/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EnrollmentDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_enrollment = kwargs['pk']
        enrollment = Enrollment.objects.get(id=id_enrollment)
        enrollment_name = "%s : %s" % (enrollment.student, enrollment.course)
        enrollment.delete()
        message = 'Se ha eliminado correctamente la matrícula: %s.' % enrollment_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(EnrollmentListView, request)


class PeriodListView(TemplateView):
    title = 'Listado de Períodos'
    template_name = 'period_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Períodos", "/period/"),)

    def get_context_data(self, **kwargs):
        context = super(PeriodListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class PeriodListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        periods = Period.objects.all().order_by("-name")
        for period in periods:
            predecessor = ""
            if hasattr(period, 'predecessor'):
                predecessor = period.predecessor

            std = {'id': period.id,
                   'name': "%s" % (period.name),
                   'predecessor': "%s" % predecessor,
                   'active': period.active,
                   'finalized': period.finalized,
                   'start_notes': period.start_notes,
                   'end_notes': period.end_notes}
            array.append(std)
        return JsonResponse(array, safe=False)


class PeriodActivateView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PeriodActivateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        period_id = kwargs['pk']
        period = Period.objects.get(id=period_id)

        if (period.active):
            message = 'El período ya se encuentra activado.'
            messages.add_message(request, messages.ERROR, message)
            return redirect_view(PeriodListView, request)
        if (period.finalized):
            message = 'Un período finalizado no puede ser reactivado.'
            messages.add_message(request, messages.ERROR, message)
            return redirect_view(PeriodListView, request)
        if (Period.objects.filter(active=True).exists()):
            message = 'Un período no puede ser activado si otro se encuentra activo.'
            messages.add_message(request, messages.ERROR, message)
            return redirect_view(PeriodListView, request)
        period.active = True
        period.save()
        message = 'El período: %s se ha activado correctamente.' % period
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(PeriodListView, request)


class PeriodTerminateView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PeriodTerminateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        period_id = kwargs['pk']
        period = Period.objects.get(id=period_id)
        if (period.active):
            period.active = False
            period.finalized = True
            period.save()
            message = 'El período %s se ha finalizado correctamente.' % period
            messages.add_message(request, messages.SUCCESS, message)
        else:
            message = 'El período no puede ser desactivado si este no está activo.'
            messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(PeriodListView, request)


class PeriodCreateView(View):
    title = 'Registrar Período'
    template_name = 'period_form.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Períodos", "/period/"),
                         BreadCrumb("Registrar Período", "/period/new/"),)
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PeriodCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        period_form = PeriodCreateForm()
        context = {'action': self.action, 'period_form': period_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        period_form = PeriodCreateForm(request.POST)

        if period_form.is_valid():
            period = period_form.save(commit=False)
            period.save()
            message = 'Se ha añadido correctamente el período: %s' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(PeriodListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'period_form': period_form, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class PeriodUpdateView(View):
    title = 'Actualizar Período'
    template_name = 'period_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Períodos", "/period/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PeriodUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        period_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Período", "/period/%s/upgrade/" % period_id),)
        period = Period.objects.get(id=period_id)
        period_form = PeriodCreateForm(instance=period)
        context = {'action': self.action, 'period_form': period_form, 'period_id': period.id, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        period_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Período", "/period/%s/upgrade/" % period_id),)
        period = Period.objects.get(id=period_id)
        period_form = PeriodCreateForm(request.POST, instance=period)

        if period_form.is_valid():
            period_form.save()
            message = 'Se ha actualizado correctamente el período: %s' % period.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(PeriodListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'period_form': period_form, 'period_id': period.id, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class PeriodDeleteView(View):
    redirect_url = '/period/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PeriodDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_period = kwargs['pk']
        period = Period.objects.get(id=id_period)
        period_name = period.name
        period.delete()
        message = 'Se ha eliminado correctamente el período: %s.' % period_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(PeriodListView, request)


class PaymentOrderListView(TemplateView):
    title = 'Listado de Órdenes de Pago'
    template_name = 'payment_order_list.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Órdenes de Pago", "/payment_order/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PaymentOrderListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(PaymentOrderListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id', None)
        if student_id:
            student = Student.objects.get(id=student_id)
            message = base64.b64encode(("""
                    $search = $("th[data-field='name'] input");
                    $search.val("%s, %s");
                    $search.trigger('keyup');
                    """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
            messages.add_message(request, settings.JS_MESSAGE, message)
        return super(PaymentOrderListView, self).get(request, *args, **kwargs)


class PaymentOrderListData(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PaymentOrderListData, cls).as_view(**initkwargs)
        return gzip_page(view)

    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(t)))
        FROM (
            SELECT
                 "auth_user"."last_name" || ', ' || "auth_user"."first_name" AS name,
                 created_user."username" AS created_by,
                 modified_user."username" AS modified_by,
                 "public"."sigia_paymentorder"."created",
                 "public"."sigia_paymentorder"."modified",
                 "public"."sigia_paymentorder"."date_issue",
                 "public"."sigia_paymentorder"."payout",
                 "public"."sigia_paymentorder"."date_payment",
                 "public"."sigia_paymentorder"."level",
                 "public"."sigia_period"."name" AS period,
                 "public"."sigia_paymentorder"."semester",
                 "public"."sigia_paymentorder"."value",
                 "public"."sigia_paymentorder"."payment_concept",
                 "public"."sigia_paymentorder"."number",
                 "public"."sigia_paymentorder"."id"
            FROM
                 "public"."sigia_paymentorder" LEFT OUTER JOIN "public"."auth_user" ON "public"."sigia_paymentorder"."user_id" = auth_user."id"
                 LEFT OUTER JOIN "public"."auth_user" created_user ON "public"."sigia_paymentorder"."created_by_id" = created_user."id"
                 LEFT OUTER JOIN "public"."auth_user" modified_user ON "public"."sigia_paymentorder"."modified_by_id" = modified_user."id"
                 LEFT OUTER JOIN "public"."sigia_period" ON "public"."sigia_paymentorder"."period_id" = "public"."sigia_period"."id"
            WHERE
                 "public"."sigia_paymentorder"."live" = TRUE
            ORDER BY
                "public"."sigia_paymentorder"."id"
        ) t
        """)

        return JsonResponse(cursor.fetchall()[0][0], safe=False)


class PaymentOrderCreateView(View):
    title = 'Registrar Orden de Pago'
    template_name = 'payment_order_form.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Órdenes de Pago", "/payment_order/"),
        BreadCrumb("Registrar Orden de Pago", "/payment_order/new/"),)
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PaymentOrderCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        data = timezone.now()
        payment_order_form = PaymentOrderForm(initial={'date_issue': data})
        student_id = kwargs.get('student_id', None)
        if student_id:
            student = Student.objects.get(id=student_id)
            payment_order_form = PaymentOrderForm(initial={'date_issue': data, 'user': student.user})
        context = {'action': self.action, 'payment_order_form': payment_order_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        payment_order_form = PaymentOrderForm(request.POST)

        if payment_order_form.is_valid():
            payment_order = payment_order_form.save(commit=False)
            payment_order.save()

            message = 'Se ha añadido correctamente la orden de pago: %s' % payment_order
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(PaymentOrderListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'payment_order_form': payment_order_form, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class PaymentOrderUpdateView(View):
    title = 'Actualizar Orden de Pago'
    template_name = 'payment_order_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Órdenes de Pago", "/payment_order/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PaymentOrderUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        payment_order_id = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Listado de Órdenes de Pago", "/payment_order/%s/upgrade/" % payment_order_id),)
        payment_order = PaymentOrder.objects.get(id=payment_order_id)
        payment_order_form = PaymentOrderForm(instance=payment_order)
        context = {'action': self.action, 'payment_order_form': payment_order_form,
                   'payment_order_id': payment_order.id,
                   'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        payment_order_id = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Listado de Órdenes de Pago", "/payment_order/%s/upgrade/" % payment_order_id),)
        payment_order = PaymentOrder.objects.get(id=payment_order_id)
        payment_order_form = PaymentOrderForm(request.POST, instance=payment_order)

        if payment_order_form.is_valid():
            payment_order = payment_order_form.save()
            message = 'Se ha actualizado correctamente el curso: %s' % payment_order
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(PaymentOrderListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'payment_order_form': payment_order_form,
                       'payment_order_id': payment_order.id,
                       'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class PaymentOrderCancelView(View):
    title = 'Cancelar Orden de Pago'
    template_name = 'cancel_payment_order_form.djhtml'
    redirect_url = '/payment_order/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PaymentOrderCancelView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        payment_order_id = kwargs['pk']
        payment_order = PaymentOrder.objects.get(id=payment_order_id)
        payment_order_form = PaymentOrderForm(instance=payment_order,
                                              initial={'date_payment': timezone.now(), 'payout': True})
        context = {'payment_order_form': payment_order_form, 'payment_order': payment_order, 'title': self.title, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_payment_order = kwargs['pk']
        payment_order = PaymentOrder.objects.get(id=id_payment_order)
        payment_order.payout = True
        payment_order.save()
        message = 'Se ha cancelado correctamente la orden de pago: %s.' % payment_order
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(PaymentOrderListView, request)


class PaymentOrderDeleteView(View):
    redirect_url = '/payment_order/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PaymentOrderDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_payment_order = kwargs['pk']
        payment_order = PaymentOrder.objects.get(id=id_payment_order)
        payment_order_name = "%s" % payment_order
        payment_order.delete()
        message = 'Se ha eliminado correctamente la orden de pago: %s.' % payment_order_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(PaymentOrderListView, request)


class SetScholarshipView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(SetScholarshipView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_enrollment = kwargs['pk']
        enrollment = Enrollment.objects.get(id=id_enrollment)
        enrollment.scholarship = int(request.POST['in_scholarship'])
        enrollment.save()

        value = enrollment.course.value_payments

        for payment in enrollment.payment_related.all():
            if payment.number >= enrollment.course.applied_scholarship_from:
                payment.value = value - (value * float(enrollment.scholarship) / 100)
                payment.save()

        message = 'Se asignado correctamente la beca de un: %s%%, a la matrícula %s.' % (
            enrollment.scholarship, enrollment)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(EnrollmentListView, request)


class GenerateEnrollmentBookView(View):
    title = 'Generar Libro de Matrícula'
    template_name = 'generate_enrollment_book.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Matrículas", "/enrollment/"),
                         BreadCrumb("Generar Libro de Matrículas", "/enrollment/generate_enrollment_book/"))

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(GenerateEnrollmentBookView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        if Period.objects.filter(active=True).count() > 0:
            active_period = Period.objects.filter(active=True)[0]
            gen_enbook = GenEnrollmentBookForm(initial={'period': active_period})
            context = {'gen_enbook': gen_enbook, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))
        else:
            return redirect_view(EnrollmentListView, request)


class EthnicGroupListView(TemplateView):
    title = 'Listado de Grupos Étnicos'
    template_name = 'ethnic_group_list.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Grupos Étnicos", "/ethnic_group/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EthnicGroupListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(EthnicGroupListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class EthnicGroupListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        ethnic_groups = EthnicGroup.objects.all().order_by('id')
        for ethnic_group in ethnic_groups:
            std = {'id': ethnic_group.id,
                   'name': "%s" % (ethnic_group.name),
                   'description': ethnic_group.description, }
            array.append(std)
        return JsonResponse(array, safe=False)


class EthnicGroupCreateView(View):
    title = 'Registrar Grupo Étnico'
    template_name = 'ethnic_group_form.djhtml'
    action = 'CREATE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Grupos Étnicos", "/ethnic_group/"),
        BreadCrumb("Registrar Grupo Étnico", "/ethnic_group/new/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EthnicGroupCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        ethnic_group_form = EthnicGroupForm()
        context = {'title': self.title, 'action': self.action, 'ethnic_group_form': ethnic_group_form,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        ethnic_group_form = EthnicGroupForm(request.POST)

        if ethnic_group_form.is_valid():
            ethnic_group_form.save()
            message = 'Se ha añadido correctamente al grupo étnico: %s.' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(EthnicGroupListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'ethnic_group_form': ethnic_group_form,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class EthnicGroupUpdateView(View):
    title = 'Actualizar Grupo Étnico'
    template_name = 'ethnic_group_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Grupos Étnicos", "/ethnic_group/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EthnicGroupUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        ethnic_group_id = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Actualizar Grupo Étnico", "/ethnic_group/%s/upgrade/" % ethnic_group_id),)
        ethnic_group = EthnicGroup.objects.get(id=ethnic_group_id)
        ethnic_group_form = EthnicGroupForm(instance=ethnic_group)
        context = {'title': self.title, 'action': self.action, 'ethnic_group_form': ethnic_group_form,
                   'ethnic_group_id': ethnic_group.id, 'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        ethnic_group_id = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Actualizar Grupo Étnico", "/ethnic_group/%s/upgrade/" % ethnic_group_id),)
        ethnic_group = EthnicGroup.objects.get(id=ethnic_group_id)
        ethnic_group_form = EthnicGroupForm(request.POST, instance=ethnic_group)

        if ethnic_group_form.is_valid():
            ethnic_group_form.save()
            message = 'Se ha actualizado correctamente al grupo étnico: %s.' % ethnic_group.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(EthnicGroupListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'ethnic_group_form': ethnic_group_form,
                       'ethnic_group_id': ethnic_group.id, 'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class EthnicGroupDeleteView(View):
    redirect_url = '/ethnic_group/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EthnicGroupDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_ethnic_group = kwargs['pk']
        ethnic_group = EthnicGroup.objects.get(id=id_ethnic_group)
        ethnic_group_name = ethnic_group.name
        ethnic_group.delete()
        message = 'Se ha eliminado correctamente el grupo étnico: : %s.' % ethnic_group_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(EthnicGroupListView, request)


class BugReportListView(TemplateView):
    title = 'Listado de Errores'
    template_name = 'bug_report_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Errores", "/bug_report/"),)

    def get_context_data(self, **kwargs):
        context = super(BugReportListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class BugReportListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        bug_reports = BugReport.objects.all().order_by('id')
        for bug_report in bug_reports:
            std = {'id': bug_report.id,
                   'name': "%s" % (bug_report.name),
                   'description': bug_report.description,
                   'gravity': bug_report.get_gravity_display(),
                   'bug_state': bug_report.get_state_display(), }
            array.append(std)
        return JsonResponse(array, safe=False)


class BugReportCreateView(View):
    title = 'Registrar Error'
    template_name = 'bug_report_form.djhtml'
    action = 'CREATE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Errores", "/bug_report/"),
                         BreadCrumb("Registrar Error", "/bug_report/new/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(BugReportCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        bug_report_form = BugReportForm()
        context = {'title': self.title, 'action': self.action, 'bug_report_form': bug_report_form,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        bug_report_form = BugReportForm(request.POST, request.FILES)

        if bug_report_form.is_valid():
            bug_report = bug_report_form.save(commit=False)
            bug_report.state = 'R'
            bug_report.save()
            message = 'Se ha reportado correctamente el error %s.' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(BugReportListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'bug_report_form': bug_report_form,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class BugReportUpdateView(View):
    title = 'Actualizar Error'
    template_name = 'bug_report_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Errores", "/bug_report/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(BugReportUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        bug_report_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Error", "/bug_report/%s/upgrade/" % bug_report_id),)
        bug_report = BugReport.objects.get(id=bug_report_id)
        bug_report_form = BugReportForm(instance=bug_report)
        context = {'title': self.title, 'action': self.action, 'bug_report_form': bug_report_form,
                   'bug_report_id': bug_report.id, 'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        bug_report_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Error", "/bug_report/%s/upgrade/" % bug_report_id),)
        bug_report = BugReport.objects.get(id=bug_report_id)
        bug_report_form = BugReportForm(request.POST, request.FILES, instance=bug_report)

        if bug_report_form.is_valid():
            bug_report_form.save()
            message = 'Se ha actualizado correctamente el reporte del error: %s.' % bug_report.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(BugReportListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'bug_report_form': bug_report_form,
                       'bug_report_id': bug_report.id, 'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class BugReportDeleteView(View):
    redirect_url = '/bug_report/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(BugReportDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_bug_report = kwargs['pk']
        bug_report = BugReport.objects.get(id=id_bug_report)
        bug_report_name = bug_report.name
        bug_report.delete()
        message = 'Se ha eliminado correctamente el reporte de error: : %s.' % bug_report_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(BugReportListView, request)


class CountryListView(TemplateView):
    title = 'Listado de Países'
    template_name = 'country_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Países", "/country/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CountryListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class CountryListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        countrys = Country.objects.all().order_by('id')
        for country in countrys:
            std = {'id': country.id,
                   'name': "%s" % (country.name),
                   'gentilicio': country.gentilicio, }
            array.append(std)
        return JsonResponse(array, safe=False)


class CountryCreateView(View):
    title = 'Registrar País'
    template_name = 'country_form.djhtml'
    action = 'CREATE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Países", "/country/"),
                         BreadCrumb("Registrar País", "/country/new/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CountryCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        country_form = CountryForm()
        context = {'title': self.title, 'action': self.action, 'country_form': country_form,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        country_form = CountryForm(request.POST, request.FILES)

        if country_form.is_valid():
            country_form.save()
            message = 'Se ha registrado correctamente el cantón %s.' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CountryListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'country_form': country_form,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class CountryUpdateView(View):
    title = 'Actualizar País'
    template_name = 'country_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Países", "/country/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CountryUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        country_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar País", "/country/%s/upgrade/" % country_id),)
        country = Country.objects.get(id=country_id)
        country_form = CountryForm(instance=country)
        context = {'title': self.title, 'action': self.action, 'country_form': country_form,
                   'country_id': country.id, 'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        country_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar País", "/country/%s/upgrade/" % country_id),)
        country = Country.objects.get(id=country_id)
        country_form = CountryForm(request.POST, request.FILES, instance=country)

        if country_form.is_valid():
            country_form.save()
            message = 'Se ha actualizado correctamente el reporte el cantón: %s.' % country.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CountryListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'country_form': country_form,
                       'country_id': country.id, 'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class CountryDeleteView(View):
    redirect_url = '/country/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CountryDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_country = kwargs['pk']
        country = Country.objects.get(id=id_country)
        country_name = country.name
        country.delete()
        message = 'Se ha eliminado correctamente el cantón: : %s.' % country_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(CountryListView, request)


class ProvinceListView(TemplateView):
    title = 'Listado de Provincias'
    template_name = 'province_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Provincias", "/province/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProvinceListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(ProvinceListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class ProvinceListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        provinces = Province.objects.all().order_by('id')
        for province in provinces:
            std = {'id': province.id,
                   'name': "%s" % (province.name),
                   'country': "%s" % province.country, }
            array.append(std)
        return JsonResponse(array, safe=False)


class ProvinceCreateView(View):
    title = 'Registrar País'
    template_name = 'province_form.djhtml'
    action = 'CREATE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Provincias", "/province/"),
                         BreadCrumb("Registrar País", "/province/new/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProvinceCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        province_form = ProvinceForm()
        context = {'title': self.title, 'action': self.action, 'province_form': province_form,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        province_form = ProvinceForm(request.POST, request.FILES)

        if province_form.is_valid():
            province_form.save()
            message = 'Se ha registrado correctamente el cantón %s.' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(ProvinceListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'province_form': province_form,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class ProvinceUpdateView(View):
    title = 'Actualizar Provincia'
    template_name = 'province_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Provincias", "/province/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProvinceUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        province_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Provincia", "/province/%s/upgrade/" % province_id),)
        province = Province.objects.get(id=province_id)
        province_form = ProvinceForm(instance=province)
        context = {'title': self.title, 'action': self.action, 'province_form': province_form,
                   'province_id': province.id, 'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        province_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Provincia", "/province/%s/upgrade/" % province_id),)
        province = Province.objects.get(id=province_id)
        province_form = ProvinceForm(request.POST, request.FILES, instance=province)

        if province_form.is_valid():
            province_form.save()
            message = 'Se ha actualizado correctamente el reporte el cantón: %s.' % province.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(ProvinceListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'province_form': province_form,
                       'province_id': province.id, 'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class ProvinceDeleteView(View):
    redirect_url = '/province/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProvinceDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_province = kwargs['pk']
        province = Province.objects.get(id=id_province)
        province_name = province.name
        province.delete()
        message = 'Se ha eliminado correctamente el cantón: : %s.' % province_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(ProvinceListView, request)


class CantonListView(TemplateView):
    title = 'Listado de Cantones'
    template_name = 'canton_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cantones", "/canton/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CantonListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(CantonListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class CantonListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        cantons = Canton.objects.all().order_by('id')
        for canton in cantons:
            std = {'id': canton.id,
                   'name': "%s" % (canton.name),
                   'province': "%s" % canton.province, }
            array.append(std)
        return JsonResponse(array, safe=False)


class CantonCreateView(View):
    title = 'Registrar Cantón'
    template_name = 'canton_form.djhtml'
    action = 'CREATE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cantones", "/canton/"),
                         BreadCrumb("Registrar Cantón", "/canton/new/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CantonCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        canton_form = CantonForm()
        context = {'title': self.title, 'action': self.action, 'canton_form': canton_form,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        canton_form = CantonForm(request.POST, request.FILES)

        if canton_form.is_valid():
            canton_form.save()
            message = 'Se ha registrado correctamente el cantón %s.' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CantonListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'canton_form': canton_form,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class CantonUpdateView(View):
    title = 'Actualizar Cantón'
    template_name = 'canton_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cantones", "/canton/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CantonUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        canton_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Cantón", "/canton/%s/upgrade/" % canton_id),)
        canton = Canton.objects.get(id=canton_id)
        canton_form = CantonForm(instance=canton)
        context = {'title': self.title, 'action': self.action, 'canton_form': canton_form,
                   'canton_id': canton.id, 'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        canton_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Cantón", "/canton/%s/upgrade/" % canton_id),)
        canton = Canton.objects.get(id=canton_id)
        canton_form = CantonForm(request.POST, request.FILES, instance=canton)

        if canton_form.is_valid():
            canton_form.save()
            message = 'Se ha actualizado correctamente el reporte el cantón: %s.' % canton.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(CantonListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'canton_form': canton_form,
                       'canton_id': canton.id, 'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class CantonDeleteView(View):
    redirect_url = '/canton/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CantonDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_canton = kwargs['pk']
        canton = Canton.objects.get(id=id_canton)
        canton_name = canton.name
        canton.delete()
        message = 'Se ha eliminado correctamente el cantón: : %s.' % canton_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(CantonListView, request)


class ParishListView(TemplateView):
    title = 'Listado de Parroquias'
    template_name = 'parish_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Parroquias", "/parish/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ParishListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(ParishListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class ParishListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        parishs = Parish.objects.all().order_by('id')
        for parish in parishs:
            std = {'id': parish.id,
                   'name': "%s" % (parish.name),
                   'canton': "%s" % parish.canton, }
            array.append(std)
        return JsonResponse(array, safe=False)


class ParishCreateView(View):
    title = 'Registrar Parroquia'
    template_name = 'parish_form.djhtml'
    action = 'CREATE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Parroquias", "/parish/"),
                         BreadCrumb("Registrar Parroquia", "/parish/new/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ParishCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        parish_form = ParishForm()
        context = {'title': self.title, 'action': self.action, 'parish_form': parish_form,
                   'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        parish_form = ParishForm(request.POST, request.FILES)

        if parish_form.is_valid():
            parish_form.save()
            message = 'Se ha registrado correctamente el cantón %s.' % request.POST['name']
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(ParishListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'parish_form': parish_form,
                       'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class ParishUpdateView(View):
    title = 'Actualizar Parroquia'
    template_name = 'parish_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Parroquias", "/parish/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ParishUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        parish_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Parroquia", "/parish/%s/upgrade/" % parish_id),)
        parish = Parish.objects.get(id=parish_id)
        parish_form = ParishForm(instance=parish)
        context = {'title': self.title, 'action': self.action, 'parish_form': parish_form,
                   'parish_id': parish.id, 'breadCrumbEntries': self.breadCrumbEntries, }
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        parish_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Parroquia", "/parish/%s/upgrade/" % parish_id),)
        parish = Parish.objects.get(id=parish_id)
        parish_form = ParishForm(request.POST, request.FILES, instance=parish)

        if parish_form.is_valid():
            parish_form.save()
            message = 'Se ha actualizado correctamente el reporte el cantón: %s.' % parish.name
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(ParishListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'title': self.title, 'action': self.action, 'parish_form': parish_form,
                       'parish_id': parish.id, 'breadCrumbEntries': self.breadCrumbEntries, }
            return render_to_response(self.template_name, RequestContext(request, context))


class ParishDeleteView(View):
    redirect_url = '/parish/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ParishDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_parish = kwargs['pk']
        parish = Parish.objects.get(id=id_parish)
        parish_name = parish.name
        parish.delete()
        message = 'Se ha eliminado correctamente el cantón: : %s.' % parish_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(ParishListView, request)


class TeacherListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        teachers = Teacher.objects.all().order_by('id')
        for teacher in teachers:
            std = {'id': teacher.id,
                   'last_name': "%s" % teacher.user.last_name,
                   'first_name': "%s" % teacher.user.first_name,
                   'email': teacher.institutional_email,
                   'academic_category': teacher.academic_category,
                   'contract_type': teacher.get_contract_type_display(),
                   'hours_to_pedagogy': teacher.hours_to_pedagogy,
                   'approved': (True if teacher.modified_by else False),
                   'created': "%s" % teacher.created.astimezone(ecu_tz).strftime('%d/%m/%y %H:%M'),
                   'created_by': "%s" % teacher.created_by,
                   'modified': "%s" % teacher.modified.astimezone(ecu_tz).strftime("%d/%m/%y %H:%M"),
                   'modified_by': "%s" % teacher.modified_by}
            array.append(std)
        return JsonResponse(array, safe=False)


class TeacherListView(TemplateView):
    title = 'Listado de Profesores'
    template_name = 'teacher_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Profesores", "/teacher/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(TeacherListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(TeacherListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class TeacherDeleteView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(TeacherDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_student = kwargs['pk']
        teacher = Teacher.objects.get(id=id_student)
        user = teacher.user
        student_name = "%s %s" % (user.first_name, user.last_name)
        teacher.delete()
        profile = UserProfile.objects.get(user=user)
        profile.delete()
        user.is_active = False
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Se ha eliminado correctamente al profesor: %s.' % student_name)
        return redirect_view(TeacherListView, request)


class TeacherUpdateView(View):
    title = 'Actualizar Profesor'
    template_name = 'teacher_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Profesores", "/teacher/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(TeacherUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_student = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Profesor", "/teacher/%s/upgrade/" % id_student),)
        teacher = Teacher.objects.get(id=id_student)
        user = teacher.user
        profile = UserProfile.objects.get(user=user)

        user_form = UserForm(instance=user)
        personal_info_form = UserPersonalInfoForm(instance=profile)
        teacher_form = TeacherForm(instance=teacher)

        context = {'action': self.action, 'user_form': user_form, 'id_teacher': teacher.id,
                   'personal_info_form': personal_info_form,
                   'teacher_form': teacher_form, 'title': self.title,
                   'teacher': teacher, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_student = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Profesor", "/teacher/%s/upgrade/" % id_student),)
        teacher = Teacher.objects.get(id=id_student)
        user = teacher.user
        profile = UserProfile.objects.get(user=user)

        user_form = UserForm(request.POST, instance=user)
        personal_info_form = UserPersonalInfoForm(request.POST, request.FILES, instance=profile)
        teacher_form = TeacherForm(request.POST, instance=teacher)

        if user_form.is_valid() and personal_info_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            personal_info_form.save()
            teacher_form.save()

            message = 'Se ha actualizado correctamente al profesor %s %s.' % (user.first_name, user.last_name)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(TeacherListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'user_form': user_form, 'id_teacher': teacher.id,
                       'personal_info_form': personal_info_form,
                       'teacher_form': teacher_form, 'title': self.title,
                       'teacher': teacher, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))


class TeacherCreateView(View):
    title = 'Registrar Profesor'
    template_name = 'teacher_form.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Profesores", "/teacher/"),
                         BreadCrumb("Registrar Profesor", "/teacher/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(TeacherCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        personal_info_form = UserPersonalInfoForm()
        teacher_form = TeacherForm()
        context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                   'teacher_form': teacher_form, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        personal_info_form = UserPersonalInfoForm(request.POST, request.FILES)
        teacher_form = TeacherForm(request.POST)

        if user_form.is_valid() and personal_info_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()

            userprofile = personal_info_form.save(commit=False)
            userprofile.user = user
            userprofile.live = True

            teacher_info = teacher_form.save(commit=False)
            teacher_info.user = user
            teacher_info.live = True

            user.save()
            userprofile.save()
            teacher_info.save()

            if request.user.is_authenticated():
                message = 'Se ha añadido correctamente al profesor %s %s.' % (user.first_name, user.last_name)
                messages.add_message(request, messages.SUCCESS, message)
                return redirect_view(TeacherListView, request)
            else:
                return redirect_view(OnlineEnrollmentSuccessView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                       'teacher_form': teacher_form, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

            return render_to_response(self.template_name, RequestContext(request, context))


class EventTypeListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        event_types = EventType.objects.all().order_by('id')
        for event_type in event_types:
            std = {'id': event_type.id,
                   'name': "%s" % event_type.name,
                   'description': "%s" % event_type.description,
                   'student_type': event_type.get_student_type_display(),
                   'created': "%s" % event_type.created.astimezone(ecu_tz).strftime("%d/%m/%y %H:%M"),
                   'created_by': "%s" % event_type.created_by,
                   'modified': "%s" % event_type.modified.astimezone(ecu_tz).strftime("%d/%m/%y %H:%M"),
                   'modified_by': "%s" % event_type.modified_by}
            array.append(std)
        return JsonResponse(array, safe=False)


class EventTypeListView(TemplateView):
    title = 'Listado de Tipos de Eventos'
    template_name = 'event_type_list.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Tipos de Eventos", "/event_type/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventTypeListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(EventTypeListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class EventTypeDeleteView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventTypeDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_event_type = kwargs['pk']
        event_type = EventType.objects.get(id=id_event_type)
        event_type.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Se ha eliminado correctamente al tipo de evento: %s.' % event_type.name)
        return redirect_view(EventTypeListView, request)


class EventTypeUpdateView(View):
    title = 'Actualizar Tipo de Evento'
    template_name = 'event_type_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Tipos de Eventos", "/event_type/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventTypeUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_event_type = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Tipo de Evento", "/event_type/%s/upgrade/" % id_event_type),)
        event_type = EventType.objects.get(id=id_event_type)

        event_type_form = EventTypeForm(instance=event_type)

        context = {'action': self.action, 'id_event_type': event_type.id,
                   'event_type_form': event_type_form, 'title': self.title,
                   'event_type': event_type, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_event_type = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Tipo de Evento", "/event_type/%s/upgrade/" % id_event_type),)
        event_type = EventType.objects.get(id=id_event_type)

        event_type_form = EventTypeForm(request.POST, instance=event_type)

        if event_type_form.is_valid():
            event_type_form.save()

            message = 'Se ha actualizado correctamente al tipo de evento %s.' % (event_type.name)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(EventTypeListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'id_event_type': event_type.id,
                       'event_type_form': event_type_form, 'title': self.title,
                       'event_type': event_type, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))


class EventTypeCreateView(View):
    title = 'Registrar Tipo de Evento'
    template_name = 'event_type_form.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Tipos de Eventos", "/event_type/"),
        BreadCrumb("Registrar Tipo de Evento", "/event_type/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventTypeCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        event_type_form = EventTypeForm()
        context = {'action': self.action, 'event_type_form': event_type_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        event_type_form = EventTypeForm(request.POST)

        if event_type_form.is_valid():
            event_type = event_type_form.save()

            message = 'Se ha creado correctamente al tipo de evento %s.' % (event_type)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(EventTypeListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'event_type_form': event_type_form,
                       'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

            return render_to_response(self.template_name, RequestContext(request, context))


class StudentEventListData(View):
    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(t)))
        FROM (
            SELECT
                sigia_studentevent.id, 
                to_char(sigia_studentevent.created, 'DD/MM/YY HH24:MI') AS created,
                to_char(sigia_studentevent.modified, 'DD/MM/YY HH24:MI') AS modified,
                created_user.username AS created_by, 
                modified_user.username AS modified_by, 
                student_user.last_name || ', ' || student_user.first_name AS name,
                sigia_eventtype.name AS event_type, 
                to_char(sigia_studentevent.start_date, 'DD/MM/YY') AS start_date,
                to_char(sigia_studentevent.end_date, 'DD/MM/YY') AS end_date,
                sigia_studentevent.ini_obs, 
                sigia_studentevent.state AS event_state,
                sigia_studentevent.end_obs,
                teacher_user.last_name || ', ' || teacher_user.first_name AS tutor, 
                manager_user.last_name || ', ' || manager_user.first_name AS manager,
                "public"."sigia_student"."type" AS student_type
            FROM 
                "public"."auth_user" created_user RIGHT OUTER JOIN "public"."sigia_studentevent" ON created_user."id" = "public"."sigia_studentevent"."created_by_id"
                LEFT OUTER JOIN "public"."auth_user" modified_user ON "public"."sigia_studentevent"."modified_by_id" = modified_user."id"
                LEFT OUTER JOIN "public"."sigia_eventtype" ON "public"."sigia_studentevent"."type_id" = "public"."sigia_eventtype"."id"
                LEFT OUTER JOIN "public"."sigia_student" ON "public"."sigia_studentevent"."student_id" = "public"."sigia_student"."id"
                LEFT OUTER JOIN "public"."sigia_teacher" ON "public"."sigia_studentevent"."tutor_id" = "public"."sigia_teacher"."id"
                LEFT OUTER JOIN "public"."auth_user" manager_user ON "public"."sigia_studentevent"."manager_id" = manager_user."id"
                LEFT OUTER JOIN "public"."auth_user" teacher_user ON "public"."sigia_teacher"."user_id" = teacher_user."id"
                LEFT OUTER JOIN "public"."auth_user" student_user ON "public"."sigia_student"."user_id" = student_user."id"
            WHERE
                sigia_studentevent.live = TRUE
            ORDER BY
                sigia_studentevent.start_date
        ) t
        """)

        return JsonResponse(cursor.fetchall()[0][0], safe=False)


class StudentEventListView(TemplateView):
    title = 'Listado de Eventos de Estudiantes'
    template_name = 'student_event_list.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Eventos de Estudiantes", "/student_event/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentEventListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(StudentEventListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id', None)
        if student_id:
            student = Student.objects.get(id=student_id)
            message = base64.b64encode(("""
                    $search = $("th[data-field='name'] input");
                    $search.val("%s, %s");
                    $search.trigger('keyup');
                    """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
            messages.add_message(request, settings.JS_MESSAGE, message)
        return super(StudentEventListView, self).get(request, *args, **kwargs)


class StudentEventDeleteView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentEventDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        ids_str = request.POST.get("ids", None)
        if ids_str == None:
            message = 'No se ha realizado ninguna acción.'
            messages.add_message(request, messages.ERROR, message)
            return redirect_view(StudentEventListView, request)
        ids = [int(id_int) for id_int in ids_str.split(",")]
        for id_int in ids:
            student_event = StudentEvent.objects.get(id=id_int)
            student = student_event.student
            student_event.delete()
            message = base64.b64encode(("""
                        $search = $("th[data-field='name'] input");
                        $search.val("%s, %s");
                        $search.trigger('keyup');
                        """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
            messages.add_message(request, settings.JS_MESSAGE, message)
            messages.add_message(request, messages.SUCCESS,
                                 'Se ha eliminado correctamente al evento de estudiante: %s.' % student_event)
        return redirect_view(StudentEventListView, request)


class StudentEventUpdateView(View):
    title = 'Actualizar Evento de Estudiante'
    template_name = 'student_event_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Eventos de Estudiantes", "/student_event/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentEventUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_student_event = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Actualizar Evento de Estudiante", "/student_event/%s/upgrade/" % id_student_event),)
        student_event = StudentEvent.objects.get(id=id_student_event)

        student_event_form = StudentEventForm(instance=student_event)

        context = {'action': self.action, 'id_student_event': student_event.id,
                   'student_event_form': student_event_form, 'title': self.title,
                   'student_event': student_event, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_student_event = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Actualizar Evento de Estudiante", "/student_event/%s/upgrade/" % id_student_event),)
        student_event = StudentEvent.objects.get(id=id_student_event)

        student_event_form = StudentEventForm(request.POST, instance=student_event)

        if student_event_form.is_valid():
            student_event = student_event_form.save(commit=False)
            student_event.state = "ENC"
            student_event.save()
            student = student_event.student

            message = 'Se ha actualizado correctamente al evento de estudiante %s.' % student_event
            messages.add_message(request, messages.SUCCESS, message)

            message = base64.b64encode(("""
                    $search = $("th[data-field='name'] input");
                    $search.val("%s, %s");
                    $search.trigger('keyup');
                    """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
            messages.add_message(request, settings.JS_MESSAGE, message)

            return redirect_view(StudentEventListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'id_student_event': student_event.id,
                       'student_event_form': student_event_form, 'title': self.title,
                       'student_event': student_event, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))


class StudentEventCreateView(View):
    title = 'Registrar Evento de Estudiante'
    template_name = 'student_event_form.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Eventos de Estudiantes", "/student_event/"),
        BreadCrumb("Registrar Evento de Estudiante", "/student_event/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentEventCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        student_event_form = StudentEventForm()
        event_type_id = kwargs.get("event_type_id", None)
        student_id = kwargs.get("student_id", None)

        context = {'action': self.action, 'student_event_form': student_event_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}

        if event_type_id:
            event_type = EventType.objects.get(id=event_type_id)
            student_type = event_type.student_type
            student_event_form = StudentEventForm(initial={'type': event_type})
            student_event_form.fields["student"].queryset = Student.objects.filter(type=student_type).order_by('id')
            context = dict(
                context.items() + {'student_type': student_type, 'student_event_form': student_event_form}.items())

        if student_id:
            student = Student.objects.get(id=student_id)
            student_event_form = StudentEventForm(initial={'student': student})
            student_event_form.fields["type"].queryset = EventType.objects.filter(
                Q(student_type=student.type) | Q(student_type="TOD")).order_by('id')
            context = dict(
                context.items() + {'student_type': student.type, 'student_event_form': student_event_form}.items())

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        student_event_form = StudentEventForm(request.POST)

        if student_event_form.is_valid():
            student_event = student_event_form.save(commit=False)
            student_event.state = "ENC"
            student_event.save()
            student = student_event.student

            message = 'Se ha creado correctamente al evento de estudiante %s.' % student_event
            messages.add_message(request, messages.SUCCESS, message)

            message = base64.b64encode(("""
                    $search = $("th[data-field='name'] input");
                    $search.val("%s, %s");
                    $search.trigger('keyup');
                    """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
            messages.add_message(request, settings.JS_MESSAGE, message)

            return redirect_view(StudentEventListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'student_event_form': student_event_form,
                       'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

            return render_to_response(self.template_name, RequestContext(request, context))


class StudentEventChangeStateView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudentEventChangeStateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        ids_str = request.POST.get("ids", None)
        if ids_str == None:
            message = 'No se ha realizado ninguna acción.'
            messages.add_message(request, messages.ERROR, message)
            return redirect_view(StudentEventListView, request)
        ids = [int(id_int) for id_int in ids_str.split(",")]
        try:
            for id_int in ids:
                student_event = StudentEvent.objects.get(id=id_int)
                student_event.state = kwargs['new_state']
                student_event.end_obs = request.POST['end_obs']
                student_event.save()
                message = 'Se ha actualizado correctamente al evento de estudiante %s.' % student_event
                messages.add_message(request, messages.SUCCESS, message)

                student = student_event.student
                message = base64.b64encode(("""
                        $search = $("th[data-field='name'] input");
                        $search.val("%s, %s");
                        $search.trigger('keyup');
                        """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
                messages.add_message(request, settings.JS_MESSAGE, message)
        except:
            message = 'Se ha producido un error al salvar el evento de estudiante %s.' % student_event
            messages.add_message(request, messages.ERROR, message)
        return redirect_view(StudentEventListView, request)


class StudiesListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        studies_array = Studies.objects.all().order_by('id')
        for studies in studies_array:
            std = {'id': studies.id,
                   'teacher': "%s" % studies.teacher,
                   'academic_level': "%s" % studies.academic_level,
                   'institute': studies.institute,
                   'title': studies.title,
                   'date_award': "%s" % studies.date_award.astimezone(ecu_tz).strftime("%d/%m/%y"),
                   'country': "%s" % studies.country,
                   'senescyt_id': "%s" % studies.senescyt_id,
                   'created': "%s" % studies.created.astimezone(ecu_tz).strftime("%d/%m/%y %H:%M"),
                   'created_by': "%s" % studies.created_by,
                   'modified': "%s" % studies.modified.astimezone(ecu_tz).strftime("%d/%m/%y %H:%M"),
                   'modified_by': "%s" % studies.modified_by}
            array.append(std)
        return JsonResponse(array, safe=False)


class StudiesListView(TemplateView):
    title = 'Listado de Estudios de Profesores'
    template_name = 'studies_list.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Estudios de Profesores", "/studies/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudiesListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_teacher = kwargs.get('teacher_id', None)
        if id_teacher:
            teacher = Teacher.objects.get(id=id_teacher)
            message = base64.b64encode(("""
                    $search = $("th[data-field='name'] input");
                    $search.val("%s, %s");
                    $search.trigger('keyup');
                    """ % (teacher.user.last_name, teacher.user.first_name)).encode('utf-8'))
            messages.add_message(request, settings.JS_MESSAGE, message)
        return super(StudiesListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudiesListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class StudiesDeleteView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudiesDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_studies = kwargs['pk']
        studies = Studies.objects.get(id=id_studies)
        studies.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Se ha eliminado correctamente al estudios del profesor: %s.' % studies)
        return redirect_view(StudiesListView, request)


class StudiesUpdateView(View):
    title = 'Actualizar Evento de Estudiante'
    template_name = 'studies_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Estudios de Profesores", "/studies/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudiesUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_studies = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Evento de Estudiante", "/studies/%s/upgrade/" % id_studies),)
        studies = Studies.objects.get(id=id_studies)

        studies_form = StudiesForm(instance=studies)

        context = {'action': self.action, 'id_studies': studies.id,
                   'studies_form': studies_form, 'title': self.title,
                   'studies': studies, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_studies = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Evento de Estudiante", "/studies/%s/upgrade/" % id_studies),)
        studies = Studies.objects.get(id=id_studies)

        studies_form = StudiesForm(request.POST, instance=studies)

        if studies_form.is_valid():
            studies_form.save()

            message = 'Se ha actualizado correctamente al estudios del profesor %s.' % studies
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(StudiesListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'id_studies': studies.id,
                       'studies_form': studies_form, 'title': self.title,
                       'studies': studies, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))


class StudiesCreateView(View):
    title = 'Registrar Estudios de Profesor'
    template_name = 'studies_form.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Estudios de Profesores", "/studies/"),
        BreadCrumb("Registrar Estudios de Profesor", "/studies/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(StudiesCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        studies_form = StudiesForm()
        teacher_id = kwargs.get('teacher_id', None)
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
            studies_form = StudiesForm(initial={'teacher': teacher})

        context = {'action': self.action, 'studies_form': studies_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        studies_form = StudiesForm(request.POST)

        if studies_form.is_valid():
            studies = studies_form.save()

            message = 'Se ha creado correctamente al estudios del profesor %s.' % studies
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(StudiesListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'studies_form': studies_form,
                       'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

            return render_to_response(self.template_name, RequestContext(request, context))


class EventsGroupListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        event_group_events = EventsGroup.objects.all().order_by('id')
        for event_group_event in event_group_events:
            std = {'id': event_group_event.id,
                   'name': "%s" % event_group_event.name,
                   'description': "%s" % event_group_event.description,
                   'student_type': event_group_event.get_student_type_display(),
                   'created': "%s" % event_group_event.created.astimezone(ecu_tz).strftime("%d/%m/%y %H:%M"),
                   'created_by': "%s" % event_group_event.created_by,
                   'modified': "%s" % event_group_event.modified.astimezone(ecu_tz).strftime("%d/%m/%y %H:%M"),
                   'modified_by': "%s" % event_group_event.modified_by}
            array.append(std)
        return JsonResponse(array, safe=False)


class EventsGroupListView(TemplateView):
    title = 'Listado de Grupos de Eventos'
    template_name = 'event_group_list.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Grupos de Eventos", "/event_group/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventsGroupListView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get_context_data(self, **kwargs):
        context = super(EventsGroupListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class EventsGroupDeleteView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventsGroupDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_event_group = kwargs['pk']
        event_group = EventsGroup.objects.get(id=id_event_group)
        event_group.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Se ha eliminado correctamente al grupo de evento: %s.' % event_group.name)
        return redirect_view(EventsGroupListView, request)


class EventsGroupUpdateView(View):
    title = 'Actualizar Grupo de Evento'
    template_name = 'event_group_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Grupos de Eventos", "/event_group/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventsGroupUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_event_group = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Actualizar Grupo de Evento", "/event_group/%s/upgrade/" % id_event_group),)
        event_group = EventsGroup.objects.get(id=id_event_group)
        event_relations = EventsGroupRelation.objects.filter(event_group=event_group).order_by("order")
        selected_event_types = [x.event_type for x in event_relations]
        selected_event_types_values = [x.id for x in selected_event_types]
        event_types = EventType.objects.exclude(id__in=selected_event_types_values)

        event_group_form = EventGroupForm(instance=event_group)

        context = {'action': self.action, 'id_event_group': event_group.id, 'event_types': event_types,
                   'event_group_form': event_group_form, 'title': self.title,
                   'selected_event_types': selected_event_types,
                   'event_group': event_group, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        id_event_group = kwargs['pk']
        self.breadCrumbEntries += (
            BreadCrumb("Actualizar Grupo de Evento", "/event_group/%s/upgrade/" % id_event_group),)
        event_group = EventsGroup.objects.get(id=id_event_group)

        event_group_form = EventGroupForm(request.POST, instance=event_group)

        if event_group_form.is_valid():
            event_group.events.clear()

            event_group.name = event_group_form.cleaned_data["name"]
            event_group.description = event_group_form.cleaned_data["description"]
            event_group.student_type = event_group_form.cleaned_data["student_type"]
            event_group.save()

            for x in range(0, len(request.POST.getlist('events'))):
                event_type = EventType.objects.get(id=request.POST.getlist('events')[x])
                EventsGroupRelation.objects.create(event_type=event_type, event_group=event_group,
                                                   order=x)

            message = 'Se ha actualizado correctamente al grupo de evento %s.' % (event_group.name)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(EventsGroupListView, request)
        else:
            selected_event_types = event_group.events.all()
            selected_event_types_values = event_group.events.all().values('id')
            event_types = EventType.objects.exclude(id__in=selected_event_types_values)
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'id_event_group': event_group.id, 'event_types': event_types,
                       'event_group_form': event_group_form, 'title': self.title,
                       'selected_event_types': selected_event_types,
                       'event_group': event_group, 'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))


class EventsGroupCreateView(View):
    title = 'Registrar Grupo de Eventos'
    template_name = 'event_group_form.djhtml'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Grupos de Eventos", "/event_group/"),
        BreadCrumb("Registrar Grupo de Eventos", "/event_group/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventsGroupCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        event_types = EventType.objects.all()
        event_group_form = EventGroupForm()
        context = {'action': self.action, 'event_types': event_types, 'title': self.title,
                   'event_group_form': event_group_form,
                   'breadCrumbEntries': self.breadCrumbEntries}

        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        event_group_form = EventGroupForm(request.POST)

        if event_group_form.is_valid():
            event_group = EventsGroup()
            event_group.name = event_group_form.cleaned_data["name"]
            event_group.description = event_group_form.cleaned_data["description"]
            event_group.student_type = event_group_form.cleaned_data["student_type"]
            event_group.save()

            for x in range(0, len(request.POST.getlist('events'))):
                event_type = EventType.objects.get(id=request.POST.getlist('events')[x])
                EventsGroupRelation.objects.create(event_type=event_type, event_group=event_group,
                                                   order=x)

            message = 'Se ha creado correctamente al grupo de evento %s.' % (event_group)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(EventsGroupListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            event_types = EventType.objects.all()

            context = {'action': self.action, 'event_group_form': event_group_form, 'event_types': event_types,
                       'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

            return render_to_response(self.template_name, RequestContext(request, context))


class AssignEventsGroupToStudentView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(AssignEventsGroupToStudentView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        event_group_id = kwargs['event_group_id']
        student_id = kwargs['student_id']
        event_group = EventsGroup.objects.get(id=event_group_id)
        student = Student.objects.get(id=student_id)

        # if StudentEventsGroupRelation.objects.filter(student=student,event_group=event_group).count() > 0:
        #    messages.add_message(request, messages.ERROR, 'No se ha asociado el grupo de evento: %s, al estudiante %s, pues ya esta asociación existe' % (event_group.name, student))
        #    return redirect_view(StudentsListView, request)

        egr = EventsGroupRelation.objects.filter(event_group=event_group).order_by("order")
        events = [eg.event_type for eg in egr]

        StudentEventsGroupRelation.objects.create(student=student, event_group=event_group)

        for event in events:
            StudentEvent.objects.create(type=event, student=student, state="ESP")

        messages.add_message(request, messages.SUCCESS,
                             'Se ha asociado correctamente el grupo de evento: %s, al estudiante %s' % (
                                 event_group.name, student))

        message = base64.b64encode(("""
                    $search = $("th[data-field='name'] input");
                    $search.val("%s, %s");
                    $search.trigger('keyup');
                    """ % (student.user.last_name, student.user.first_name)).encode('utf-8'))
        messages.add_message(request, settings.JS_MESSAGE, message)

        return redirect_view(StudentEventListView, request)


class EventsGroupOfStudentView(View):
    template_name = 'event_group_of_student.djhtml'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(EventsGroupOfStudentView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        student_id = kwargs['student_id']
        student = Student.objects.get(id=student_id)

        egr = StudentEventsGroupRelation.objects.filter(student=student).order_by("order")

        event_groups = [eg.event_group for eg in egr]

        context = {'event_groups': event_groups}

        return render_to_response(self.template_name, RequestContext(request, context))


class InstitutionListView(TemplateView):
    title = 'Listado de Cursos'
    template_name = 'course_list.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cursos", "/course/"),)

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class InstitutionListData(View):
    def get(self, request, *args, **kwargs):
        array = []
        courses = Institution.objects.all().order_by('id')
        for course in courses:
            level = ""
            if course.level > 0 and course.level < 7:
                level = toRoman(course.level)
            elif course.level == 7:
                level = "UTE"
            elif course.level == 0:
                level = "PRE"
            elif course.level == 12:
                level = "CE"
            std = {'id': course.id,
                   'career': "%s" % course.career,
                   'type': "%s" % course.get_type_display(),
                   'description': course.description,
                   'period': "%s" % course.period,
                   'semester': course.semester,
                   'level': level,
                   'parallel': course.parallel,
                   'quota': course.quota(),
                   'quota_payout': course.quota_payout(),
                   'max_quota': course.max_quota, }
            array.append(std)
        return JsonResponse(array, safe=False)


class InstitutionCreateView(View):
    title = 'Registrar Curso'
    template_name = 'course_form.djhtml'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cursos", "/course/"),
                         BreadCrumb("Crear Curso", "/course/new/"),)
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(InstitutionCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        course_form = InstitutionForm()
        context = {'action': self.action, 'course_form': course_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        course_form = InstitutionForm(request.POST)

        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.save()
            message = 'Se ha añadido correctamente el curso: %s-%s' % (request.POST['level'], request.POST['parallel'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(InstitutionListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'course_form': course_form, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class InstitutionUpdateView(View):
    title = 'Actualizar Curso'
    template_name = 'course_form.djhtml'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Cursos", "/course/"),)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(InstitutionUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        course_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Curso", "/course/%s/upgrade/" % course_id),)
        course = Institution.objects.get(id=course_id)
        course_form = InstitutionForm(instance=course)
        context = {'action': self.action, 'course_form': course_form, 'course_id': course.id, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render_to_response(self.template_name, RequestContext(request, context))

    def post(self, request, *args, **kwargs):
        course_id = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Curso", "/course/%s/upgrade/" % course_id),)
        course = Institution.objects.get(id=course_id)
        course_form = InstitutionForm(request.POST, instance=course)

        if course_form.is_valid():
            course_form.save()
            message = 'Se ha actualizado correctamente el curso: %s-%s' % (course.level, course.parallel)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(InstitutionListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'course_form': course_form, 'course_id': course.id, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render_to_response(self.template_name, RequestContext(request, context))


class InstitutionDeleteView(View):
    redirect_url = '/course/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(InstitutionDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_course = kwargs['pk']
        course = Institution.objects.get(id=id_course)
        course_name = "%s" % course
        course.delete()
        message = 'Se ha eliminado correctamente el curso: %s.' % course_name
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(InstitutionListView, request)


#######################################################
#
# Arturo Views
#
class MedicRecordCreateView(View):
    title = 'Historia Clínica'
    template_name = 'medic_form.html'
    action = 'CREATE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Consultas", "/medic/"),
        BreadCrumb("Nueva Consulta", "/medic/new/"))

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicRecordCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        medic_form = CreateMedicRecordForm(prefix="medico")
        try:
            id_register = kwargs['pk']
            paciente = SigiaMedicAppointment.objects.get(id=id_register).id_patient
            medic_form.fields["id_patient"].initial = paciente
            if SigiaMedicrecord.objects.filter(id_patient=paciente).exists():
                pacient = SigiaMedicrecord.objects.get(id_patient=paciente)
                return redirect('/medic/%s/consulta/new/' % pacient.id)
        except KeyError as e:
            print e
        personal_form = personal(prefix='personal_form', queryset=SigiaMedicPersonalBackground.objects.none())
        personal_fem_form = personal_fem(prefix='persona_fem_form',
                                         queryset=SigiaMedicPersonalBackground.objects.none())
        family_form = family(prefix='family_form', queryset=SigiaMedicFamilyBackground.objects.none())
        contacto_form = contacto(prefix='contacto_form', queryset=SigiaMedicContact.objects.none())
        context = {'action': self.action, 'medic_form': medic_form, 'title': self.title, 'formset': personal_form,
                   'breadCrumbEntries': self.breadCrumbEntries, 'personalFemForm': personal_fem_form,
                   'familyform': family_form, 'contacto_form': contacto_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        medic = CreateMedicRecordForm(request.POST, prefix='medico')
        personal_form = personal(request.POST, prefix='personal_form')
        personal_fem_form = personal_fem(request.POST, prefix='persona_fem_form')
        family_form = family(request.POST, prefix='family_form')
        contacto_form = contacto(request.POST, prefix='contacto_form')
        if medic.is_valid() and personal_form.is_valid() and personal_fem_form.is_valid() and family_form.is_valid() \
                and contacto_form.is_valid():
            nuevo = medic.save(commit=False)
            tiempo = request.POST['hora']
            nuevo.date = "%s %s" % (nuevo.date.date(), tiempo)
            nuevo.live = True
            nuevo.save()
            for form in personal_form.forms:
                control_save(form, nuevo)
            for form in personal_fem_form.forms:
                control_save(form, nuevo)
            for form in family_form.forms:
                control_save(form, nuevo)
            for form in contacto_form.forms:
                control_save(form, nuevo)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'medic_form': medic, 'title': self.title, 'formset': personal_form,
                       'breadCrumbEntries': self.breadCrumbEntries, 'personalFemForm': personal_fem_form,
                       'familyform': family_form, 'contacto_form': contacto_form}
            return render(request, self.template_name, context)
        message = 'Se ha creado correctamente el historial clínico'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(MedicRecordListView, request)


class UserLista(View):
    @staticmethod
    def get(request, *args, **kwargs):
        ids = request.GET.get('ids')
        if not ids:
            return JsonResponse({})
        pacientes = UserProfile.objects.get(user=ids)
        if pacientes.nationality is None:
            return JsonResponse(serializers.serialize('json', [pacientes, pacientes.user]),
                                safe=False)
        return JsonResponse(serializers.serialize('json', [pacientes, pacientes.user, pacientes.nationality,
                                                           pacientes.address_province, pacientes.address_canton]),
                            safe=False)


class Cie10Lista(View):
    @staticmethod
    def get(request, *args, **kwargs):
        q = request.GET.get('term', '')
        query = Q(id__contains=q) | Q(detail__contains=q)
        cie10 = SigiaMedicCie10.objects.filter(query)[:20]
        results = []
        for cie in cie10:
            cie_json = {}
            cie_json['id'] = cie.id
            cie_json['label'] = cie.detail
            cie_json['value'] = cie.detail
            results.append(cie_json)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


class MedicRecordListView(TemplateView):
    title = 'Historia Clínica'
    template_name = 'medic_list.html'
    action = 'LIST'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Historiales", "/medic/"))

    def get_context_data(self, **kwargs):
        context = super(MedicRecordListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class MedicRecordListData(View):
    def get(self, request, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, '')
        array = []
        records = SigiaMedicrecord.objects.all().order_by('id')
        for record in records:
            std = {'id': record.id,
                   'name': "%s %s" % (record.id_patient.last_name, record.id_patient.first_name),
                   'date': "%s" % record.date.strftime("%d de %B de %Y a las %H:%M"),
                   'actual': record.actual_problem}
            array.append(std)
        return JsonResponse(array, safe=False)


class MedicRecordDeleteView(View):
    redirect_url = '/medic/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicRecordDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        register = SigiaMedicrecord.objects.get(id=id_register)
        SigiaMedicPersonalBackground.objects.filter(id_sigia_medic_record=register).update(live=False)
        SigiaMedicFamilyBackground.objects.filter(id_sigia_medic_record=register).update(live=False)
        SigiaMedicContact.objects.filter(id_sigia_medic_record=register).update(live=False)
        register_1 = SigiaMedicConsulta.objects.get(id=id_register)
        SigiaMedicPhysicalExam.objects.filter(id_sigia_medic_record=register_1).update(live=False)
        SigiaMedicDiagnosticPlan.objects.filter(id_sigia_medic_record=register_1).update(live=False)
        SigiaMedicDiagnosticPresumptive.objects.filter(id_sigia_medic_record=register_1).update(live=False)
        register.delete()
        register_1.delete()
        message = 'Se ha eliminado correctamente el registro.'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(MedicRecordListView, request)


class MedicRecordUpdateView(View):
    title = 'Actualizar Historia Clínica'
    template_name = 'medic_form.html'
    action = 'UPGRADE'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Historiales", "/medic/"))

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicRecordUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Historial", "/medic/%s/upgrade/" % id_register),)
        register = SigiaMedicrecord.objects.get(id=id_register)
        fecha = register.date.date()
        hora = "%s:%s:%s" % (register.date.hour, register.date.minute, register.date.second)
        medic = CreateMedicRecordForm(prefix="medico", instance=register)
        personal_query = register.personal_background.filter(id__range=[1, 24]).all()
        personal_fem_query = register.personal_background.filter(id__range=[25, 41]).all()
        personal_form = personal(prefix='personal_form', instance=register, queryset=personal_query)
        personal_fem_form = personal_fem(prefix='persona_fem_form', instance=register, queryset=personal_fem_query)
        family_form = family(prefix='family_form', instance=register)
        contacto_form = contacto(prefix='contacto_form', instance=register)
        context = {'action': self.action, 'medic_form': medic, 'title': self.title, 'formset': personal_form,
                   'breadCrumbEntries': self.breadCrumbEntries, 'personalFemForm': personal_fem_form,
                   'familyform': family_form, 'contacto_form': contacto_form, "date1": fecha,
                   "hour": hora, "registro_id": register.id, "registro": register}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Historial", "/medic/%s/upgrade/" % id_register),)
        registro = SigiaMedicrecord.objects.get(id=id_register)
        medic = CreateMedicRecordForm(request.POST, prefix="medico", instance=registro)
        personal_form = personal(request.POST, prefix='personal_form', instance=registro)
        personal_fem_form = personal_fem(request.POST, prefix='persona_fem_form', instance=registro)
        family_form = family(request.POST, prefix='family_form', instance=registro)
        contacto_form = contacto(request.POST, prefix='contacto_form', instance=registro)
        if medic.is_valid() and personal_form.is_valid() and personal_fem_form.is_valid() and family_form.is_valid() \
                and contacto_form.is_valid():
            nuevo = medic.save(commit=False)
            tiempo = request.POST['hora']
            nuevo.date = "%s %s" % (nuevo.date.date(), tiempo)
            nuevo.live = True
            nuevo.save()
            for form in personal_form.forms:
                control_save_update(form, nuevo)
            for form in personal_fem_form.forms:
                control_save_update(form, nuevo)
            for form in family_form.forms:
                control_save_update(form, nuevo)
            for form in contacto_form.forms:
                control_save_update(form, nuevo)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'medic_form': medic, 'title': self.title, 'formset': personal_form,
                       'breadCrumbEntries': self.breadCrumbEntries, 'personalFemForm': personal_fem_form,
                       'familyform': family_form, 'contacto_form': contacto_form, "registro_id": registro.id,
                       "registro": registro}
            return render(request, self.template_name, context)
        message = 'Se ha actualizado correctamente el historial clínico'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(MedicRecordListView, request)


class MedicPatientCreateView(View):
    title = 'Registrar Paciente'
    template_name = 'medic_patient.html'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de pacientes", "/medic/patient/"),
                         BreadCrumb("Registrar Paciente", "/medic/patient/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicPatientCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        personal_info_form = UserPersonalInfoForm()
        context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                   'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}
        if not request.user.is_authenticated():
            captcha_form = CaptchaForm()
            context['captcha_form'] = captcha_form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        personal_info_form = UserPersonalInfoForm(request.POST, request.FILES)
        captcha_form = CaptchaForm(request.POST)
        if user_form.is_valid() and personal_info_form.is_valid():
            if not request.user.is_authenticated():
                if not captcha_form.is_valid():
                    message = 'Corrija el captcha antes de enviar el formulario.'
                    messages.add_message(request, messages.ERROR, message)
                    context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                               'captcha_form': captcha_form, 'title': self.title,
                               'breadCrumbEntries': self.breadCrumbEntries}
                    return render(request, self.template_name, context)
            user = user_form.save()
            userprofile = personal_info_form.save(commit=False)
            userprofile.user = user
            if not request.user.is_authenticated():
                user.is_active = False
            else:
                user.is_active = True
            userprofile.live = True
            grupo, created = Group.objects.get_or_create(name="paciente")
            user.groups.add(grupo)
            user.save()
            userprofile.save()
            message = 'Se ha añadido correctamente al paciente %s %s.' % (user.first_name, user.last_name)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(MedicPatientListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)

            context = {'action': self.action, 'user_form': user_form, 'personal_info_form': personal_info_form,
                       'captcha_form': captcha_form, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries}

            return render(request, self.template_name, context)


class MedicPatientListView(TemplateView):
    title = 'Listado de pacientes'
    template_name = 'medic_patient_list.html'
    action = 'LIST'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de pacientes", "/medic/patient/"))

    def get_context_data(self, **kwargs):
        context = super(MedicPatientListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class MedicPatientListData(View):
    def get(self, request, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, '')
        array = []
        records = Group.objects.get(name="paciente").user_set.filter(is_active=True).all()
        for record in records:
            std = {'id': record.id,
                   'name': "%s %s" % (record.last_name, record.first_name),
                   'date': "%s" % record.date_joined.strftime("%d de %B de %Y a las %H:%M")}
            array.append(std)
        return JsonResponse(array, safe=False)


class MedicPatientUpdateView(View):
    title = 'Actualizar Paciente'
    template_name = 'medic_patient.html'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de pacientes", "/medic/patient/"))

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicPatientUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_patient = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Paciente", "/medic/patient/%s/upgrade/" % id_patient),)
        user = User.objects.get(id=id_patient)
        profile = user.profile
        user_form = UserForm(instance=user)
        personal_info_form = UserPersonalInfoForm(instance=profile)

        context = {'action': self.action, 'user_form': user_form, 'id_patient': id_patient,
                   'personal_info_form': personal_info_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_patient = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Paciente", "/medic/patient/%s/upgrade/" % id_patient),)
        user = User.objects.get(id=id_patient)
        profile = user.profile

        user_form = UserForm(request.POST, instance=user)
        personal_info_form = UserPersonalInfoForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and personal_info_form.is_valid():
            user_form.save()
            personal_info_form.save()
            message = 'Se ha actualizado correctamente al paciente %s %s.' % (user.first_name, user.last_name)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(MedicPatientListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'user_form': user_form, 'id_student': id_patient,
                       'personal_info_form': personal_info_form, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render(request, self.template_name, context)


class MedicPatientDeleteView(View):
    redirect_url = '/medic/patient/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicPatientDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        register = User.objects.get(id=id_register)
        register.profile.delete()
        register.is_active = False
        register.save()
        message = 'Se ha eliminado correctamente el registro.'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(MedicPatientListView, request)


class MedicAppointmentListView(TemplateView):
    title = 'Listado de citas programadas'
    template_name = 'medic_patient_appointment_list.html'
    action = 'LIST'
    breadCrumbEntries = (
        BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de citas", "/medic/appointment/"))

    def get_context_data(self, **kwargs):
        context = super(MedicAppointmentListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        return context


class MedicAppointmentListData(View):
    def get(self, request, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, '')
        array = []
        records = SigiaMedicAppointment.objects.all().order_by('id')
        for record in records:
            std = {'id': record.id,
                   'name': "%s %s" % (record.id_patient.last_name, record.id_patient.first_name),
                   'date': "%s" % record.date.strftime("%d de %B de %Y a las %H:%M"),
                   'description': record.description,
                   'done': "Realizada" if record.done else "Sin Realizar"}
            array.append(std)
        return JsonResponse(array, safe=False)


class MedicAppointmentCreateView(View):
    title = 'Registrar cita'
    template_name = 'medic_appointment.html'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de citas", "/medic/appointment/"),
                         BreadCrumb("Registrar cita", "/medic/appointment/new/"))
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicAppointmentCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        user_form = PatientAppointment()
        context = {'action': self.action, 'user_form': user_form, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = PatientAppointment(request.POST)
        if user_form.is_valid():
            nuevo = user_form.save(commit=False)
            tiempo = request.POST['hora']
            nuevo.date = "%s %s" % (nuevo.date.date(), tiempo)
            nuevo.live = True
            nuevo.save()
            message = 'Se ha creado correctamente la cita'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(MedicAppointmentListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'user_form': user_form, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries}
            return render(request, self.template_name, context)


class MedicAppointmentUpdateView(View):
    title = 'Actualizar cita'
    template_name = 'medic_appointment.html'
    action = 'UPGRADE'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"),
                         BreadCrumb("Listado de pacientes", "/medic/appointment/"))

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicAppointmentUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_cita = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Paciente", "/medic/appointment/%s/upgrade/" % id_cita),)
        user = SigiaMedicAppointment.objects.get(id=id_cita)
        user_form = PatientAppointment(instance=user)
        context = {'action': self.action, 'user_form': user_form, 'registro_id': id_cita, 'title': self.title,
                   'breadCrumbEntries': self.breadCrumbEntries, 'registro': user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_cita = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Actualizar Paciente", "/medic/appointment/%s/upgrade/" % id_cita),)
        user = SigiaMedicAppointment.objects.get(id=id_cita)
        user_form = PatientAppointment(request.POST, instance=user)
        if user_form.is_valid():
            nuevo = user_form.save(commit=False)
            tiempo = request.POST['hora']
            nuevo.date = "%s %s" % (nuevo.date.date(), tiempo)
            nuevo.live = True
            nuevo.save()
            message = 'Se ha actualizado correctamente la cita'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect_view(MedicAppointmentListView, request)
        else:
            message = 'Por favor corrija los errores en el formulario'
            messages.add_message(request, messages.ERROR, message)
            context = {'action': self.action, 'user_form': user_form, 'registro_id': id_cita, 'title': self.title,
                       'breadCrumbEntries': self.breadCrumbEntries, 'registro': user}
            return render(request, self.template_name, context)


class MedicAppointmentDeleteView(View):
    redirect_url = '/medic/appointment/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicAppointmentDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        register = SigiaMedicAppointment.objects.get(id=id_register)
        register.delete()
        message = 'Se ha eliminado correctamente la cita.'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect_view(MedicAppointmentListView, request)


class MedicAppointmentRealize(View):
    redirect_url = '/medic/appointment/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicAppointmentRealize, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        register = SigiaMedicAppointment.objects.get(id=id_register)
        register.done = True
        register.save()
        return redirect('/medic/new/%s/' % id_register)


class MedicConsultaCreateView(View):
    title = 'Registrar Consulta'
    template_name = 'medic_form_consultas.html'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"),)
    action = 'CREATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicConsultaCreateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Listado de Consulta", "/medic/%s/consulta/" % id_register),
                                   BreadCrumb("Realizar Consulta", "/medic/%s/consulta/new" % id_register),)
        register = ConsultaForm(prefix='consulta')
        registro = SigiaMedicrecord.objects.get(id=id_register)
        nombre = "%s %s" % (registro.id_patient.last_name, registro.id_patient.first_name)
        register.fields["id_sigia_medic_record"].initial = registro
        fisico_form = fisico(prefix='physical_form', queryset=SigiaMedicPhysicalExam.objects.none())
        diagnostic_form = diagnostic(prefix='diagnostic_form', queryset=SigiaMedicDiagnosticPlan.objects.none())
        presumptive_form = presumptive(prefix='presumptive_form',
                                       queryset=SigiaMedicDiagnosticPresumptive.objects.none())
        prescription_form = prescription(prefix='prescription_form', queryset=SigiaMedicPrescription.objects.none())
        context = {'action': self.action, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries,
                   'fisico_form': fisico_form, 'diagnostic_form': diagnostic_form, 'name': nombre,
                   'prescription_form': prescription_form, 'presumptive_form': presumptive_form,
                   "registro_id": id_register, "consulta": register}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Listado de Consulta", "/medic/%s/consulta/" % id_register),
                                   BreadCrumb("Realizar Consulta", "/medic/%s/consulta/new" % id_register),)
        register = ConsultaForm(request.POST, prefix='consulta')
        fisico_form = fisico(request.POST, prefix='physical_form')
        diagnostic_form = diagnostic(request.POST, prefix='diagnostic_form')
        presumptive_form = presumptive(request.POST, prefix='presumptive_form')
        prescription_form = prescription(request.POST, prefix='prescription_form')
        if register.is_valid() and fisico_form.is_valid() and diagnostic_form.is_valid() \
                and presumptive_form.is_valid() and prescription_form.is_valid():
            nuevo = register.save(commit=False)
            nuevo.live = True
            nuevo.save()
            for form in fisico_form.forms:
                control_save(form, nuevo)
            for form in diagnostic_form.forms:
                control_save(form, nuevo)
            for form in presumptive_form.forms:
                control_save(form, nuevo)
            for form in prescription_form.forms:
                control_save(form, nuevo)
            message = 'Se ha creado correctamente la consulta'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('/medic/%s/consulta/' % id_register)
        registro = SigiaMedicrecord.objects.get(id=id_register)
        nombre = "%s %s" % (registro.id_patient.last_name, registro.id_patient.first_name)
        message = 'Por favor corrija los errores en el formulario'
        messages.add_message(request, messages.ERROR, message)
        context = {'action': self.action, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries,
                   'fisico_form': fisico_form, 'diagnostic_form': diagnostic_form, 'name': nombre,
                   'prescription_form': prescription_form, 'presumptive_form': presumptive_form,
                   "registro_id": id_register, "consulta": register}
        return render(request, self.template_name, context)


class MedicConsultaListView(TemplateView):
    title = 'Lista de consultas'
    template_name = 'medic_form_consultas_lista.html'
    action = 'LIST'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"), BreadCrumb("Listado de Historiales", "/medic/"))

    def get_context_data(self, **kwargs):
        id_register = kwargs['pk']
        self.breadCrumbEntries += (BreadCrumb("Listado de Consulta", "/medic/%s/consulta/" % id_register),)
        register = SigiaMedicrecord.objects.get(id=id_register)
        nombre = "%s %s" % (register.id_patient.last_name, register.id_patient.first_name)
        context = super(MedicConsultaListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['breadCrumbEntries'] = self.breadCrumbEntries
        context['id_registro'] = id_register
        context['name'] = nombre
        return context


class MedicConsultaListData(View):
    def get(self, request, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, '')
        array = []
        id_register = kwargs['pk']
        records = SigiaMedicrecord.objects.get(id=id_register).medic_consulta.all()
        for record in records:
            fisico = ""
            diagnostico = ""
            presumptive = ""
            for x in record.physical_exam.all():
                fisico += "%s <br>" % x.detail_background
            for x in record.diagnostic_plan.all():
                diagnostico += "%s <br>" % x.detail_background
            for x in record.diagnostic_presumptive.all():
                presumptive += "%s <br>" % x.detail_background
            std = {'id': record.id,
                   'actual': record.actual_problem,
                   'fisico': fisico,
                   'diagnostico': diagnostico,
                   'presumptive': presumptive}
            array.append(std)
        return JsonResponse(array, safe=False)


class MedicConsultaDeleteView(View):
    redirect_url = '/medic/appointment/'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicConsultaDeleteView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def post(self, request, *args, **kwargs):
        print kwargs
        id_register = kwargs['id_consulta']
        id_historial = kwargs['pk']
        register_1 = SigiaMedicConsulta.objects.get(id=id_register)
        SigiaMedicPhysicalExam.objects.filter(id_sigia_medic_record=register_1).update(live=False)
        SigiaMedicDiagnosticPlan.objects.filter(id_sigia_medic_record=register_1).update(live=False)
        SigiaMedicDiagnosticPresumptive.objects.filter(id_sigia_medic_record=register_1).update(live=False)
        register_1.delete()
        message = 'Se ha eliminado correctamente la consulta.'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('/medic/%s/consulta/' % id_historial)


class MedicConsultaUpdateView(View):
    title = 'Actualizar Consulta'
    template_name = 'medic_form_consultas.html'
    breadCrumbEntries = (BreadCrumb("Bienvenido", "/welcome/"),)
    action = 'UPDATE'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MedicConsultaUpdateView, cls).as_view(**initkwargs)
        return login_required(view, "/")

    def get(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        id_consulta = kwargs['id_consulta']
        self.breadCrumbEntries += (BreadCrumb("Listado de Consulta", "/medic/%s/consulta/" % id_register),
                                   BreadCrumb("Actualizar Consulta",
                                              "medic/%s/consulta/%s/upgrade/" % (id_register, id_consulta)),)
        consulta = SigiaMedicConsulta.objects.get(id=id_consulta)
        register = ConsultaForm(prefix='consulta', instance=consulta)
        registro = SigiaMedicrecord.objects.get(id=id_register)
        nombre = "%s %s" % (registro.id_patient.last_name, registro.id_patient.first_name)
        fisico_form = fisico(prefix='physical_form', instance=consulta)
        diagnostic_form = diagnostic(prefix='diagnostic_form', instance=consulta)
        presumptive_form = presumptive(prefix='presumptive_form', instance=consulta)
        prescription_form = prescription(prefix='prescription_form', instance=consulta)
        context = {'action': self.action, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries,
                   'fisico_form': fisico_form, 'diagnostic_form': diagnostic_form, 'name': nombre,
                   'presumptive_form': presumptive_form, "registro_id": id_register, "consulta": register,
                   "consulta_id": id_consulta, 'prescription_form': prescription_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_register = kwargs['pk']
        id_consulta = kwargs['id_consulta']
        self.breadCrumbEntries += (BreadCrumb("Listado de Consulta", "/medic/%s/consulta/" % id_register),
                                   BreadCrumb("Actualizar Consulta",
                                              "medic/%s/consulta/%s/upgrade/" % (id_register, id_consulta)),)
        consulta = SigiaMedicConsulta.objects.get(id=id_consulta)
        register = ConsultaForm(request.POST, prefix='consulta', instance=consulta)
        fisico_form = fisico(request.POST, prefix='physical_form', instance=consulta)
        diagnostic_form = diagnostic(request.POST, prefix='diagnostic_form', instance=consulta)
        presumptive_form = presumptive(request.POST, prefix='presumptive_form', instance=consulta)
        prescription_form = prescription(request.POST, prefix='prescription_form', instance=consulta)
        if register.is_valid() and fisico_form.is_valid() and diagnostic_form.is_valid() \
                and presumptive_form.is_valid() and prescription_form.is_valid():
            nuevo = register.save(commit=False)
            nuevo.live = True
            nuevo.save()
            for form in fisico_form.forms:
                control_save_update(form, nuevo)
            for form in diagnostic_form.forms:
                control_save_update(form, nuevo)
            for form in presumptive_form.forms:
                control_save_update(form, nuevo)
            for form in prescription_form.forms:
                control_save_update(form, nuevo)
            message = 'Se ha actualizado correctamente la consulta'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('/medic/%s/consulta/' % id_register)
        registro = SigiaMedicrecord.objects.get(id=id_register)
        nombre = "%s %s" % (registro.id_patient.last_name, registro.id_patient.first_name)
        message = 'Por favor corrija los errores en el formulario'
        messages.add_message(request, messages.ERROR, message)
        context = {'action': self.action, 'title': self.title, 'breadCrumbEntries': self.breadCrumbEntries,
                   'fisico_form': fisico_form, 'diagnostic_form': diagnostic_form, 'name': nombre,
                   'presumptive_form': presumptive_form, "registro_id": id_register, "consulta": register,
                   "consulta_id": id_consulta, 'prescription_form': prescription_form}
        return render(request, self.template_name, context)
