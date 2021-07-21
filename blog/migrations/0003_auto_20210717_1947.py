# Generated by Django 2.2 on 2021-07-18 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.CharField(choices=[('yes', 'YES'), ('no', 'NO')], default='no', max_length=3),
        ),
    ]