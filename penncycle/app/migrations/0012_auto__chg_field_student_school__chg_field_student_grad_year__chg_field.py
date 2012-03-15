# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Student.school'
        db.alter_column('app_student', 'school', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Student.grad_year'
        db.alter_column('app_student', 'grad_year', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Student.phone'
        db.alter_column('app_student', 'phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=128))


    def backwards(self, orm):
        
        # Changing field 'Student.school'
        db.alter_column('app_student', 'school', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'Student.grad_year'
        db.alter_column('app_student', 'grad_year', self.gf('django.db.models.fields.CharField')(max_length=5))

        # Changing field 'Student.phone'
        db.alter_column('app_student', 'phone', self.gf('django.db.models.fields.CharField')(max_length=16))


    models = {
        'app.bike': {
            'Meta': {'object_name': 'Bike'},
            'bike_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Manufacturer']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'}),
            'tag_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'app.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'app.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'app.ride': {
            'Meta': {'object_name': 'Ride'},
            'bike': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rides'", 'to': "orm['app.Bike']"}),
            'checkin_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'checkins'", 'null': 'True', 'to': "orm['app.Station']"}),
            'checkin_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'checkout_station': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'checkouts'", 'to': "orm['app.Station']"}),
            'checkout_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_users': ('django.db.models.fields.IntegerField', [], {}),
            'rider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Student']"})
        },
        'app.station': {
            'Meta': {'object_name': 'Station'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '39.9529399'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '-75.1905607'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'app.student': {
            'Meta': {'object_name': 'Student'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'grad_year': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 3, 15)'}),
            'living_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'penncard_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '128'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'}),
            'waiver_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['app']
