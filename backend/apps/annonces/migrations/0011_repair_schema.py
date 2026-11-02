from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('annonces', '0010_add_date_collecte_field'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RemoveField(
                    model_name='annonce',
                    name='date_collecte',
                ),
                migrations.AddField(
                    model_name='recherchesauvegardee',
                    name='updated_at',
                    field=models.DateTimeField(auto_now=True),
                ),
                migrations.AddField(
                    model_name='battle',
                    name='updated_at',
                    field=models.DateTimeField(auto_now=True),
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name='annonce',
                    name='date_collecte',
                ),
            ],
        ),
    ]
