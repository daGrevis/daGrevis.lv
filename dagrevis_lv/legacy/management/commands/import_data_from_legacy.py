from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template import defaultfilters
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from blog.models import Article
from legacy.models import LegacyArticle


class Command(BaseCommand):
    help = "Imports data from legacy"
    option_list = BaseCommand.option_list + (
        make_option("-u",
                    "--superuser_username",
                    dest="superuser_username",
                    default="daGrevis",
                    help="Superuser username that will be the author for imported data"),
    )

    def handle(self, *args, **options):
        superuser_username = options["superuser_username"]
        try:
            superuser = User.objects.get(username=superuser_username)
        except ObjectDoesNotExist:
            raise CommandError("Can't found the superuser with username '{}'!".format(superuser_username))
        legacy_articles = LegacyArticle.objects.all()
        for legacy_article in legacy_articles:
            article = Article()
            article.pk = legacy_article.pk
            article.author = superuser
            # MySQL returns `long` type for all `IntegerField`s.
            article.created = datetime.fromtimestamp(int(legacy_article.created))
            # Field `last_updated` is not set always.
            if legacy_article.last_updated:
                article.modified = datetime.fromtimestamp(int(legacy_article.last_updated))
            article.title = legacy_article.title
            article.content = legacy_article.content
            article.slug = defaultfilters.slugify(legacy_article.title)
            if legacy_article.tweet_id:
                article.tweet_id = int(legacy_article.tweet_id)
            article.save()
        self.stdout.write("Import was successful! Total of {} articles were imported.\n".format(legacy_articles.count()))
