# -*- coding: utf-8 -*-
"""
    File name: medic_tables
    Author: Edgar Arturo Haas Pacheco
    Date created: 14/7/2016
    Python Version: 2.7.11
"""
import json
import os

from django.core.management.base import BaseCommand

from sigia.dev_settings import BASE_DIR
from sigia.models import SigiaMedicPersonalBackgroundDetail, SigiaMedicFamilyBackgroundDetail, \
    SigiaMedicPhysicalExamDetail, SigiaMedicDiagnosticPlanDetail, SigiaMedicCie10
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    args = '<none>'
    help = 'our help string comes here franklin'
    user = User.objects.get(username='franklin')
    date = timezone.now()

    def _create_personal_background(self):
        lista = []
        lista_detalle = ['VACUNAS', 'ENF. PRENATAL', 'ENF. INFANCIA', 'ENF. ADOLESCENCIA', 'ENF. ALÉRGICA',
                         'ENF. CARDIACA', 'ENF. RESPIRATORIA', 'ENF. DIGESTIVA', 'ENF. NEUROLÓGICA', 'ENF. METABÓLICA',
                         'ENF. HEMO LINF.', 'ENF. URINARIA', 'ENF. TRAUMÁTICA',
                         'ENF. QUIRÚRGICA', 'ENF. MENTAL', 'ENF. TRANGM SEX', 'TENDENCIA SEXUAL', 'RIESGO SOCIAL',
                         'RIESGO LABORAL', 'RIESGO FAMILIAR', 'ACTIVIDAD FÍSICA', 'DIETA Y HÁBITOS',
                         'RELIGION Y CULTURA', 'OTRO', 'MENARQUA', 'MENOPAUSIA', 'CICLOS', 'VIDA SEXUAL ACTIVA',
                         'GESTA', 'PARTOS', 'ABORTOS', 'CESÁREAS', 'HIJOS VIVOS', 'FUM', 'FUP', 'FUC', 'BIOCOPIA',
                         'MÉTODO DE P. FAMILIAR', 'TERAPIA HORMONAL', 'COLPOS COPIA', 'MAMOGRAFÍA']
        for detalle in lista_detalle:
            lista.append(SigiaMedicFamilyBackgroundDetail(detail=detalle, created=self.date, modified=self.date,
                                                          created_by=self.user,
                                                          modified_by=self.user))
        SigiaMedicPersonalBackgroundDetail.objects.bulk_create(lista)

    def _create_family_background(self):
        lista = []
        lista__detalle = ['CARDIOPATÍA', 'DIABETES', 'ENF. C. VASCULAR', 'HIPERTENSIÓN', 'CANCER', 'TUBERCULOSIS',
                          'ENF. MENTAL', 'ENF. INFECCIOSA', 'MALFORMACIÓN', 'OTRO']
        for detalle in lista__detalle:
            lista.append(SigiaMedicFamilyBackgroundDetail(detail=detalle, created=self.date, modified=self.date,
                                                          created_by=self.user, modified_by=self.user))
        SigiaMedicFamilyBackgroundDetail.objects.bulk_create(lista)

    def _create_physical_background(self):
        lista = []
        lista_detalle1 = ['PIEL Y FANERAS', 'CABEZA', 'OJOS', 'OÍDOS', 'NARIZ', 'BOCA', 'ORO FARINGE', 'CUELLO',
                          'AXILAS - MAMAS', 'TÓRAX', 'ABDOMEN', 'COLUMNA VERTEBRAL', 'INGLE PERINE',
                          'MIEMBROS SUPERIORES', 'MIEMBROS SUPERIORES', 'ÓRGANO DE LOS SENTIDOS', 'RESPIRATORIO',
                          'CARDIO VASCULAR', 'DIGESTIVO', 'GENITAL', 'URINARIO', 'MUSCULO ESQUELÉTICO', 'ENDOCRINO',
                          'HEMO LINFÁTICO', 'NEUROLÓGICO']
        for detalle in lista_detalle1:
            lista.append(SigiaMedicPhysicalExamDetail(detail=detalle, created=self.date, modified=self.date,
                                                      created_by=self.user, modified_by=self.user))
        SigiaMedicPhysicalExamDetail.objects.bulk_create(lista)

    def _create_diagnostic_background(self):
        lista = []
        lista_detalle2 = ['BIOMETRÍA', 'UROANALISIS', 'QUÍMICA BAN..', 'ELECTROLITOS', 'GASOMETRÍA',
                          'ELECTRO CARDIOGRAMA', 'ENDOSCOPIA', 'R-X TÓRAX', 'R-X ABDOMEN', 'R-X ÓSEA', 'TOMOGRAFÍA',
                          'RESONANCIA', 'ECOGRAFÍA PÉLVICA', 'ECOGRAFÍA ABDOMEN', 'INTERCONSULTA', 'OTROS']
        for detalle in lista_detalle2:
            lista.append(SigiaMedicDiagnosticPlanDetail(detail=detalle, created=self.date, modified=self.date,
                                                        created_by=self.user, modified_by=self.user))
        SigiaMedicDiagnosticPlanDetail.objects.bulk_create(lista)

    @staticmethod
    def _create_cie10_rows():
        lista = []
        base = os.path.dirname(os.path.dirname(__file__))
        data = open(BASE_DIR + '\sigia\static\data\cie10.json').read()
        json_data = json.loads(data)
        for row in json_data:
            lista.append(SigiaMedicCie10(id=row['c'], detail=row['d']))
        SigiaMedicCie10.objects.bulk_create(lista)

    def handle(self, *args, **options):
        # self._create_personal_background()
        # self._create_family_background()
        # self._create_physical_background()
        # self._create_diagnostic_background()
        self._create_cie10_rows()
