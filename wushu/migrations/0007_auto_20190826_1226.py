# Generated by Django 2.2.1 on 2019-08-26 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wushu', '0006_auto_20190825_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True, verbose_name='Ülke')),
            ],
        ),
        migrations.AddField(
            model_name='communication',
            name='phoneNumber2',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='communication',
            name='postalCode',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('Erkek', 'Erkek'), ('Kadın', 'Kadın')], default='Erkek', max_length=128, verbose_name='Cinsiyeti'),
        ),
    ]
