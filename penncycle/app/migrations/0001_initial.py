# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Manufacturer'
        db.create_table('app_manufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal('app', ['Manufacturer'])

        # Adding model 'Student'
        db.create_table('app_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('penncard_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('grad_year', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('join_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 3, 10))),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('living_location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('quiz_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waiver_signed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(default='available', max_length=100)),
        ))
        db.send_create_signal('app', ['Student'])

        # Adding model 'Bike'
        db.create_table('app_bike', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bike_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Manufacturer'])),
            ('purchase_date', self.gf('django.db.models.fields.DateField')()),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='available', max_length=100)),
        ))
        db.send_create_signal('app', ['Bike'])

        # Adding model 'Station'
        db.create_table('app_station', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=39.9529399)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=-75.1905607)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=100, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('app', ['Station'])

        # Adding model 'Ride'
        db.create_table('app_ride', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Student'])),
            ('bike', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rides', to=orm['app.Bike'])),
            ('checkout_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('checkin_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('checkout_station', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checkouts', to=orm['app.Station'])),
            ('checkin_station', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='checkins', null=True, to=orm['app.Station'])),
        ))
        db.send_create_signal('app', ['Ride'])

        # Adding model 'Quiz'
        db.create_table('app_quiz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wrong1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wrong2', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wrong3', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wrong4', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('app', ['Quiz'])


    def backwards(self, orm):
        
        # Deleting model 'Manufacturer'
        db.delete_table('app_manufacturer')

        # Deleting model 'Student'
        db.delete_table('app_student')

        # Deleting model 'Bike'
        db.delete_table('app_bike')

        # Deleting model 'Station'
        db.delete_table('app_station')

        # Deleting model 'Ride'
        db.delete_table('app_ride')

        # Deleting model 'Quiz'
        db.delete_table('app_quiz')


    models = {
        'app.bike': {
            'Meta': {'object_name': 'Bike'},
            'bike_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Manufacturer']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'})
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
        'app.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wrong1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wrong2': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wrong3': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wrong4': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'app.ride': {
            'Meta': {'object_name': 'Ride'},
            'bike': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rides'", 'to': "orm['app.Bike']"}),
            'checkin_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'checkins'", 'null': 'True', 'to': "orm['app.Station']"}),
            'checkin_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'checkout_station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkouts'", 'to': "orm['app.Station']"}),
            'checkout_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'grad_year': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 3, 10)'}),
            'living_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'penncard_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'quiz_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'}),
            'waiver_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['app']
