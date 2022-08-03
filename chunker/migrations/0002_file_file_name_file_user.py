# Generated by Django 4.0.4 on 2022-08-02 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chunker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
