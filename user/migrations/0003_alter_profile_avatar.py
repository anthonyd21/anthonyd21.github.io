# Generated by Django 3.2.3 on 2021-06-02 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='static/user/defaultavatar.jpg', upload_to='static/user'),
        ),
    ]