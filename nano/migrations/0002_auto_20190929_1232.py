# Generated by Django 2.2.5 on 2019-09-29 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nano', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
            ],
        ),
        migrations.RemoveField(
            model_name='inputfile',
            name='upload_file',
        ),
        migrations.AddField(
            model_name='inputfile',
            name='upload_files',
            field=models.ManyToManyField(to='nano.Files'),
        ),
    ]
