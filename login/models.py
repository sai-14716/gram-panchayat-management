# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    citizenid = models.ForeignKey('Citizen', models.DO_NOTHING, db_column='citizenid', blank=True, null=True)
    citizenid_0 = models.ForeignKey('Citizen', models.DO_NOTHING, db_column='citizenid_id', related_name='user_citizenid_0_set', blank=True, null=True)  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'User'


class Application(models.Model):
    applicationid = models.AutoField(primary_key=True)
    applicationdate = models.DateField()
    status = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)
    citizenid = models.ForeignKey('Citizen', models.DO_NOTHING, db_column='citizenid', blank=True, null=True)
    programid = models.ForeignKey('Welfareprogram', models.DO_NOTHING, db_column='programid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'application'


class Asset(models.Model):
    assetid = models.AutoField(primary_key=True)
    assettype = models.CharField(max_length=100)
    location = models.TextField(blank=True, null=True)
    installationdate = models.DateField(blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True)
    lastmaintenancedate = models.DateField(blank=True, null=True)
    householdid = models.ForeignKey('Household', models.DO_NOTHING, db_column='householdid', blank=True, null=True)
    panchayatid = models.ForeignKey('Panchayat', models.DO_NOTHING, db_column='panchayatid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Censusevent(models.Model):
    censuseventid = models.AutoField(primary_key=True)
    eventtype = models.CharField(max_length=100)
    eventdate = models.DateField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'censusevent'


class Censusparticipation(models.Model):
    censuseventid = models.OneToOneField(Censusevent, models.DO_NOTHING, db_column='censuseventid', primary_key=True)  # The composite primary key (censuseventid, citizenid) found, that is not supported. The first column is selected.
    citizenid = models.ForeignKey('Citizen', models.DO_NOTHING, db_column='citizenid')

    class Meta:
        managed = False
        db_table = 'censusparticipation'
        unique_together = (('censuseventid', 'citizenid'),)


class Citizen(models.Model):
    citizenid = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    dateofbirth = models.DateField()
    gender = models.CharField(max_length=50, blank=True, null=True)
    contactnumber = models.CharField(max_length=20, blank=True, null=True)
    fatherid = models.ForeignKey('self', models.DO_NOTHING, db_column='fatherid', blank=True, null=True)
    motherid = models.ForeignKey('self', models.DO_NOTHING, db_column='motherid', related_name='citizen_motherid_set', blank=True, null=True)
    educationlevel = models.CharField(max_length=100, blank=True, null=True)
    householdid = models.ForeignKey('Household', models.DO_NOTHING, db_column='householdid', blank=True, null=True)
    panchayatid = models.ForeignKey('Panchayat', models.DO_NOTHING, db_column='panchayatid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'citizen'


class Cultivationrecord(models.Model):
    cultivationid = models.AutoField(primary_key=True)
    year = models.IntegerField()
    season = models.CharField(max_length=50, blank=True, null=True)
    croptype = models.CharField(max_length=100, blank=True, null=True)
    cultivatedarea = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    yield_field = models.DecimalField(db_column='yield', max_digits=10, decimal_places=2, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    householdid = models.ForeignKey('Household', models.DO_NOTHING, db_column='householdid', blank=True, null=True)
    landid = models.ForeignKey('Land', models.DO_NOTHING, db_column='landid', blank=True, null=True)
    panchayatid = models.ForeignKey('Panchayat', models.DO_NOTHING, db_column='panchayatid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cultivationrecord'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Household(models.Model):
    householdid = models.AutoField(primary_key=True)
    address = models.TextField()
    annualincome = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    totalmembers = models.IntegerField(blank=True, null=True)
    propertyvalue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    panchayatid = models.ForeignKey('Panchayat', models.DO_NOTHING, db_column='panchayatid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'household'


class Land(models.Model):
    landid = models.AutoField(primary_key=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.TextField()
    householdid = models.ForeignKey(Household, models.DO_NOTHING, db_column='householdid', blank=True, null=True)
    panchayatid = models.ForeignKey('Panchayat', models.DO_NOTHING, db_column='panchayatid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'land'


class LoginPanchayat(models.Model):
    panchayatid = models.AutoField(primary_key=True)
    panchayatname = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'login_panchayat'


class Panchayat(models.Model):
    panchayatid = models.AutoField(primary_key=True)
    panchayatname = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'panchayat'


class Servicerequest(models.Model):
    requestid = models.AutoField(primary_key=True)
    requesttype = models.CharField(max_length=100)
    requestdate = models.DateField()
    status = models.CharField(max_length=50)
    citizenid = models.ForeignKey(Citizen, models.DO_NOTHING, db_column='citizenid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicerequest'


class Vaccinationrecord(models.Model):
    vaccinationid = models.AutoField(primary_key=True)
    vaccinename = models.CharField(max_length=100)
    dateadministered = models.DateField()
    citizenid = models.ForeignKey(Citizen, models.DO_NOTHING, db_column='citizenid', blank=True, null=True)
    panchayatid = models.ForeignKey(Panchayat, models.DO_NOTHING, db_column='panchayatid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vaccinationrecord'


class Welfareprogram(models.Model):
    programid = models.AutoField(primary_key=True)
    programname = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    eligibilitycriteria = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    startdate = models.DateField()
    managingdepartment = models.CharField(max_length=255, blank=True, null=True)
    expirydate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'welfareprogram'

class Employee(models.Model):
    employeeid = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20)
    citizenid = models.ForeignKey(Citizen, models.CASCADE, db_column='citizenid', blank=False, null=False, related_name="employee")

    def __str__(self):
        return f"{self.citizenid} is an employee with the role {self.role}"