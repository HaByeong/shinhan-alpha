# Generated by Django 4.1.5 on 2023-02-20 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_name', models.CharField(max_length=128, verbose_name='리워드 이름')),
                ('tier_name', models.CharField(max_length=128, verbose_name='티어 이름')),
                ('tier_point', models.CharField(max_length=128, verbose_name='기준 점수')),
            ],
            options={
                'verbose_name': '리워드',
                'verbose_name_plural': '리워드',
                'db_table': 'shinhan_reward',
            },
        ),
    ]
