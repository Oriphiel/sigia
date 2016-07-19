from django.conf import settings

from django.core.management.base import NoArgsCommand

DATABASE_HOST = settings.DATABASES['default']['HOST']
DATABASE_USER = settings.DATABASES['default']['USER']
DATABASE_PASSWORD = settings.DATABASES['default']['PASSWORD']
DATABASE_PORT = settings.DATABASES['default']['PORT']
DATABASE_NAME = settings.DATABASES['default']['NAME']


class Command(NoArgsCommand):
    help = "Drop and re-create the database"

    def handle_noargs(self, **options):
        import MySQLdb

        print "Connecting..."
        db = MySQLdb.connect(host=DATABASE_HOST or "localhost", user=DATABASE_USER,
                             passwd=DATABASE_PASSWORD, port=int(DATABASE_PORT or 3306))

        cursor = db.cursor()
        print "Dropping database %s" % DATABASE_NAME
        cursor.execute("drop database %s; create database %s;" % (DATABASE_NAME, DATABASE_NAME))
        print "Dropped"
