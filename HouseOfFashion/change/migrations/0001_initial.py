# Generated by Django 2.2.4 on 2019-11-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompositeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_result', models.FileField(upload_to='composite-image/%Y/%m/%d')),
            ],
        ),
    ]
