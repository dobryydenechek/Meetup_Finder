# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Eventlist(models.Model):
    el_id = models.AutoField(primary_key=True, verbose_name='ID')
    el_title = models.CharField(max_length=50, verbose_name='Название мероприятия')
    el_description = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Описание')
    el_id_place = models.ForeignKey('Placelist', models.DO_NOTHING, db_column='el_id_place', verbose_name='ID Места проведения')
    el_date = models.DateTimeField(verbose_name='Дата')
    el_time = models.TimeField()
    el_link = models.CharField(max_length=100, verbose_name='Ссылка на сайт мероприятия')
    el_chk_active = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.el_title}'

    class Meta:
        managed = False
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
        managed = False
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
        managed = False
        db_table = 'placelist'
        verbose_name = 'Место проведения'
        verbose_name_plural = 'Места проведения'


class Taglist(models.Model):
    tl_id = models.AutoField(primary_key=True, verbose_name='ID')
    tl_title = models.CharField(max_length=15, verbose_name='Тэг')

    def __str__(self):
        return f'{self.tl_title}'

    class Meta:
        managed = False
        db_table = 'taglist'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Userlist(models.Model):
    ul_id = models.AutoField(primary_key=True, verbose_name='ID')
    ul_login = models.CharField(max_length=20, verbose_name='Логин')
    ul_password = models.CharField(max_length=20, verbose_name='Пароль')
    ul_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Имя')
    ul_surname = models.CharField(max_length=20, blank=True, null=True, verbose_name='Фамилия')
    ul_secondname = models.CharField(max_length=20, blank=True, null=True)
    ul_email = models.CharField(max_length=30, verbose_name='E-mail')
    ul_linkvkmessage = models.CharField(max_length=30, blank=True, null=True, verbose_name='Ссылка на вк')
    ul_linktgmessage = models.CharField(max_length=30, blank=True, null=True, verbose_name='ID чата в телеграм')
    ul_chk_mailing = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.ul_login}'

    class Meta:
        managed = False
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
        managed = False
        db_table = 'usertaglist'
        verbose_name = 'Тэг пользователя'
        verbose_name_plural = 'Тэги пользователя'
