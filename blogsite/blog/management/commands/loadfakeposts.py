import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Post
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("user_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for user_id in options["user_ids"]:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise CommandError(f"User does not exist with id {user_id}")

            for _ in range(30):
                # Change the number as needed
                author = user
                title = fake.sentence()
                body = fake.paragraphs(nb=1, ext_word_list=None)[0]
                slug = slugify(title)
                post = Post(author=author, title=title, body=body, slug=slug)
                post.save()
