# Generated by Django 4.2.6 on 2023-10-12 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='description',
            field=models.CharField(blank=True, max_length=1023, null=True, verbose_name='Описание'),
        ),
    ]
