# Generated by Django 3.2.8 on 2022-09-13 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.CharField(blank=True, default='RU', max_length=10, verbose_name='язык'),
        ),
    ]
