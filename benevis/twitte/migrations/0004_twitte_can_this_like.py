# Generated by Django 3.2.7 on 2021-10-06 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitte', '0003_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitte',
            name='can_this_like',
            field=models.BooleanField(default=False),
        ),
    ]
