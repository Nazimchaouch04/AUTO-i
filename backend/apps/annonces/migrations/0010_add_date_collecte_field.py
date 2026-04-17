# Generated migration to add date_collecte field with default

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0009_sync_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='annonce',
            name='date_collecte',
            field=models.DateTimeField(default=timezone.now, null=True, blank=True),
        ),
    ]
