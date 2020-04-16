# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Eventlist(models.Model):
    el_id = models.AutoField(primary_key=True, verbose_name='ID')
    el_title = models.CharField(max_length=100, verbose_name='Название мероприятия')
    el_description = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Описание')
    el_id_place = models.ForeignKey('Placelist', models.DO_NOTHING, null=True, db_column='el_id_place', verbose_name='ID Места проведения')
    el_date = models.DateTimeField(verbose_name='Дата')
    el_time = models.TimeField(null=True)
    el_link = models.CharField(max_length=300, verbose_name='Ссылка на сайт мероприятия')
    el_chk_active = models.IntegerField(blank=True, null=True, verbose_name='Мероприятие активно')

    def __str__(self):
        return f'{self.el_id} - {self.el_title}'

    class Meta:
        db_table = 'eventlist'
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Eventtaglist(models.Model):
    etl_id = models.AutoField(primary_key=True, verbose_name='ID')
    etl_id_event = models.ForeignKey(Eventlist, models.DO_NOTHING, db_column='etl_id_event', verbose_name='ID мероприятия')
    etl_id_tag = models.ForeignKey('Taglist', models.DO_NOTHING, db_column='etl_id_tag', verbose_name='Тэг')

    def __str__(self):
        return f'#{self.etl_id} {self.etl_id_event} -- {self.etl_id_tag}'

    class Meta:
        db_table = 'eventtaglist'
        verbose_name = 'Тэг мероприятия'
        verbose_name_plural = 'Тэги мероприятия'


class Placelist(models.Model):
    pl_id = models.AutoField(primary_key=True, verbose_name='ID')
    pl_city = models.CharField(max_length=30, verbose_name='Город')
    pl_str_name = models.CharField(max_length=30, verbose_name='Улица')
    pl_house_num = models.IntegerField(verbose_name='Номер дома')
    pl_letter = models.CharField(max_length=1, blank=True, null=True, verbose_name='Буква дома')
    pl_place_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Название места проведения')

    def __str__(self):
        return f'#{self.pl_id}'

    class Meta:
        db_table = 'placelist'
        verbose_name = 'Место проведения'
        verbose_name_plural = 'Места проведения'


class Taglist(models.Model):
    tl_id = models.AutoField(primary_key=True, verbose_name='ID')
    tl_title = models.CharField(max_length=30, verbose_name='Тэг')

    def __str__(self):
        return f'{self.tl_title}'

    class Meta:
        db_table = 'taglist'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Userlist(models.Model):
    ul_id = models.AutoField(primary_key=True, verbose_name='ID')
    ul_login = models.CharField(max_length=20, verbose_name='Логин')
    ul_password = models.CharField(max_length=20, verbose_name='Пароль')
    ul_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Имя')
    ul_surname = models.CharField(max_length=20, blank=True, null=True, verbose_name='Фамилия')
    ul_secondname = models.CharField(max_length=20, blank=True, null=True,  verbose_name='Отчество')
    ul_email = models.CharField(max_length=30, verbose_name='E-mail')
    ul_linkvkmessage = models.CharField(max_length=30, blank=True, null=True, verbose_name='Ссылка на вк')
    ul_linktgmessage = models.CharField(max_length=30, blank=True, null=True, verbose_name='ID чата в телеграм')
    ul_chk_mailing = models.IntegerField(blank=True, null=True, verbose_name='Согласие на рассылку')

    def __str__(self):
        return f'{self.ul_id} - {self.ul_login}'

    class Meta:
        db_table = 'userlist'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Usertaglist(models.Model):
    utl_id = models.AutoField(primary_key=True, verbose_name='ID')
    utl_id_user = models.ForeignKey(Userlist, models.DO_NOTHING, db_column='utl_id_user', verbose_name='ID пользователя')
    utl_id_tag = models.ForeignKey(Taglist, models.DO_NOTHING, db_column='utl_id_tag',  verbose_name='Тэг')

    def __str__(self):
        return f'#{self.utl_id} {self.utl_id_user} -- {self.utl_id_tag}'

    class Meta:
        db_table = 'usertaglist'
        verbose_name = 'Тэг пользователя'
        verbose_name_plural = 'Тэги пользователя'
