# Generated by Django 2.2.5 on 2019-10-06 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nano', '0004_auto_20191006_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='GCFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='uploads/gc/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='VCFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='uploads/volcano/%Y/%m/%d/')),
            ],
        ),
        migrations.RemoveField(
            model_name='gevolcano',
            name='files',
        ),
        migrations.RemoveField(
            model_name='groupcomparison',
            name='files',
        ),
        migrations.AddField(
            model_name='gevolcano',
            name='vc_files',
            field=models.ManyToManyField(to='nano.VCFiles'),
        ),
        migrations.AddField(
            model_name='groupcomparison',
            name='gc_files',
            field=models.ManyToManyField(to='nano.GCFiles'),
        ),
    ]