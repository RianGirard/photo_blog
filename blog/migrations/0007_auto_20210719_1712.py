# Generated by Django 2.2 on 2021-07-20 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210719_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(null=True, upload_to='blog/'),
        ),
    ]
