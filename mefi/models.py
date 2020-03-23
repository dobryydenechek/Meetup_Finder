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
    el_id = models.AutoField(primary_key=True)
    el_title = models.CharField(max_length=50)
    el_description = models.CharField(max_length=1000, blank=True, null=True)
    el_id_place = models.ForeignKey('Placelist', models.DO_NOTHING, db_column='el_id_place')
    el_date = models.DateTimeField()
    el_time = models.TimeField()
    el_link = models.CharField(max_length=100)
    el_chk_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventlist'


class Eventtaglist(models.Model):
    etl_id = models.AutoField(primary_key=True)
    etl_id_event = models.ForeignKey(Eventlist, models.DO_NOTHING, db_column='etl_id_event')
    etl_id_tag = models.ForeignKey('Taglist', models.DO_NOTHING, db_column='etl_id_tag')

    class Meta:
        managed = False
        db_table = 'eventtaglist'


class Placelist(models.Model):
    pl_id = models.AutoField(primary_key=True)
    pl_city = models.CharField(max_length=30)
    pl_str_name = models.CharField(max_length=30)
    pl_house_num = models.IntegerField()
    pl_letter = models.CharField(max_length=1, blank=True, null=True)
    pl_place_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'placelist'


class Taglist(models.Model):
    tl_id = models.AutoField(primary_key=True)
    tl_title = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'taglist'


class Userlist(models.Model):
    ul_id = models.AutoField(primary_key=True)
    ul_login = models.CharField(max_length=20)
    ul_password = models.CharField(max_length=20)
    ul_name = models.CharField(max_length=20, blank=True, null=True)
    ul_surname = models.CharField(max_length=20, blank=True, null=True)
    ul_secondname = models.CharField(max_length=20, blank=True, null=True)
    ul_email = models.CharField(max_length=30)
    ul_linkvkmessage = models.CharField(max_length=30, blank=True, null=True)
    ul_linktgmessage = models.CharField(max_length=30, blank=True, null=True)
    ul_chk_mailing = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userlist'


class Usertaglist(models.Model):
    utl_id = models.AutoField(primary_key=True)
    utl_id_user = models.ForeignKey(Userlist, models.DO_NOTHING, db_column='utl_id_user')
    utl_id_tag = models.ForeignKey(Taglist, models.DO_NOTHING, db_column='utl_id_tag')

    class Meta:
        managed = False
        db_table = 'usertaglist'
