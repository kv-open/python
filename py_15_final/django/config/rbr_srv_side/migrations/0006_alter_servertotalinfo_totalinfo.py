# Generated by Django 4.1.1 on 2022-09-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbr_srv_side', '0005_alter_servertotalinfo_totalinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servertotalinfo',
            name='totalinfo',
            field=models.JSONField(),
        ),
    ]