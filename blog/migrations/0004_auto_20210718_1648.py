# Generated by Django 2.2 on 2021-07-18 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210717_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.FileField(null=True, upload_to='blog/'),
        ),
    ]
