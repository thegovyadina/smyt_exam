# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'users'
        db.create_table(u'dynamic_models_users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            (u'paycheck', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            (u'date_joined', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dynamic_models', ['users'])

        # Adding model 'rooms'
        db.create_table(u'dynamic_models_rooms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'department', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            (u'spots', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dynamic_models', ['rooms'])


    def backwards(self, orm):
        # Deleting model 'users'
        db.delete_table(u'dynamic_models_users')

        # Deleting model 'rooms'
        db.delete_table(u'dynamic_models_rooms')


    models = {
        u'dynamic_models.rooms': {
            'Meta': {'object_name': 'rooms'},
            u'department': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'spots': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dynamic_models.users': {
            'Meta': {'object_name': 'users'},
            u'date_joined': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'paycheck': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dynamic_models']