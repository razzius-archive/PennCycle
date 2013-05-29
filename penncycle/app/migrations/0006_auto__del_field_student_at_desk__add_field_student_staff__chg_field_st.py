# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Student.at_desk'
        db.delete_column(u'app_student', 'at_desk')

        # Adding field 'Student.staff'
        db.add_column(u'app_student', 'staff',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Student.phone'
        db.alter_column(u'app_student', 'phone', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20))

    def backwards(self, orm):
        # Adding field 'Student.at_desk'
        db.add_column(u'app_student', 'at_desk',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Student.staff'
        db.delete_column(u'app_student', 'staff')


        # Changing field 'Student.phone'
        db.alter_column(u'app_student', 'phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20))

    models = {
        u'app.bike': {
            'Meta': {'object_name': 'Bike'},
            'bike_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'combo': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'combo_update': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_serial_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Manufacturer']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'}),
            'tag_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'app.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_problem': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ride': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Ride']", 'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Student']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'app.info': {
            'Meta': {'object_name': 'Info'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        },
        u'app.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'app.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'app.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['app.Plan']"}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': u"orm['app.Student']"})
        },
        u'app.plan': {
            'Meta': {'object_name': 'Plan'},
            'banner': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'Details coming soon!'", 'max_length': '150'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'app.ride': {
            'Meta': {'object_name': 'Ride'},
            'bike': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rides'", 'to': u"orm['app.Bike']"}),
            'checkin_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'checkins'", 'null': 'True', 'to': u"orm['app.Station']"}),
            'checkin_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'checkout_station': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'checkouts'", 'to': u"orm['app.Station']"}),
            'checkout_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_users': ('django.db.models.fields.IntegerField', [], {}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Student']"})
        },
        u'app.station': {
            'Meta': {'object_name': 'Station'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'full_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'hours': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '39.9529399'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '-75.1905607'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'app.student': {
            'Meta': {'object_name': 'Student'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'grad_year': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'last_two': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'living_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'penncard': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'phone': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20'}),
            'plan': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['app.Plan']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'staff': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'waiver_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['app']