# Generated by Django 3.0.4 on 2020-04-28 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Eventlist',
            fields=[
                ('el_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('el_title', models.CharField(max_length=100, verbose_name='Название мероприятия')),
                ('el_description', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Описание')),
                ('el_date', models.DateTimeField(verbose_name='Дата')),
                ('el_time', models.TimeField(null=True)),
                ('el_link', models.CharField(max_length=300, verbose_name='Ссылка на сайт мероприятия')),
                ('el_chk_active', models.IntegerField(blank=True, null=True, verbose_name='Мероприятие активно')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
            },
        ),
        migrations.CreateModel(
            name='Placelist',
            fields=[
                ('pl_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('pl_city', models.CharField(max_length=30, verbose_name='Город')),
                ('pl_str_name', models.CharField(max_length=30, verbose_name='Улица')),
                ('pl_house_num', models.IntegerField(verbose_name='Номер дома')),
                ('pl_letter', models.CharField(blank=True, max_length=1, null=True, verbose_name='Буква дома')),
                ('pl_place_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Название места проведения')),
            ],
            options={
                'verbose_name': 'Место проведения',
                'verbose_name_plural': 'Места проведения',
            },
        ),
        migrations.CreateModel(
            name='Taglist',
            fields=[
                ('tl_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('tl_title', models.CharField(max_length=30, verbose_name='Тэг')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Userlist',
            fields=[
                ('ul_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('ul_login', models.CharField(max_length=20, verbose_name='Логин')),
                ('ul_password', models.CharField(max_length=20, verbose_name='Пароль')),
                ('ul_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Имя')),
                ('ul_surname', models.CharField(blank=True, max_length=20, null=True, verbose_name='Фамилия')),
                ('ul_secondname', models.CharField(blank=True, max_length=20, null=True, verbose_name='Отчество')),
                ('ul_email', models.CharField(max_length=30, verbose_name='E-mail')),
                ('ul_linkvkmessage', models.CharField(blank=True, max_length=30, null=True, verbose_name='Ссылка на вк')),
                ('ul_linktgmessage', models.CharField(blank=True, max_length=30, null=True, verbose_name='ID чата в телеграм')),
                ('ul_chk_mailing', models.IntegerField(blank=True, null=True, verbose_name='Согласие на рассылку')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Usertaglist',
            fields=[
                ('utl_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('utl_id_tag', models.ForeignKey(db_column='utl_id_tag', on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Taglist', verbose_name='Тэг')),
                ('utl_id_user', models.ForeignKey(db_column='utl_id_user', on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Userlist', verbose_name='ID пользователя')),
            ],
            options={
                'verbose_name': 'Тэг пользователя',
                'verbose_name_plural': 'Тэги пользователя',
            },
        ),
        migrations.CreateModel(
            name='Eventtaglist',
            fields=[
                ('etl_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('etl_id_event', models.ForeignKey(db_column='etl_id_event', on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Eventlist', verbose_name='ID мероприятия')),
                ('etl_id_tag', models.ForeignKey(db_column='etl_id_tag', on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Taglist', verbose_name='Тэг')),
            ],
            options={
                'verbose_name': 'Тэг мероприятия',
                'verbose_name_plural': 'Тэги мероприятия',
            },
        ),
        migrations.AddField(
            model_name='eventlist',
            name='el_id_place',
            field=models.ForeignKey(db_column='el_id_place', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Placelist', verbose_name='ID Места проведения'),
        ),
    ]
