# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Eventlist(models.Model):
    el_id = models.AutoField(primary_key=True)
    el_title = models.CharField(max_length=50)
    el_description = models.CharField(max_length=1000, blank=True, null=True)
    el_id_place = models.ForeignKey('Placelist', models.DO_NOTHING, db_column='el_id_place')
    el_date = models.DateTimeField()
    el_time = models.TimeField()
    el_link = models.CharField(max_length=100)
    el_chk_active = models.IntegerField(blank=True, null=True)



class Eventtaglist(models.Model):
    etl_id = models.AutoField(primary_key=True)
    etl_id_event = models.ForeignKey(Eventlist, models.DO_NOTHING, db_column='etl_id_event')
    etl_id_tag = models.ForeignKey('Taglist', models.DO_NOTHING, db_column='etl_id_tag')



class Placelist(models.Model):
    pl_id = models.AutoField(primary_key=True)
    pl_city = models.CharField(max_length=30)
    pl_str_name = models.CharField(max_length=30)
    pl_house_num = models.IntegerField()
    pl_letter = models.CharField(max_length=1, blank=True, null=True)
    pl_place_name = models.CharField(max_length=30, blank=True, null=True)



class Taglist(models.Model):
    tl_id = models.AutoField(primary_key=True)
    tl_title = models.CharField(max_length=15)



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



class Usertaglist(models.Model):
    utl_id = models.AutoField(primary_key=True)
    utl_id_user = models.ForeignKey(Userlist, models.DO_NOTHING, db_column='utl_id_user')
    utl_id_tag = models.ForeignKey(Taglist, models.DO_NOTHING, db_column='utl_id_tag')