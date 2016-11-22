from django.contrib import admin

from sigia.models import UserProfile, Student, Teacher, Career, Course, Matter,\
    Enrollment, Studies, Country, Province, Canton, Parish, Period, PaymentOrder,\
    BugReport, EventType, StudentEvent, Institution, EthnicGroup, SigiaMedicalCenter

admin.site.register(UserProfile)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Career)
admin.site.register(Course)
admin.site.register(Matter)
admin.site.register(Enrollment)
admin.site.register(Studies)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Canton)
admin.site.register(Parish)
admin.site.register(Period)
admin.site.register(PaymentOrder)
admin.site.register(BugReport)
admin.site.register(EventType)
admin.site.register(StudentEvent)
admin.site.register(Institution)
admin.site.register(EthnicGroup)
admin.site.register(SigiaMedicalCenter)
