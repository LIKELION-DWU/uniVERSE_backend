# Generated by Django 4.2.5 on 2023-09-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_alter_booth_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booth',
            name='notice',
        ),
        migrations.AddField(
            model_name='booth',
            name='category',
            field=models.CharField(choices=[('day1', '2023-10-04'), ('day2', '2023-10-05'), ('day3', '2023-10-06')], default='day1', max_length=10, verbose_name='부스 카테고리(날짜별)'),
        ),
        migrations.AddField(
            model_name='booth',
            name='place',
            field=models.TextField(default='동덕여자대학교', verbose_name='장소'),
        ),
        migrations.AlterField(
            model_name='booth',
            name='date',
            field=models.TextField(default='10.04 - 10.06', verbose_name='일시'),
        ),
        migrations.AlterField(
            model_name='booth',
            name='introduce',
            field=models.TextField(verbose_name='내용'),
        ),
    ]
