# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ForwardRule'
        db.create_table('inbox_forwardrule', (
            ('inboxsettings_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inbox.InboxSettings'], unique=True, primary_key=True)),
            ('mask', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_directly', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('period', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('email_to', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('inbox', ['ForwardRule'])

        # Adding model 'InboxSettings'
        db.create_table('inbox_inboxsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inbox', self.gf('django.db.models.fields.related.ForeignKey')(related_name='settings', to=orm['inbox.Inbox'])),
        ))
        db.send_create_signal('inbox', ['InboxSettings'])

        # Adding model 'DeleteRule'
        db.create_table('inbox_deleterule', (
            ('inboxsettings_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inbox.InboxSettings'], unique=True, primary_key=True)),
            ('mask', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_directly', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('period', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('inbox', ['DeleteRule'])

        # Adding field 'Mail.bcc'
        db.add_column('inbox_mail', 'bcc',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Mail.cc'
        db.add_column('inbox_mail', 'cc',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Mail.content_type'
        db.add_column('inbox_mail', 'content_type',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field readers on 'Mail'
        db.create_table('inbox_mail_readers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mail', models.ForeignKey(orm['inbox.mail'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('inbox_mail_readers', ['mail_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'ForwardRule'
        db.delete_table('inbox_forwardrule')

        # Deleting model 'InboxSettings'
        db.delete_table('inbox_inboxsettings')

        # Deleting model 'DeleteRule'
        db.delete_table('inbox_deleterule')

        # Deleting field 'Mail.bcc'
        db.delete_column('inbox_mail', 'bcc')

        # Deleting field 'Mail.cc'
        db.delete_column('inbox_mail', 'cc')

        # Deleting field 'Mail.content_type'
        db.delete_column('inbox_mail', 'content_type')

        # Removing M2M table for field readers on 'Mail'
        db.delete_table('inbox_mail_readers')


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
            'Meta': {'object_name': 'DeleteRule'},
            'inboxsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inbox.InboxSettings']", 'unique': 'True', 'primary_key': 'True'}),
            'is_directly': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mask': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'inbox.forwardrule': {
            'Meta': {'object_name': 'ForwardRule'},
            'email_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'inboxsettings_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inbox.InboxSettings']", 'unique': 'True', 'primary_key': 'True'}),
            'is_directly': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mask': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'inbox.inbox': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Inbox'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'inboxes'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'inbox.inboxsettings': {
            'Meta': {'object_name': 'InboxSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbox': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'settings'", 'to': "orm['inbox.Inbox']"})
        },
        'inbox.mail': {
            'Meta': {'object_name': 'Mail'},
            'bcc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbox': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mails'", 'to': "orm['inbox.Inbox']"}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'peer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'raw': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mails'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'subject': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'to_email': ('django.db.models.fields.TextField', [], {}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inbox']