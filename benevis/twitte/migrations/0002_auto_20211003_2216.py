# Generated by Django 3.2.7 on 2021-10-03 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitte', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitte',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='twitte',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTwitte', to=settings.AUTH_USER_MODEL),
        ),
    ]
