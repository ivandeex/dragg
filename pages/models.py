from django.db.models import (Model, Min,
                              CharField, TextField, URLField,
                              AutoField, IntegerField, PositiveIntegerField,
                              SmallIntegerField, PositiveSmallIntegerField,
                              ForeignKey, OneToOneField, CASCADE, SET_NULL)
from unixtimestampfield.fields import UnixTimeStampField
from lib.models import BooleanIntField, BooleanSmallIntField
from django.utils.translation import ugettext_lazy as _


class FilterFormat(Model):
    format = AutoField(primary_key=True)
    name = CharField(max_length=255)
    roles = CharField(max_length=255)
    cache = BooleanSmallIntField()

    class Meta:
        db_table = 'filter_formats'
        managed = False


class Filter(Model):
    fid = AutoField(primary_key=True)
    format = ForeignKey(FilterFormat, CASCADE, db_column='format', related_name='filters')
    module = CharField(max_length=64)
    delta = PositiveSmallIntegerField()
    weight = SmallIntegerField()

    class Meta:
        db_table = 'filters'
        managed = False


class NodeType(Model):
    type = CharField(max_length=32, primary_key=True)
    name = CharField(max_length=255)
    module = CharField(max_length=255)
    description = TextField()
    help = TextField()
    has_title = BooleanSmallIntField()
    title_label = CharField(max_length=255)
    has_body = BooleanSmallIntField()
    body_label = CharField(max_length=255)
    min_word_count = PositiveSmallIntegerField()
    custom = PositiveSmallIntegerField()
    modified = BooleanSmallIntField()
    locked = BooleanSmallIntField()
    orig_type = CharField(max_length=255)

    class Meta:
        db_table = 'node_type'
        managed = False

    def __unicode__(self):
        return u'%s' % self.type


class Node(Model):
    nid = AutoField(primary_key=True)
    rev = OneToOneField('NodeRev', SET_NULL, db_column='vid',
                        related_name='+', null=True, blank=True)
    type = ForeignKey(NodeType, CASCADE, db_column='type')
    language = CharField(max_length=12, blank=True)
    title = CharField(max_length=255)
    uid = PositiveIntegerField()
    status = PositiveIntegerField()
    created = UnixTimeStampField()
    changed = UnixTimeStampField()
    comment = PositiveIntegerField()
    promote = BooleanIntField()
    moderate = BooleanIntField()
    sticky = BooleanIntField()
    trans_node = ForeignKey('self', SET_NULL, db_column='tnid',
                            related_name='+', null=True, blank=True)
    translate = BooleanIntField()

    class Meta:
        db_table = 'node'
        managed = False
        default_permissions = ()

    def __unicode__(self):
        return u'{} "{}"'.format(self.nid, self.title)

    def story_url(self):
        if self.type_id == 'story':
            return self.rev.story_link.url

    def url(self):
        from nav.models import UrlAlias
        lang_url = self.language + '/' if self.language and self.language != 'en' else ''
        raw_url = 'node/%d' % self.nid
        alias = UrlAlias.objects.filter(src=raw_url).aggregate(Min('dst'))['dst__min']
        return lang_url + (alias or raw_url)
    url.short_description = _('Node URL')


class NodeRev(Model):
    node = ForeignKey(Node, CASCADE, db_column='nid', related_name='revs')
    vid = AutoField(primary_key=True)
    uid = IntegerField()
    title = CharField(max_length=255)
    body = TextField(blank=True)
    teaser = TextField(blank=True)
    log = TextField()
    timestamp = UnixTimeStampField()
    format = ForeignKey(FilterFormat, SET_NULL, db_column='format',
                        related_name='+', null=True, blank=True)

    class Meta:
        db_table = 'node_revisions'
        managed = False
        default_permissions = ()

    def __unicode__(self):
        return u'{} ({}) "{}"'.format(self.vid, self.node_id, self.title)


class NodeAccess(Model):
    node = OneToOneField(Node, CASCADE, db_column='nid', related_name='access',
                         primary_key=True)
    gid = PositiveIntegerField()
    realm = CharField(max_length=255)
    grant_view = BooleanSmallIntField()
    grant_update = BooleanSmallIntField()
    grant_delete = BooleanSmallIntField()

    class Meta:
        db_table = 'node_access'
        managed = False

    def __unicode__(self):
        return u'{} "{}" v={} u={} d={}'.format(
            self.gid, self.realm,
            self.grant_view, self.grant_update, self.grant_delete)


class StoryLink(Model):
    rev = OneToOneField(NodeRev, CASCADE, db_column='vid', related_name='story_link',
                        primary_key=True)
    node = ForeignKey(Node, CASCADE, db_column='nid', related_name='+')
    url = URLField(max_length=2048, db_column='field_story_url_url', null=True, blank=True)
    title = CharField(max_length=2048, db_column='field_story_url_title',
                      null=True, blank=True)
    attrs = TextField(db_column='field_story_url_attributes',
                      null=True, blank=True)

    class Meta:
        db_table = 'content_type_story'
        managed = False
