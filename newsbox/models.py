from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
from django.utils import timezone


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    val = models.CharField(max_length=200)
    str_ini = UnixTimeStampField(default='0.0')
    float_ini = UnixTimeStampField(default=0.0)
    int_ini = UnixTimeStampField(default=0)
    dt_ini = UnixTimeStampField(default=timezone.now)
    num_field = UnixTimeStampField(use_numeric=True, default=0.0)
    int2_field = UnixTimeStampField(use_numeric=False, default=0)
    int3_field = UnixTimeStampField(use_numeric=True, default=0)
    int4_field = UnixTimeStampField(use_numeric=False, default=0, round_to=0)


class Node(models.Model):
    nid = models.AutoField(primary_key=True)
    rev = models.OneToOneField('NodeRevisions', on_delete=models.SET_NULL,
                               db_column='vid', related_name='+',
                               null=True, blank=True)
    type = models.CharField(max_length=32)
    language = models.CharField(max_length=12)
    title = models.CharField(max_length=255)
    uid = models.IntegerField()
    status = models.IntegerField()
    created = UnixTimeStampField()
    changed = UnixTimeStampField()
    comment = models.IntegerField()
    promote = models.BooleanField()
    moderate = models.BooleanField()
    sticky = models.BooleanField()
    tnid = models.IntegerField()
    translate = models.BooleanField()

    class Meta:
        db_table = 'node'
        managed = False

    def __unicode__(self):
        return u'{} "{}"'.format(self.nid, self.title)


class NodeRevisions(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE,
                             db_column='nid', related_name='revs')
    vid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    teaser = models.TextField()
    log = models.TextField()
    timestamp = UnixTimeStampField()
    format = models.IntegerField()

    class Meta:
        db_table = 'node_revisions'
        managed = False

    def __unicode__(self):
        return u'{} ({}) "{}"'.format(self.vid, self.node_id, self.title)
