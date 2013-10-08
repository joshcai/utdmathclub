# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.kind'
        db.add_column(u'blog_post', 'kind',
                      self.gf('django.db.models.fields.CharField')(default='post', max_length=120),
                      keep_default=False)

        # Adding field 'Post.link'
        db.add_column(u'blog_post', 'link',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.kind'
        db.delete_column(u'blog_post', 'kind')

        # Deleting field 'Post.link'
        db.delete_column(u'blog_post', 'link')


    models = {
        u'blog.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_rendered': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'date_str': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'post'", 'max_length': '120'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'blog.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['blog']