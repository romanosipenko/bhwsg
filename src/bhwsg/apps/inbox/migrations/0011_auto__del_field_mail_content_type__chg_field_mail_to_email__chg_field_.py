# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Mail.content_type'
        db.delete_column('inbox_mail', 'content_type')


        # Changing field 'Mail.to_email'
        db.alter_column('inbox_mail', 'to_email', self.gf('core.fields.JSONField')())

        # Changing field 'Mail.cc'
        db.alter_column('inbox_mail', 'cc', self.gf('core.fields.JSONField')(null=True))

        # Changing field 'Mail.bcc'
        db.alter_column('inbox_mail', 'bcc', self.gf('core.fields.JSONField')(null=True))

    def backwards(self, orm):
        # Adding field 'Mail.content_type'
        db.add_column('inbox_mail', 'content_type',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Mail.to_email'
        db.alter_column('inbox_mail', 'to_email', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Mail.cc'
        db.alter_column('inbox_mail', 'cc', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Mail.bcc'
        db.alter_column('inbox_mail', 'bcc', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'inbox.deleterule': {
            'Meta': {'object_name': 'DeleteRule', '_ormbases': ['inbox.InboxSettings']},
            'inboxsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inbox.InboxSettings']", 'unique': 'True', 'primary_key': 'True'}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'inbox.forwardrule': {
            'Meta': {'object_name': 'ForwardRule', '_ormbases': ['inbox.InboxSettings']},
            'email_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'inboxsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inbox.InboxSettings']", 'unique': 'True', 'primary_key': 'True'})
        },
        'inbox.inbox': {
            'Meta': {'ordering': "('slug',)", 'unique_together': "(('title', 'label'),)", 'object_name': 'Inbox'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_inboxes'", 'null': 'True', 'to': "orm['auth.User']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'inboxes'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'inbox.inboxsettings': {
            'Meta': {'object_name': 'InboxSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbox': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'settings'", 'to': "orm['inbox.Inbox']"}),
            'mask': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'inbox.mail': {
            'Meta': {'object_name': 'Mail'},
            'bcc': ('core.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'cc': ('core.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'content_types': ('core.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbox': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mails'", 'to': "orm['inbox.Inbox']"}),
            'peer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'raw': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mails'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'subject': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'to_email': ('core.fields.JSONField', [], {}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'inbox.mailattachment': {
            'Meta': {'object_name': 'MailAttachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['inbox.Mail']"})
        }
    }

    complete_apps = ['inbox']