from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    args = '<none>'
    help = 'our help string comes here'

    def handle(self, *args, **options):
        print 'Droping database'
        call_command('drop')
        print 'Syncronizing database'
        call_command('syncdb', interactive=False)
        print 'Creating superuser'
        call_command('createsuperuser', username='dariov', email='dvazquez@aitec.edu.ec')
        print 'Populating database'
        call_command('populate_db')
