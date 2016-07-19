"""
    File name: medic_tables
    Author: Edgar Arturo Haas Pacheco
    Date created: 14/7/2016
    Python Version: 2.7.11
"""
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from sigia.models import SigiaMedicPersonalBackgroundDetail, SigiaMedicFamilyBackgroundDetail
from django.contrib.auth.models import User
from django.utils import timezone
import codecs
from django.core.files import File
import sigia.settings as settings
import os


class Command(BaseCommand):
    args = '<none>'
    help = 'our help string comes here franklin'
    user = User.objects.get(username='franklin')
    date = timezone.now()

    def _create_personal_background(self):
        lista = []
        lista_detalle = ['VACUNAS', 'ENF. PERNATAL', 'ENF. INFANCIA', 'ENF. ADOLESCENCIA', 'ENF. ALERGICA',
                         'ENF. CARDIACA', 'ENF. RESPIRATORIA', 'ENF. DIGESTIVA', 'ENF. NEUROLOGICA', 'ENF. METABOLICA',
                         'ENF. HEMO LINF.', 'ENF. URINARIA', 'ENF. TRAUMATICA',
                         'ENF. QUIRURGICA', 'ENF. MENTAL', 'ENF. TRANGM SEX', 'TENDENCIA SEXUAL', 'RIESGO SOCIAL',
                         'RIESGO LABORAL', 'RIESGO FAMILIAR', 'ACTIVIDAD FISICA', 'DIETA Y HABITOS',
                         'RELIGION Y CULTURA', 'OTRO', 'MENARQUA', 'MENOPAUSIA', 'CICLOS', 'VIDA SEXUAL ACTIVA',
                         'GESTA', 'PARTOS', 'ABORTOS', 'CESAREAS', 'HIJOS VIVOS', 'FUM', 'FUP', 'FUC', 'BIOCOPIA',
                         'METODO DE P. FAMILIAR', 'TERAPIA HORMONAL', 'COLPOS COPIA', 'MAMOGRAFIA']
        for detalle in lista_detalle:
            lista.append(SigiaMedicFamilyBackgroundDetail(detail=detalle, created=self.date, modified=self.date,
                                                          created_by=self.user,
                                                          modified_by=self.user))
        SigiaMedicPersonalBackgroundDetail.objects.bulk_create(lista)

    def _create_family_background(self):
        lista = []
        lista_Detalle = ['CARDIOPAT', 'DIABETES', 'ENF. C. VASCULAR', 'HIPERTENSION', 'CANCER', 'TUBERCULOSIS',
                         'ENF. MENTAL', 'ENF. INFECCIOSA', 'MALFORMACION', 'OTRO']
        for detalle in lista_Detalle:
            lista.append(SigiaMedicFamilyBackgroundDetail(detail=detalle, created=self.date, modified=self.date,
                                                          created_by=self.user, modified_by=self.user))
        SigiaMedicFamilyBackgroundDetail.objects.bulk_create(lista)

    def handle(self, *args, **options):
        # self._create_personal_background()
        self._create_family_background()