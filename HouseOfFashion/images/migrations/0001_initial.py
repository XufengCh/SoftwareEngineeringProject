# Generated by Django 2.2.4 on 2019-11-17 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BodyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=40)),
                ('image_file', models.FileField(upload_to='uploads/bodys/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='ClotheImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=40)),
                ('image_file', models.FileField(upload_to='uploads/clothes/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Clothe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.PositiveSmallIntegerField()),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.ClotheImage')),
            ],
        ),
    ]
