# Generated by Django 2.2 on 2021-07-19 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210718_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(null=True, upload_to='blog/% Y/% m/% d/'),
        ),
    ]
