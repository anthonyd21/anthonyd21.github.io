# Generated by Django 3.2.3 on 2021-06-02 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='uploads/%Y/%m/%d'),
        ),
    ]
