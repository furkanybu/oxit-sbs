# Generated by Django 2.2.1 on 2019-08-26 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wushu', '0013_sportclubuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True, verbose_name='Kulüp Üye Rolü')),
            ],
        ),
    ]
