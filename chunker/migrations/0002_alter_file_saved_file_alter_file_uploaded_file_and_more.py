# Generated by Django 4.0.4 on 2022-08-04 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chunker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='saved_file',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='file',
            name='uploaded_file',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='file',
            name='zip_file',
            field=models.FileField(upload_to=''),
        ),
    ]
