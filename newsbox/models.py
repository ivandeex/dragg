from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
from django.utils.translation import ugettext_lazy as _


class BooleanIntField(models.BooleanField):
    description = _('Boolean represented as int4')

    def __init__(self, *args, **kwargs):
        super(BooleanIntField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'PositiveIntegerField'

    def to_python(self, value):
        if isinstance(value, int):
            return value != 0
        return super(BooleanIntField, self).to_python(value)

    def get_prep_value(self, value):
        value = super(BooleanIntField, self).get_prep_value(value)
        return None if value is None else int(value)


class BooleanSmallIntField(BooleanIntField):
    description = _('Boolean represented as int2')

    def get_internal_type(self):
        return 'PositiveSmallIntegerField'


class FilterFormat(models.Model):
    format = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    roles = models.CharField(max_length=255)
    cache = BooleanSmallIntField()

    class Meta:
        db_table = 'filter_formats'
        managed = False


class Filter(models.Model):
    fid = models.AutoField(primary_key=True)
    format = models.ForeignKey(FilterFormat, models.CASCADE, db_column='format',
                               related_name='filters')
    module = models.CharField(max_length=64)
    delta = models.PositiveSmallIntegerField()
    weight = models.SmallIntegerField()

    class Meta:
        db_table = 'filters'
        managed = False


class NodeType(models.Model):
    type = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    description = models.TextField()
    help = models.TextField()
    has_title = BooleanSmallIntField()
    title_label = models.CharField(max_length=255)
    has_body = BooleanSmallIntField()
    body_label = models.CharField(max_length=255)
    min_word_count = models.PositiveSmallIntegerField()
    custom = models.PositiveSmallIntegerField()
    modified = BooleanSmallIntField()
    locked = BooleanSmallIntField()
    orig_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'node_type'
        managed = False

    def __unicode__(self):
        return u'%s' % self.type


class Node(models.Model):
    nid = models.AutoField(primary_key=True)
    rev = models.OneToOneField('NodeRev', models.SET_NULL, db_column='vid',
                               related_name='+', null=True, blank=True)
    type = models.ForeignKey(NodeType, models.CASCADE, db_column='type')
    language = models.CharField(max_length=12, blank=True)
    title = models.CharField(max_length=255)
    uid = models.PositiveIntegerField()
    status = models.PositiveIntegerField()
    created = UnixTimeStampField()
    changed = UnixTimeStampField()
    comment = models.PositiveIntegerField()
    promote = BooleanIntField()
    moderate = BooleanIntField()
    sticky = BooleanIntField()
    trans_node = models.ForeignKey('self', models.SET_NULL, db_column='tnid',
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
        lang_url = self.language + '/' if self.language and self.language != 'en' else ''
        raw_url = 'node/%d' % self.nid
        alias = UrlAlias.objects.filter(src=raw_url).aggregate(models.Min('dst'))['dst__min']
        return lang_url + (alias or raw_url)
    url.short_description = _('Node URL')


class NodeRev(models.Model):
    node = models.ForeignKey(Node, models.CASCADE, db_column='nid',
                             related_name='revs')
    vid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    teaser = models.TextField(blank=True)
    log = models.TextField()
    timestamp = UnixTimeStampField()
    format = models.ForeignKey(FilterFormat, models.SET_NULL, db_column='format',
                               related_name='+', null=True, blank=True)

    class Meta:
        db_table = 'node_revisions'
        managed = False
        default_permissions = ()

    def __unicode__(self):
        return u'{} ({}) "{}"'.format(self.vid, self.node_id, self.title)


class NodeAccess(models.Model):
    node = models.OneToOneField(Node, models.CASCADE, primary_key=True,
                                db_column='nid', related_name='access')
    gid = models.PositiveIntegerField()
    realm = models.CharField(max_length=255)
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


class StoryLink(models.Model):
    rev = models.OneToOneField(NodeRev, models.CASCADE, db_column='vid',
                               related_name='story_link', primary_key=True)
    node = models.ForeignKey(Node, models.CASCADE, db_column='nid', related_name='+')
    url = models.URLField(max_length=2048, db_column='field_story_url_url',
                          null=True, blank=True)
    title = models.CharField(max_length=2048, db_column='field_story_url_title',
                             null=True, blank=True)
    attrs = models.TextField(db_column='field_story_url_attributes',
                             null=True, blank=True)

    class Meta:
        db_table = 'content_type_story'
        managed = False


class Term(models.Model):
    tid = models.AutoField(primary_key=True)
    vid = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.SmallIntegerField()
    language = models.CharField(max_length=12)
    trid = models.IntegerField()
    nodes = models.ManyToManyField(Node, related_name='terms', through='TermNode')

    class Meta:
        db_table = 'term_data'
        managed = False

    def __unicode__(self):
        return u'{} "{}"'.format(self.tid, self.name)


class TermNode(models.Model):
    term = models.ForeignKey(Term, models.CASCADE, db_column='tid')
    vid = models.PositiveIntegerField(primary_key=True)  # FAKE! Prevents attempts to use 'id'!
    node = models.ForeignKey(Node, models.CASCADE, db_column='nid')

    class Meta:
        db_table = 'term_node'
        managed = False


class TermHierarchy(models.Model):
    term = models.OneToOneField(Term, models.CASCADE, db_column='tid',
                                related_name='hier', primary_key=True)
    parent = models.ForeignKey(Term, models.CASCADE, db_column='parent',
                               related_name='children')

    class Meta:
        db_table = 'term_hierarchy'
        managed = False

    def __unicode__(self):
        return unicode(self.term)


class UrlAlias(models.Model):
    pid = models.AutoField(primary_key=True)
    src = models.CharField(max_length=128)
    dst = models.CharField(max_length=128)
    language = models.CharField(max_length=12)

    class Meta:
        db_table = 'url_alias'
        managed = False
        verbose_name = _('URL Alias')
        verbose_name_plural = _('URL Aliases')


class NewsCategory(models.Model):
    cid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    block = models.SmallIntegerField()

    class Meta:
        db_table = 'aggregator_category'
        managed = False
        verbose_name_plural = _('News categories')


class NewsFeed(models.Model):
    fid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url = models.URLField(_('URL'), max_length=255)
    refresh = models.IntegerField()  # interval in seconds
    checked = UnixTimeStampField()
    link = models.URLField(max_length=255)
    description = models.TextField()
    image = models.TextField()
    etag = models.CharField(max_length=255)
    modified = UnixTimeStampField()
    block = models.SmallIntegerField()
    categories = models.ManyToManyField(NewsCategory, related_name='feeds',
                                        through='NewsFeedCategory')

    class Meta:
        db_table = 'aggregator_feed'
        managed = False

    def category_list(self):
        return ', '.join(sorted(self.categories.values_list('title', flat=True)))

    def item_count(self):
        return self.items.count()


class NewsFeedCategory(models.Model):
    feed = models.ForeignKey(NewsFeed, models.CASCADE, db_column='fid',
                             primary_key=True)  # FAKE! Prevents attempts to access 'id'!
    category = models.ForeignKey(NewsCategory, models.CASCADE, db_column='cid')

    class Meta:
        db_table = 'aggregator_category_feed'
        managed = False


class NewsItem(models.Model):
    iid = models.AutoField(primary_key=True)
    feed = models.ForeignKey(NewsFeed, models.SET_NULL, db_column='fid',
                             related_name='items', null=True, blank=True)
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = UnixTimeStampField()
    guid = models.CharField(max_length=255)

    class Meta:
        db_table = 'aggregator_item'
        managed = False

    def category_list(self):
        return self.feed.category_list()
