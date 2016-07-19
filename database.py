# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AntCur02(models.Model):
    periodo = models.CharField(max_length=4, blank=True, null=True)
    cod_niv = models.CharField(max_length=2, blank=True, null=True)
    cod_cur = models.CharField(max_length=5, blank=True, null=True)
    des_cur = models.CharField(max_length=60, blank=True, null=True)
    abr_cur = models.CharField(max_length=20, blank=True, null=True)
    des_bac = models.CharField(max_length=30, blank=True, null=True)
    cod_pro = models.CharField(max_length=4, blank=True, null=True)
    nom_pro = models.CharField(max_length=40, blank=True, null=True)
    fec_cre = models.DateField(blank=True, null=True)
    cup_max = models.SmallIntegerField(blank=True, null=True)
    alu_mat = models.SmallIntegerField(blank=True, null=True)
    alu_ret = models.SmallIntegerField(blank=True, null=True)
    fec_cie = models.DateField(blank=True, null=True)
    fec_max = models.DateField(blank=True, null=True)
    cur_niv = models.CharField(max_length=1, blank=True, null=True)
    cen_cos = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ant_cur02'


class AntDoc02(models.Model):
    periodo = models.CharField(max_length=4, blank=True, null=True)
    cod_niv = models.CharField(max_length=2, blank=True, null=True)
    cod_est = models.CharField(max_length=6, blank=True, null=True)
    cod_rub = models.CharField(max_length=3, blank=True, null=True)
    val_doc = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    val_pag = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fec_cre = models.DateField(blank=True, null=True)
    fec_pag = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ant_doc02'


class AntEst02(models.Model):
    sta_est = models.CharField(max_length=1, blank=True, null=True)
    periodo = models.CharField(max_length=4, blank=True, null=True)
    cod_niv = models.CharField(max_length=2, blank=True, null=True)
    cod_est = models.CharField(max_length=6, blank=True, null=True)
    num_ced = models.CharField(max_length=16, blank=True, null=True)
    nom_est = models.CharField(max_length=50, blank=True, null=True)
    cod_cur = models.CharField(max_length=5, blank=True, null=True)
    dir_est = models.CharField(max_length=50, blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)
    cod_zon = models.CharField(max_length=4, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    est_civ = models.CharField(max_length=1, blank=True, null=True)
    fec_nac = models.DateField(blank=True, null=True)
    cod_bec = models.CharField(max_length=1, blank=True, null=True)
    nom_pad = models.CharField(max_length=40, blank=True, null=True)
    nom_mad = models.CharField(max_length=40, blank=True, null=True)
    nom_rep = models.CharField(max_length=40, blank=True, null=True)
    par_rep = models.CharField(max_length=10, blank=True, null=True)
    cod_prf = models.CharField(max_length=25, blank=True, null=True)
    tel_trb = models.CharField(max_length=20, blank=True, null=True)
    lug_trb = models.CharField(max_length=30, blank=True, null=True)
    observa = models.CharField(max_length=60, blank=True, null=True)
    col_pro = models.CharField(max_length=30, blank=True, null=True)
    mat_con = models.CharField(max_length=1, blank=True, null=True)
    fec_mat = models.DateField(blank=True, null=True)
    fec_ret = models.DateField(blank=True, null=True)
    usa_trn = models.CharField(max_length=1, blank=True, null=True)
    trn_adi = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    num_bus = models.CharField(max_length=3, blank=True, null=True)
    num_mat = models.CharField(max_length=5, blank=True, null=True)
    num_fol = models.CharField(max_length=5, blank=True, null=True)
    sta_apb = models.CharField(max_length=1, blank=True, null=True)
    sta_doc = models.CharField(max_length=1, blank=True, null=True)
    sta_con = models.CharField(max_length=1, blank=True, null=True)
    observ2 = models.CharField(max_length=60, blank=True, null=True)
    rep_can = models.CharField(max_length=30, blank=True, null=True)
    tip_bec = models.CharField(max_length=2, blank=True, null=True)
    zon_nac = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ant_est02'


class AntPag02(models.Model):
    periodo = models.CharField(max_length=4, blank=True, null=True)
    cod_niv = models.CharField(max_length=2, blank=True, null=True)
    cod_est = models.CharField(max_length=6, blank=True, null=True)
    cod_rub = models.CharField(max_length=3, blank=True, null=True)
    val_doc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    num_rec = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ant_pag02'


class AntPer02(models.Model):
    periodo = models.CharField(max_length=4, blank=True, null=True)
    cod_niv = models.CharField(max_length=2, blank=True, null=True)
    des_per = models.CharField(max_length=50, blank=True, null=True)
    fec_ini = models.DateField(blank=True, null=True)
    fec_fin = models.DateField(blank=True, null=True)
    dis_per = models.CharField(max_length=1, blank=True, null=True)
    num_per = models.SmallIntegerField(blank=True, null=True)
    num_not = models.SmallIntegerField(blank=True, null=True)
    not_min = models.SmallIntegerField(blank=True, null=True)
    not_max = models.SmallIntegerField(blank=True, null=True)
    prm_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prm_rec = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prm_re1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    not_re1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prm_re2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    not_re2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prm_re3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    not_re3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fec_cre = models.DateField(blank=True, null=True)
    fec_cie = models.DateField(blank=True, null=True)
    nom_rec = models.CharField(max_length=40, blank=True, null=True)
    nom_sec = models.CharField(max_length=40, blank=True, null=True)
    nom_sup = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ant_per02'


class AntRec02(models.Model):
    num_rec = models.CharField(max_length=7, blank=True, null=True)
    fec_rec = models.DateField(blank=True, null=True)
    cod_niv = models.CharField(max_length=2, blank=True, null=True)
    cod_rub = models.CharField(max_length=3, blank=True, null=True)
    val_rec = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    val_chq = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dsc_rec = models.CharField(max_length=60, blank=True, null=True)
    cod_cur = models.CharField(max_length=5, blank=True, null=True)
    cod_caj = models.CharField(max_length=2, blank=True, null=True)
    cod_bco = models.CharField(max_length=2, blank=True, null=True)
    nom_bco = models.CharField(max_length=12, blank=True, null=True)
    cta_cte = models.CharField(max_length=12, blank=True, null=True)
    num_chq = models.CharField(max_length=12, blank=True, null=True)
    sta_rec = models.SmallIntegerField(blank=True, null=True)
    fec_anl = models.DateField(blank=True, null=True)
    num_sec = models.CharField(max_length=13, blank=True, null=True)
    periodo = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ant_rec02'


class AntRub02(models.Model):
    periodo = models.CharField(max_length=4, blank=True, null=True)
    cod_niv = models.CharField(max_length=2, blank=True, null=True)
    cod_rub = models.CharField(max_length=3, blank=True, null=True)
    des_rub = models.CharField(max_length=50, blank=True, null=True)
    abr_rub = models.CharField(max_length=20, blank=True, null=True)
    sta_rub = models.CharField(max_length=2, blank=True, null=True)
    tip_rub = models.CharField(max_length=1, blank=True, null=True)
    val_rub = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    num_mes = models.SmallIntegerField(blank=True, null=True)
    fec_pag = models.DateField(blank=True, null=True)
    cod_cta = models.CharField(max_length=7, blank=True, null=True)
    cod_aux = models.CharField(max_length=5, blank=True, null=True)
    cod_cta2 = models.CharField(max_length=7, blank=True, null=True)
    cod_aux2 = models.CharField(max_length=5, blank=True, null=True)
    fec_cre = models.DateField(blank=True, null=True)
    cod_niv2 = models.CharField(max_length=2, blank=True, null=True)
    num_ord = models.SmallIntegerField(blank=True, null=True)
    dc2_rub = models.CharField(max_length=60, blank=True, null=True)
    dev_cta = models.CharField(max_length=7, blank=True, null=True)
    dev_aux = models.CharField(max_length=5, blank=True, null=True)
    dev_cta2 = models.CharField(max_length=7, blank=True, null=True)
    dev_aux2 = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ant_rub02'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BajasDeudas(models.Model):
    id = models.IntegerField(primary_key=True)
    idestudiante = models.IntegerField(blank=True, null=True)
    idmatricula = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.CharField(max_length=15, blank=True, null=True)
    idcajero = models.IntegerField(blank=True, null=True)
    cedula = models.CharField(max_length=16, blank=True, null=True)
    nombreestudiante = models.CharField(max_length=150, blank=True, null=True)
    idcarrera = models.IntegerField(blank=True, null=True)
    idcurso = models.IntegerField(blank=True, null=True)
    carreranivelparalelo = models.CharField(max_length=150, blank=True, null=True)
    periodo = models.CharField(max_length=40, blank=True, null=True)
    semestre = models.CharField(max_length=2, blank=True, null=True)
    idpayment = models.IntegerField(blank=True, null=True)
    idrubro = models.IntegerField(blank=True, null=True)
    concepto = models.CharField(max_length=200, blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    iddetalle = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bajas_deudas'


class Cajeros(models.Model):
    id = models.IntegerField(primary_key=True)
    nombres = models.CharField(max_length=200, blank=True, null=True)
    nusuario = models.CharField(max_length=20, blank=True, null=True)
    clave = models.CharField(max_length=10, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    fechaingres = models.DateTimeField(blank=True, null=True)
    fechacreacion = models.DateTimeField(blank=True, null=True)
    secuencia1 = models.CharField(max_length=3, blank=True, null=True)
    secuencia2 = models.CharField(max_length=3, blank=True, null=True)
    secuencia3 = models.CharField(max_length=9, blank=True, null=True)
    rol = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cajeros'


class CaptchaCaptchastore(models.Model):
    challenge = models.CharField(max_length=32)
    response = models.CharField(max_length=32)
    hashkey = models.CharField(unique=True, max_length=40)
    expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'captcha_captchastore'


class CeleryTaskmeta(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.BooleanField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'celery_taskmeta'


class CeleryTasksetmeta(models.Model):
    taskset_id = models.CharField(unique=True, max_length=255)
    result = models.TextField()
    date_done = models.DateTimeField()
    hidden = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'celery_tasksetmeta'


class DeuCierreMes(models.Model):
    idusuario = models.IntegerField(blank=True, null=True)
    idestudiante = models.IntegerField(blank=True, null=True)
    idmatricula = models.IntegerField(blank=True, null=True)
    estudiante = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    celular = models.CharField(max_length=30, blank=True, null=True)
    correo = models.TextField(blank=True, null=True)
    carrera = models.TextField(blank=True, null=True)
    idcurso = models.IntegerField(blank=True, null=True)
    nivel = models.IntegerField(blank=True, null=True)
    paralelo = models.CharField(max_length=2, blank=True, null=True)
    concepto = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pago = models.NullBooleanField()
    fecha_cierre = models.DateField(blank=True, null=True)
    periodo = models.CharField(max_length=9, blank=True, null=True)
    semestre = models.CharField(max_length=1, blank=True, null=True)
    mes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deu_cierre_mes'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjceleryCrontabschedule(models.Model):
    minute = models.CharField(max_length=64)
    hour = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=64)
    month_of_year = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'djcelery_crontabschedule'


class DjceleryIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'djcelery_intervalschedule'


class DjceleryPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    interval = models.ForeignKey(DjceleryIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    crontab = models.ForeignKey(DjceleryCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'djcelery_periodictask'


class DjceleryPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'djcelery_periodictasks'


class DjceleryTaskstate(models.Model):
    state = models.CharField(max_length=64)
    task_id = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=200, blank=True, null=True)
    tstamp = models.DateTimeField()
    args = models.TextField(blank=True, null=True)
    kwargs = models.TextField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    retries = models.IntegerField()
    worker = models.ForeignKey('DjceleryWorkerstate', models.DO_NOTHING, blank=True, null=True)
    hidden = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'djcelery_taskstate'


class DjceleryWorkerstate(models.Model):
    hostname = models.CharField(unique=True, max_length=255)
    last_heartbeat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_workerstate'


class EasyThumbnailsSource(models.Model):
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_source'
        unique_together = (('storage_hash', 'name'),)


class EasyThumbnailsThumbnail(models.Model):
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()
    source = models.ForeignKey(EasyThumbnailsSource, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnail'
        unique_together = (('storage_hash', 'name', 'source'),)


class EasyThumbnailsThumbnaildimensions(models.Model):
    thumbnail = models.ForeignKey(EasyThumbnailsThumbnail, models.DO_NOTHING, unique=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnaildimensions'


class FactCab(models.Model):
    id = models.IntegerField(primary_key=True)
    idestudiante = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    idcajero = models.IntegerField(blank=True, null=True)
    cedula = models.CharField(max_length=16, blank=True, null=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    periodo = models.CharField(max_length=40, blank=True, null=True)
    nombreestudiante = models.CharField(max_length=150, blank=True, null=True)
    carreranivelparalelo = models.CharField(max_length=150, blank=True, null=True)
    semestre = models.CharField(max_length=2, blank=True, null=True)
    subtotal12 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal0 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valortotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dinerorecibe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    numfact = models.CharField(max_length=20, blank=True, null=True)
    idcarrera = models.IntegerField(blank=True, null=True)
    idcurso = models.IntegerField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    idcli = models.IntegerField(blank=True, null=True)
    hora = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_cab'


class FactDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    idfcab = models.IntegerField(blank=True, null=True)
    idrubro = models.IntegerField(blank=True, null=True)
    concepto = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    cajero = models.IntegerField(blank=True, null=True)
    idpayment = models.IntegerField(blank=True, null=True)
    idantdoc02 = models.IntegerField(blank=True, null=True)
    hora = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_detalle'


class FactFpagos(models.Model):
    id = models.IntegerField(primary_key=True)
    idfactcab = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    formapago = models.CharField(max_length=100, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    num_t_ch = models.CharField(max_length=100, blank=True, null=True)
    autoriza = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    cajero = models.IntegerField(blank=True, null=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hora = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_fpagos'


class NcCab(models.Model):
    id = models.IntegerField(primary_key=True)
    ncidcajero = models.IntegerField(blank=True, null=True)
    ncfecha = models.DateField(blank=True, null=True)
    ncscuencia = models.CharField(max_length=20, blank=True, null=True)
    ncmotivo = models.TextField(blank=True, null=True)
    ncestado = models.IntegerField(blank=True, null=True)
    factura = models.IntegerField(blank=True, null=True)
    fidestudiante = models.IntegerField(blank=True, null=True)
    ffecha = models.DateField(blank=True, null=True)
    fidcajero = models.IntegerField(blank=True, null=True)
    fcedula = models.CharField(max_length=16, blank=True, null=True)
    fcliente = models.CharField(max_length=100, blank=True, null=True)
    fdireccion = models.CharField(max_length=150, blank=True, null=True)
    ftelefono = models.CharField(max_length=40, blank=True, null=True)
    fperiodo = models.CharField(max_length=40, blank=True, null=True)
    fnombreestudiante = models.CharField(max_length=150, blank=True, null=True)
    fcarreranivelparalelo = models.CharField(max_length=150, blank=True, null=True)
    fsemestre = models.CharField(max_length=2, blank=True, null=True)
    fsubtotal12 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fsubtotal0 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fiva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fvalortotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    festado = models.IntegerField(blank=True, null=True)
    fnumfact = models.CharField(max_length=20, blank=True, null=True)
    idcarrera = models.IntegerField(blank=True, null=True)
    idcurso = models.IntegerField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    idcli = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nc_cab'


class NcDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    idnccab = models.IntegerField(blank=True, null=True)
    idrubro = models.IntegerField(blank=True, null=True)
    concepto = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    cajero = models.IntegerField(blank=True, null=True)
    idpayment = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nc_detalle'


class Resucart(models.Model):
    periodo = models.TextField()
    semestre = models.CharField(max_length=1)
    carrera = models.TextField()
    curso = models.TextField()
    concepto = models.TextField()
    saldoanterior = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cobros = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    diario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deudarma = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deudames = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saldoactual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resucart'
        unique_together = (('periodo', 'semestre', 'carrera', 'curso', 'concepto'),)


class Rubros2(models.Model):
    id = models.IntegerField(primary_key=True)
    periodo = models.IntegerField(blank=True, null=True)
    semestre = models.CharField(max_length=1, blank=True, null=True)
    nivel = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    abrevia = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    tiporubro = models.CharField(max_length=1, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    num_mes = models.SmallIntegerField(blank=True, null=True)
    fec_pag = models.DateField(blank=True, null=True)
    cod_cta = models.CharField(max_length=7, blank=True, null=True)
    cod_aux = models.CharField(max_length=7, blank=True, null=True)
    cod_cta2 = models.CharField(max_length=7, blank=True, null=True)
    cod_aux2 = models.CharField(max_length=7, blank=True, null=True)
    fec_cre = models.DateField(blank=True, null=True)
    cod_niv2 = models.CharField(max_length=2, blank=True, null=True)
    num_ord = models.SmallIntegerField(blank=True, null=True)
    dc2_rub = models.CharField(max_length=60, blank=True, null=True)
    dev_cta = models.CharField(max_length=7, blank=True, null=True)
    dev_aux = models.CharField(max_length=7, blank=True, null=True)
    dev_cta2 = models.CharField(max_length=7, blank=True, null=True)
    dev_aux2 = models.CharField(max_length=5, blank=True, null=True)
    grabaiva = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rubros2'


class Secuenciafact(models.Model):
    id = models.IntegerField(primary_key=True)
    secuencia1 = models.CharField(max_length=3, blank=True, null=True)
    secuencia2 = models.CharField(max_length=3, blank=True, null=True)
    secuencia3 = models.CharField(max_length=9, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    cajero = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'secuenciafact'


class SigiaBugreport(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    gravity = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    description = models.TextField()
    snapshot = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'sigia_bugreport'


class SigiaCanton(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    province = models.ForeignKey('SigiaProvince', models.DO_NOTHING)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sigia_canton'


class SigiaCareer(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'sigia_career'


class SigiaCharge(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    nombre = models.CharField(max_length=30)
    teacher = models.ForeignKey(AuthUser, models.DO_NOTHING)
    date_start_charge = models.TimeField(blank=True, null=True)
    date_end_charge = models.TimeField(blank=True, null=True)
    no_doc_charge = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_charge'


class SigiaContact(models.Model):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    user_id = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id_doc_num = models.CharField(max_length=30)
    email = models.CharField(max_length=75, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    cellphone = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_contact'


class SigiaCountry(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    name = models.CharField(unique=True, max_length=50)
    gentilicio = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sigia_country'


class SigiaCourse(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    career = models.ForeignKey(SigiaCareer, models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=30)
    type = models.CharField(max_length=1)
    period = models.ForeignKey('SigiaPeriod', models.DO_NOTHING)
    semester = models.CharField(max_length=1)
    level = models.IntegerField()
    parallel = models.CharField(max_length=1)
    max_quota = models.IntegerField()
    payment_reg = models.FloatField()
    payment_ext = models.FloatField()
    payment_esp = models.FloatField()
    amount_payments = models.IntegerField()
    value_payments = models.IntegerField()
    applied_scholarship_from = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sigia_course'


class SigiaEmaillog(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    sender = models.ForeignKey(AuthUser, models.DO_NOTHING)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    send_success = models.BooleanField()
    send_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sigia_emaillog'


class SigiaEmaillogCc(models.Model):
    emaillog = models.ForeignKey(SigiaEmaillog, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sigia_emaillog_cc'
        unique_together = (('emaillog', 'user'),)


class SigiaEmaillogCco(models.Model):
    emaillog = models.ForeignKey(SigiaEmaillog, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sigia_emaillog_cco'
        unique_together = (('emaillog', 'user'),)


class SigiaEmaillogTo(models.Model):
    emaillog = models.ForeignKey(SigiaEmaillog, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sigia_emaillog_to'
        unique_together = (('emaillog', 'user'),)


class SigiaEnrollment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    student = models.ForeignKey('SigiaStudent', models.DO_NOTHING)
    course = models.ForeignKey(SigiaCourse, models.DO_NOTHING)
    type = models.CharField(max_length=3)
    date = models.DateField()
    financing_sys = models.CharField(max_length=4)
    condition = models.CharField(max_length=1)
    scholarship = models.IntegerField()
    payment_order = models.ForeignKey('SigiaPaymentorder', models.DO_NOTHING, blank=True, null=True)
    n_matricula = models.IntegerField(blank=True, null=True)
    baja = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'sigia_enrollment'


class SigiaEthnicgroup(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_ethnicgroup'


class SigiaEventsgroup(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    name = models.CharField(max_length=50)
    description = models.TextField()
    student_type = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_eventsgroup'


class SigiaEventsgrouprelation(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    event_type = models.ForeignKey('SigiaEventtype', models.DO_NOTHING)
    event_group = models.ForeignKey(SigiaEventsgroup, models.DO_NOTHING)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_eventsgrouprelation'


class SigiaEventtype(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    name = models.CharField(max_length=50)
    description = models.TextField()
    student_type = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_eventtype'


class SigiaInstitution(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'sigia_institution'


class SigiaMatter(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    career = models.ForeignKey(SigiaCareer, models.DO_NOTHING)
    description = models.CharField(max_length=30)
    period = models.ForeignKey('SigiaPeriod', models.DO_NOTHING)
    semester = models.CharField(max_length=1)
    level = models.IntegerField()
    parallel = models.CharField(max_length=1)
    credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sigia_matter'


class SigiaMedicContac(models.Model):
    id_sigiamedicrecord = models.ForeignKey('SigiaMedicrecord', models.DO_NOTHING, db_column='id_sigiamedicrecord')
    relationship_type = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_medic_contac'


class SigiaMedicFamilyBackground(models.Model):
    id_sigiamedicrecord = models.ForeignKey('SigiaMedicrecord', models.DO_NOTHING, db_column='id_sigiamedicrecord')
    type_background = models.ForeignKey('SigiaMedicFamilyBackgroundDetail', models.DO_NOTHING, db_column='type_background', blank=True, null=True)
    detail_background = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_medic_family_background'


class SigiaMedicFamilyBackgroundDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    detail = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_medic_family_background_detail'


class SigiaMedicPersonalBackground(models.Model):
    id_sigiamedicrecord = models.ForeignKey('SigiaMedicrecord', models.DO_NOTHING, db_column='id_sigiamedicrecord')
    type_background = models.ForeignKey('SigiaMedicPersonalBackgroundDetail', models.DO_NOTHING, db_column='type_background', blank=True, null=True)
    detail_background = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_medic_personal_background'


class SigiaMedicPersonalBackgroundDetail(models.Model):
    detail = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_medic_personal_background_detail'


class SigiaMedicrecord(models.Model):
    created = models.DateTimeField()
    created_by_id = models.IntegerField()
    modified = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    create_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    id_patient = models.ForeignKey('SigiaUserprofile', models.DO_NOTHING, db_column='id_patient', blank=True, null=True)
    blood_type_by = models.IntegerField(blank=True, null=True)
    blood_type = models.CharField(max_length=4, blank=True, null=True)
    form_arrival = models.CharField(max_length=40, blank=True, null=True)
    source_information = models.CharField(max_length=40, blank=True, null=True)
    delivery_patient = models.CharField(max_length=40, blank=True, null=True)
    phone_delivery = models.CharField(max_length=12, blank=True, null=True)
    actual_problem = models.CharField(max_length=40, blank=True, null=True)
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    breathing_frequency = models.IntegerField(blank=True, null=True)
    oral_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    asolar_temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    p_cephalico = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_medicrecord'


class SigiaParish(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    canton = models.ForeignKey(SigiaCanton, models.DO_NOTHING)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sigia_parish'


class SigiaPaymentorder(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    user_id = models.IntegerField()
    date_issue = models.DateField()
    payout = models.BooleanField()
    date_payment = models.DateField(blank=True, null=True)
    level = models.IntegerField()
    period = models.ForeignKey('SigiaPeriod', models.DO_NOTHING)
    semester = models.CharField(max_length=1)
    value = models.FloatField()
    payment_concept = models.CharField(max_length=4)
    number = models.IntegerField()
    enrollment = models.ForeignKey(SigiaEnrollment, models.DO_NOTHING, blank=True, null=True)
    contabilizada = models.NullBooleanField()
    baja = models.NullBooleanField()
    idbaja = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_paymentorder'


class SigiaPeriod(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    name = models.CharField(unique=True, max_length=9)
    predecessor = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    finalized = models.BooleanField()
    active = models.BooleanField()
    start_notes = models.TextField(blank=True, null=True)
    end_notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_period'


class SigiaProvince(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    country = models.ForeignKey(SigiaCountry, models.DO_NOTHING)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sigia_province'


class SigiaStudent(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    user_id = models.IntegerField(unique=True)
    career = models.ForeignKey(SigiaCareer, models.DO_NOTHING, blank=True, null=True)
    working = models.NullBooleanField()
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.CharField(max_length=200, blank=True, null=True)
    charge = models.CharField(max_length=50, blank=True, null=True)
    work_telephone = models.CharField(max_length=50, blank=True, null=True)
    work_email = models.CharField(max_length=75, blank=True, null=True)
    campus_orig = models.CharField(max_length=50, blank=True, null=True)
    campus_city = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    language_know_lvl = models.CharField(max_length=1, blank=True, null=True)
    informatic_know_lvl = models.CharField(max_length=1, blank=True, null=True)
    income_sys = models.CharField(max_length=3, blank=True, null=True)
    first_time_ingress = models.DateField(blank=True, null=True)
    decline = models.NullBooleanField()
    date_graduation = models.DateField(blank=True, null=True)
    date_thesis_defense = models.DateField(blank=True, null=True)
    act_number = models.IntegerField(blank=True, null=True)
    senescyt_number = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=3, blank=True, null=True)
    approved = models.NullBooleanField()
    cohort_semester = models.CharField(max_length=1, blank=True, null=True)
    cohort_period = models.ForeignKey(SigiaPeriod, models.DO_NOTHING, blank=True, null=True)
    motivo_elimina = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_student'


class SigiaStudentevent(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    type = models.ForeignKey(SigiaEventtype, models.DO_NOTHING)
    student = models.ForeignKey(SigiaStudent, models.DO_NOTHING)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    ini_obs = models.TextField(blank=True, null=True)
    tutor = models.ForeignKey('SigiaTeacher', models.DO_NOTHING, blank=True, null=True)
    state = models.CharField(max_length=3)
    end_obs = models.TextField(blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_studentevent'


class SigiaStudenteventsgrouprelation(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    student = models.ForeignKey(SigiaStudent, models.DO_NOTHING)
    event_group = models.ForeignKey(SigiaEventsgroup, models.DO_NOTHING)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sigia_studenteventsgrouprelation'


class SigiaStudentnotes(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    student = models.ForeignKey(SigiaStudent, models.DO_NOTHING)
    note = models.TextField()

    class Meta:
        managed = False
        db_table = 'sigia_studentnotes'


class SigiaStudies(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    teacher = models.ForeignKey('SigiaTeacher', models.DO_NOTHING)
    academic_level = models.IntegerField()
    institute = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    title_img = models.CharField(max_length=100, blank=True, null=True)
    date_award = models.DateField()
    country = models.ForeignKey(SigiaCountry, models.DO_NOTHING)
    senescyt_id = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'sigia_studies'


class SigiaTeacher(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    user_id = models.IntegerField(unique=True)
    institutional_email = models.CharField(max_length=75, blank=True, null=True)
    academic_category = models.CharField(max_length=30, blank=True, null=True)
    contract_type = models.CharField(max_length=2, blank=True, null=True)
    academic_unity = models.CharField(max_length=30, blank=True, null=True)
    hours_to_pedagogy = models.IntegerField(blank=True, null=True)
    hours_to_research = models.IntegerField(blank=True, null=True)
    hours_to_society = models.IntegerField(blank=True, null=True)
    hours_to_other = models.IntegerField(blank=True, null=True)
    other_activities = models.CharField(max_length=50, blank=True, null=True)
    studying = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'sigia_teacher'


class SigiaUserprofile(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    created_by_id = models.IntegerField(blank=True, null=True)
    created_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    modified_by_id = models.IntegerField(blank=True, null=True)
    modified_with_session_key = models.CharField(max_length=40, blank=True, null=True)
    live = models.NullBooleanField()
    user_id = models.IntegerField(unique=True)
    photo = models.CharField(max_length=100, blank=True, null=True)
    id_doc_type = models.CharField(max_length=1, blank=True, null=True)
    id_doc_num = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    nationality = models.ForeignKey(SigiaCountry, models.DO_NOTHING, blank=True, null=True)
    birthplace_country = models.ForeignKey(SigiaCountry, models.DO_NOTHING, blank=True, null=True)
    birthplace_province = models.ForeignKey(SigiaProvince, models.DO_NOTHING, blank=True, null=True)
    birthplace_canton = models.ForeignKey(SigiaCanton, models.DO_NOTHING, blank=True, null=True)
    birthplace_parish = models.ForeignKey(SigiaParish, models.DO_NOTHING, blank=True, null=True)
    address_province = models.ForeignKey(SigiaProvince, models.DO_NOTHING, blank=True, null=True)
    address_canton = models.ForeignKey(SigiaCanton, models.DO_NOTHING, blank=True, null=True)
    address_parish = models.ForeignKey(SigiaParish, models.DO_NOTHING, blank=True, null=True)
    marital_status = models.CharField(max_length=1, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    cellphone = models.CharField(max_length=30, blank=True, null=True)
    handed_id_doc = models.NullBooleanField()
    id_doc_img = models.CharField(max_length=100, blank=True, null=True)
    handed_voting_cert = models.NullBooleanField()
    voting_cert_img = models.CharField(max_length=100, blank=True, null=True)
    handed_degree = models.NullBooleanField()
    handed_degree_img = models.CharField(max_length=100, blank=True, null=True)
    handed_medical_cert = models.NullBooleanField()
    medical_cert_img = models.CharField(max_length=100, blank=True, null=True)
    handed_birth_cert = models.NullBooleanField()
    birth_cert_img = models.CharField(max_length=100, blank=True, null=True)
    disability = models.NullBooleanField()
    disability_percent = models.IntegerField(blank=True, null=True)
    disability_id = models.CharField(max_length=20, blank=True, null=True)
    ethnic_group = models.ForeignKey(SigiaEthnicgroup, models.DO_NOTHING, blank=True, null=True)
    email_confirmed = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'sigia_userprofile'
