from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from sigia.settings import BASE_DIR
import os

from views import LoginView, WelcomeView, LogoutView, StudentCreateView, StudentDeleteView, StudentsListView, \
    StudentsListData, \
    StudentUpdateView, CareerCreateView, CareerListView, CareerListData, CareerDeleteView, CareerUpdateView, \
    CourseListView, \
    CourseCreateView, CourseListData, CourseDeleteView, CourseUpdateView, EnrollmentCreateView, EnrollmentListView, \
    EnrollmentListData, \
    EnrollmentDeleteView, EnrollmentUpdateView, PeriodCreateView, PeriodListView, PeriodListData, \
    PeriodDeleteView, PeriodUpdateView, PaymentOrderCreateView, PaymentOrderListView, PaymentOrderListData, \
    PaymentOrderDeleteView, PaymentOrderUpdateView, GenerateEnrollmentBookView, PaymentOrderCancelView, \
    GetCantonByProvince, GetParishByCanton, GetProvincesByCountry, RootView, OnlineEnrollmentSuccessView, \
    EthnicGroupCreateView, \
    EthnicGroupListView, EthnicGroupListData, EthnicGroupDeleteView, EthnicGroupUpdateView, \
    PeriodActivateView, PeriodTerminateView, UserUpdateView, SetScholarshipView, \
    BugReportListView, BugReportCreateView, BugReportListData, \
    BugReportDeleteView, BugReportUpdateView, CountryListView, CountryCreateView, \
    CountryListData, CountryDeleteView, CountryUpdateView, ProvinceListView, \
    ProvinceCreateView, ProvinceListData, ProvinceDeleteView, ProvinceUpdateView, \
    CantonListView, CantonCreateView, CantonListData, CantonDeleteView, \
    CantonUpdateView, ParishListView, ParishCreateView, ParishListData, \
    ParishDeleteView, ParishUpdateView, ReducedStudentCreateView, \
    TeacherListView, TeacherCreateView, TeacherListData, TeacherDeleteView, \
    TeacherUpdateView, UserListData, EventTypeListView, EventTypeCreateView, EventTypeListData, EventTypeDeleteView, \
    EventTypeUpdateView, StudentEventListView, StudentEventCreateView, StudentEventListData, StudentEventDeleteView, \
    StudentEventUpdateView, StudentEventChangeStateView, StudiesListView, StudiesCreateView, StudiesListData, \
    StudiesDeleteView, StudiesUpdateView, ReportView, EventsGroupListView, EventsGroupCreateView, EventsGroupListData, \
    EventsGroupDeleteView, EventsGroupUpdateView, AssignEventsGroupToStudentView, EventsGroupOfStudentView, \
    EmailBulkListView, TeachersAndAdminsListData, SendEmailView, SendWelcomeEmailView, MedicRecordCreateView, UserLista, \
    Cie10Lista

urlpatterns = [
    # Examples:
    # url(r'^$', 'sigia.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^$', RootView.as_view(), name='index'),
    url(r'^favicon.ico$', RedirectView.as_view(url='static/img/favicon.ico', permanent=False),
        name='favicon'),
    url(r'^welcome/$', WelcomeView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),

    url(r'^api/provinces/by_country/(?P<pk>[^/]+)/$', GetProvincesByCountry.as_view()),
    url(r'^api/parishes/by_canton/(?P<pk>[^/]+)/$', GetParishByCanton.as_view()),
    url(r'^api/cantons/by_province/(?P<pk>[^/]+)/$', GetCantonByProvince.as_view()),

    url(r'^students/$', StudentsListView.as_view()),
    url(r'^students/new/$', StudentCreateView.as_view()),
    url(r'^students/api/list/$', StudentsListData.as_view()),
    url(r'^students/api/list/student_type/(?P<student_type>[^/]+)/$', StudentsListData.as_view()),
    url(r'^students/(?P<pk>[^/]+)/delete/$', StudentDeleteView.as_view()),
    url(r'^students/(?P<pk>[^/]+)/upgrade/$', StudentUpdateView.as_view()),

    url(r'^teachers_admins/api/list/$', TeachersAndAdminsListData.as_view()),

    url(r'^reports/$', ReportView.as_view()),

    url(r'^user/api/list/$', UserListData.as_view()),

    url(r'^reduced_students/new/$', ReducedStudentCreateView.as_view()),

    url(r'^teacher/$', TeacherListView.as_view()),
    url(r'^teacher/new/$', TeacherCreateView.as_view()),
    url(r'^teacher/api/list/$', TeacherListData.as_view()),
    url(r'^teacher/(?P<pk>[^/]+)/delete/$', TeacherDeleteView.as_view()),
    url(r'^teacher/(?P<pk>[^/]+)/upgrade/$', TeacherUpdateView.as_view()),

    url(r'^event_type/$', EventTypeListView.as_view()),
    url(r'^event_type/new/$', EventTypeCreateView.as_view()),
    url(r'^event_type/api/list/$', EventTypeListData.as_view()),
    url(r'^event_type/(?P<pk>[^/]+)/delete/$', EventTypeDeleteView.as_view()),
    url(r'^event_type/(?P<pk>[^/]+)/upgrade/$', EventTypeUpdateView.as_view()),

    url(r'^event_group/$', EventsGroupListView.as_view()),
    url(r'^event_group/new/$', EventsGroupCreateView.as_view()),
    url(r'^event_group/api/list/$', EventsGroupListData.as_view()),
    url(r'^event_group/(?P<pk>[^/]+)/delete/$', EventsGroupDeleteView.as_view()),
    url(r'^event_group/(?P<pk>[^/]+)/upgrade/$', EventsGroupUpdateView.as_view()),
    url(r'^event_group/assign/(?P<event_group_id>[^/]+)/to_student/(?P<student_id>[^/]+)/$',
        AssignEventsGroupToStudentView.as_view()),

    url(r'^event_group/of_student/(?P<student_id>[^/]+)/$', EventsGroupOfStudentView.as_view()),

    url(r'^student_event/$', StudentEventListView.as_view()),
    url(r'^student_event/student/(?P<student_id>[^/]+)/$', StudentEventListView.as_view()),
    url(r'^student_event/new/$', StudentEventCreateView.as_view()),
    url(r'^student_event/new/event_type/(?P<event_type_id>[^/]+)/$',
        StudentEventCreateView.as_view()),
    url(r'^student_event/new/for_student/(?P<student_id>[^/]+)/$', StudentEventCreateView.as_view()),
    url(r'^student_event/api/list/$', StudentEventListData.as_view()),
    url(r'^student_event/change_state/(?P<new_state>[^/]+)/$',
        StudentEventChangeStateView.as_view()),
    url(r'^student_event/delete/$', StudentEventDeleteView.as_view()),
    url(r'^student_event/(?P<pk>[^/]+)/upgrade/$', StudentEventUpdateView.as_view()),

    url(r'^studies/$', StudiesListView.as_view()),
    url(r'^studies/new/$', StudiesCreateView.as_view()),
    url(r'^studies/new/teacher/(?P<teacher_id>[^/]+)/$', StudiesCreateView.as_view()),
    url(r'^studies/api/list/$', StudiesListData.as_view()),
    url(r'^studies/teacher/(?P<teacher_id>[^/]+)/$', StudiesListView.as_view()),
    url(r'^studies/(?P<pk>[^/]+)/delete/$', StudiesDeleteView.as_view()),
    url(r'^studies/(?P<pk>[^/]+)/upgrade/$', StudiesUpdateView.as_view()),

    url(r'^ethnic_group/$', EthnicGroupListView.as_view()),
    url(r'^ethnic_group/new/$', EthnicGroupCreateView.as_view()),
    url(r'^ethnic_group/api/list/$', EthnicGroupListData.as_view()),
    url(r'^ethnic_group/(?P<pk>[^/]+)/delete/$', EthnicGroupDeleteView.as_view()),
    url(r'^ethnic_group/(?P<pk>[^/]+)/upgrade/$', EthnicGroupUpdateView.as_view()),

    url(r'^user/(?P<pk>[^/]+)/upgrade/$', UserUpdateView.as_view()),

    url(r'^period/$', PeriodListView.as_view()),
    url(r'^period/new/$', PeriodCreateView.as_view()),
    url(r'^period/api/list/$', PeriodListData.as_view()),
    url(r'^period/(?P<pk>[^/]+)/delete/$', PeriodDeleteView.as_view()),
    url(r'^period/(?P<pk>[^/]+)/activate/$', PeriodActivateView.as_view()),
    url(r'^period/(?P<pk>[^/]+)/terminate/$', PeriodTerminateView.as_view()),
    url(r'^period/(?P<pk>[^/]+)/upgrade/$', PeriodUpdateView.as_view()),

    url(r'^career/$', CareerListView.as_view()),
    url(r'^career/new/$', CareerCreateView.as_view()),
    url(r'^career/api/list/$', CareerListData.as_view()),
    url(r'^career/(?P<pk>[^/]+)/delete/$', CareerDeleteView.as_view()),
    url(r'^career/(?P<pk>[^/]+)/upgrade/$', CareerUpdateView.as_view()),

    url(r'^country/$', CountryListView.as_view()),
    url(r'^country/new/$', CountryCreateView.as_view()),
    url(r'^country/api/list/$', CountryListData.as_view()),
    url(r'^country/(?P<pk>[^/]+)/delete/$', CountryDeleteView.as_view()),
    url(r'^country/(?P<pk>[^/]+)/upgrade/$', CountryUpdateView.as_view()),

    url(r'^province/$', ProvinceListView.as_view()),
    url(r'^province/new/$', ProvinceCreateView.as_view()),
    url(r'^province/api/list/$', ProvinceListData.as_view()),
    url(r'^province/(?P<pk>[^/]+)/delete/$', ProvinceDeleteView.as_view()),
    url(r'^province/(?P<pk>[^/]+)/upgrade/$', ProvinceUpdateView.as_view()),

    url(r'^canton/$', CantonListView.as_view()),
    url(r'^canton/new/$', CantonCreateView.as_view()),
    url(r'^canton/api/list/$', CantonListData.as_view()),
    url(r'^canton/(?P<pk>[^/]+)/delete/$', CantonDeleteView.as_view()),
    url(r'^canton/(?P<pk>[^/]+)/upgrade/$', CantonUpdateView.as_view()),

    url(r'^parish/$', ParishListView.as_view()),
    url(r'^parish/new/$', ParishCreateView.as_view()),
    url(r'^parish/api/list/$', ParishListData.as_view()),
    url(r'^parish/(?P<pk>[^/]+)/delete/$', ParishDeleteView.as_view()),
    url(r'^parish/(?P<pk>[^/]+)/upgrade/$', ParishUpdateView.as_view()),

    url(r'^bug_report/$', BugReportListView.as_view()),
    url(r'^bug_report/new/$', BugReportCreateView.as_view()),
    url(r'^bug_report/api/list/$', BugReportListData.as_view()),
    url(r'^bug_report/(?P<pk>[^/]+)/delete/$', BugReportDeleteView.as_view()),
    url(r'^bug_report/(?P<pk>[^/]+)/upgrade/$', BugReportUpdateView.as_view()),

    url(r'^course/$', CourseListView.as_view()),
    url(r'^course/new/$', CourseCreateView.as_view()),
    url(r'^course/api/list/$', CourseListData.as_view()),
    url(r'^course/(?P<pk>[^/]+)/delete/$', CourseDeleteView.as_view()),
    url(r'^course/(?P<pk>[^/]+)/upgrade/$', CourseUpdateView.as_view()),

    url(r'^email/students/$', EmailBulkListView.as_view()),

    url(r'^enrollment/$', EnrollmentListView.as_view()),
    url(r'^enrollment/student/(?P<student_id>[^/]+)/$', EnrollmentListView.as_view()),
    url(r'^enrollment/new/$', EnrollmentCreateView.as_view()),
    url(r'^enrollment/new/student/(?P<pk>[^/]+)/$', EnrollmentCreateView.as_view()),
    url(r'^enrollment/api/list/$', EnrollmentListData.as_view()),
    url(r'^enrollment/(?P<pk>[^/]+)/delete/$', EnrollmentDeleteView.as_view()),
    url(r'^enrollment/(?P<pk>[^/]+)/upgrade/$', EnrollmentUpdateView.as_view()),
    url(r'^enrollment/(?P<pk>[^/]+)/assign_scholarship/$', SetScholarshipView.as_view()),
    url(r'^enrollment/set_scholarship/$',
        TemplateView.as_view(template_name='set_scholarship_form.djhtml')),
    url(r'^enrollment/generate_enrollment_book/$', GenerateEnrollmentBookView.as_view()),

    url(r'^payment_order/$', PaymentOrderListView.as_view()),
    url(r'^payment_order/student/(?P<student_id>[^/]+)/$', PaymentOrderListView.as_view()),
    url(r'^payment_order/new/$', PaymentOrderCreateView.as_view()),
    url(r'^payment_order/new/student/(?P<student_id>[^/]+)/$', PaymentOrderCreateView.as_view()),
    url(r'^payment_order/api/list/$', PaymentOrderListData.as_view()),
    url(r'^payment_order/(?P<pk>[^/]+)/delete/$', PaymentOrderDeleteView.as_view()),
    url(r'^payment_order/(?P<pk>[^/]+)/cancel/$', PaymentOrderCancelView.as_view()),
    url(r'^payment_order/(?P<pk>[^/]+)/upgrade/$', PaymentOrderUpdateView.as_view()),

    url(r'^send_email/$', SendEmailView.as_view()),
    url(r'^email/welcome_students/$', SendWelcomeEmailView.as_view()),

    url(r'^under_construction/$', TemplateView.as_view(template_name='under_construction.djhtml')),
    url(r'^online_enrollment_success/$', OnlineEnrollmentSuccessView.as_view()),

    url(r'^help/$', TemplateView.as_view(template_name='help.djhtml')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.djhtml')),
    url(r'^not_implemented/$', TemplateView.as_view(template_name='not_implemented.djhtml')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(BASE_DIR, 'media'),
         'show_indexes': True}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(BASE_DIR, 'static'),
         'show_indexes': True}),

    url(r'^hola/$', MedicRecordCreateView.as_view()),
    url(r'^api/medic/cie10/$', Cie10Lista.as_view()),
    url(r'^user/api/lista/$', UserLista.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
