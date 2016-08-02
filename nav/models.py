from django.db.models import (Model, AutoField, CharField, TextField,
                              IntegerField, PositiveIntegerField, SmallIntegerField,
                              ForeignKey, OneToOneField, ManyToManyField, CASCADE)
from django.utils.translation import ugettext_lazy as _


class Term(Model):
    tid = AutoField(primary_key=True)
    vid = PositiveIntegerField()
    name = CharField(max_length=255)
    description = TextField()
    weight = SmallIntegerField()
    language = CharField(max_length=12)
    trid = IntegerField()
    nodes = ManyToManyField('nodes.Node', related_name='terms', through='TermNode')

    class Meta:
        db_table = 'term_data'
        managed = False

    def __unicode__(self):
        return u'{} "{}"'.format(self.tid, self.name)

    def get_absolute_url(self):
        return u'{}/tag/{}'.format('/' + self.language if self.language else '', self.name)


class TermNode(Model):
    term = ForeignKey(Term, CASCADE, db_column='tid')
    vid = PositiveIntegerField(primary_key=True)  # FAKE! Prevents attempts to use 'id'!
    node = ForeignKey('nodes.Node', CASCADE, db_column='nid')

    class Meta:
        db_table = 'term_node'
        managed = False


class TermHierarchy(Model):
    term = OneToOneField(Term, CASCADE, db_column='tid', related_name='hier',
                         primary_key=True)
    parent = ForeignKey(Term, CASCADE, db_column='parent', related_name='children')

    class Meta:
        db_table = 'term_hierarchy'
        managed = False

    def __unicode__(self):
        return unicode(self.term)


class UrlAlias(Model):
    pid = AutoField(primary_key=True)
    src = CharField(max_length=128)
    dst = CharField(max_length=128)
    language = CharField(max_length=12)

    class Meta:
        db_table = 'url_alias'
        managed = False
        verbose_name = _('URL Alias')
        verbose_name_plural = _('URL Aliases')
