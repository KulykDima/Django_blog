from datetime import datetime, time, timedelta

from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from prettytable import PrettyTable

from post.models import Posts


class Command(BaseCommand):
    helps = "Send Today's Report to Admins"

    def handle(self, *args, **options):
        today_start = make_aware(datetime.combine(timezone.now(), time()))
        today_end = make_aware(datetime.combine(timezone.now() + timedelta(1), time()))

        posts = Posts.objects.filter(create_date__range=(today_start, today_end))
        # WHERE update_timestamp >= today_start AND update_timestamp < today_end
        # WHERE update_timestamp BETWEEN today_start AND today_end

        if posts:
            # message = ""
            x = PrettyTable()
            x.field_names = ['Title', 'Author', 'Like', 'Dislike', 'Create_date']

            for post in posts:
                x.add_row(
                    [
                        post.title,
                        post.author,
                        post.like.count(),
                        post.dislike.count(),
                        post.create_date
                        # f'{post.num_correct_answers}/{post.num_incorrect_answers}',
                        # post.points(),
                        # f'{round((post.update_timestamp - post.create_timestamp).total_seconds())}s.'
                    ]
                )

            subject = f"Report from {today_start.strftime('%Y-%m-%d')} " \
                      f"to {today_end.strftime('%Y-%m-%d')}"

            mail_admins(subject=subject, message=x.get_string(), html_message=None)

            self.stdout.write("E-mail Report was sent.")
        else:
            self.stdout.write("No posts confirmed today.")
