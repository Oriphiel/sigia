# -*- coding: utf-8 -*-
'''
Created on 29/12/2014

@author: Dario
'''
from django.core.mail import send_mass_mail
from django.http.response import HttpResponse
from time import sleep
from datetime import datetime as dt
import os
from sigia.settings import BASE_DIR


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def send_emails(emails, log):
    chunk_size = 190
    f = open(os.path.abspath(os.path.join(BASE_DIR, 'sigia_email.log')), 'a')
    f.write("%s: Inicio de Envío de Correo Masivo\n" % dt.now().strftime("%H:%m - %d/%m/%Y"))
    f.write("Cantidad total de archivos a enviar: %d\n" % len(emails))
    f.write("Tamaño de los segmentos: %d\n" % chunk_size)
    i = 1
    for chunk in chunks(emails, chunk_size):
        f.write("%s: Inicio de Envío del Grupo No.: %d\n" % (dt.now().strftime("%H:%m - %d/%m/%Y"), i))
        f.write("Enviando correo a:\n")
        for email in chunk:
            f.write("%s\n" % email[3][0])
        try:
            result = send_mass_mail(chunk, fail_silently=False)
            f.write("%s: Fin de Envío de Grupo No.: %d\n" % (dt.now().strftime("%H:%m - %d/%m/%Y"), i))
            f.write("Se enviaron correctamente: %d de: %d\n" % (result, chunk_size))
        except Exception as ex:
            f.write("Error: %s\n" % ex)
            log.send_success = False
            log.save()
        sleep(60 * 60 + 60)
        i += 1
    f.close()


def convert_enrrollment_type_to_payment_concept(enrrollment_type):
    if enrrollment_type == 'ORD':
        return 'MORD'
    elif enrrollment_type == 'EXT':
        return 'MEXT'
    elif enrrollment_type == 'ESP':
        return 'MESP'
    elif enrrollment_type == 'SBA':
        return 'SBAC'
    elif enrrollment_type == 'ENE':
        return 'ENES'
    elif enrrollment_type == 'PRE':
        return 'PRET'
    elif enrrollment_type == 'ECO':
        return 'EDCO'


def case_insensitive_key(a, k):
    k = k.lower()
    return [a[key] for key in a if key.lower() == k]


class BreadCrumb:
    name = ""
    link = ""

    def __init__(self, name, link):
        self.name = name
        self.link = link

    def to_html(self):
        return "<li><a class=\"ajax-link\" href='%s'>%s</a></li>" % (self.link, self.name)

    def __unicode__(self):
        return "%s" % self.name


def cedula_valida(cedula):
    NUMERO_DE_PROVINCIAS = 24
    if not cedula.isdigit() or len(cedula) != 10:
        return False
    prov = int(cedula[:2])
    if not (prov > 0 and prov <= NUMERO_DE_PROVINCIAS):
        return False

    suma = 0

    for i in range(0, 9):
        if (i + 1) % 2 == 0:
            suma += int(cedula[i])
        else:
            suma += int(cedula[i]) * 2 if int(cedula[i]) * 2 <= 9 else (int(cedula[i]) * 2) - 9
    d10 = int(str(suma + 10)[:1] + "0") - suma
    if d10 == 10:
        d10 = 0

    return d10 == int(cedula[9])
