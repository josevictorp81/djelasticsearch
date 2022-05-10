from django.core.management.base import BaseCommand

from core.models import Category, Article


class Command(BaseCommand):
    help = 'Populates the database with some testing data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Started database population process...'))

        if Category.objects.filter(title='System administration').exists():
            self.stdout.write(self.style.SUCCESS('Database has already been populated. Cancelling the operation.'))
            return

        # Create categories
        system_administration = Category.objects.create(title='System administration')
        seo_optimization = Category.objects.create(title='SEO optimization')
        programming = Category.objects.create(title='Programming')

        # Create articles
        website_article = Article.objects.create(
           title='How to code and deploy a website?',
           category=programming
        )

        google_article = Article.objects.create(
           title='How to improve your Google rating?',
           category=seo_optimization
        )

        programming_article = Article.objects.create(
           title='Which programming language is the best?',
           category=programming
        )

        ubuntu_article = Article.objects.create(
           title='Installing the latest version of Ubuntu',
           category=system_administration
        )

        django_article = Article.objects.create(
           title='Django REST Framework and Elasticsearch',
           category=system_administration
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))