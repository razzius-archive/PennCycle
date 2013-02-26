# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Plan'
        db.create_table('app_plan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cost', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(default='Details coming soon!', max_length=150)),
        ))
        db.send_create_signal('app', ['Plan'])

        # Adding model 'Payment'
        db.create_table('app_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['app.Plan'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments', to=orm['app.Student'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('satisfied', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='available', max_length=100)),
        ))
        db.send_create_signal('app', ['Payment'])

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
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('penncard', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('last_two', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('grad_year', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('join_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2013, 2, 25))),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('living_location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('waiver_signed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('at_desk', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('app', ['Student'])

        # Adding M2M table for field plan on 'Student'
        db.create_table('app_student_plan', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['app.student'], null=False)),
            ('plan', models.ForeignKey(orm['app.plan'], null=False))
        ))
        db.create_unique('app_student_plan', ['student_id', 'plan_id'])

        # Adding model 'Bike'
        db.create_table('app_bike', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bike_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Manufacturer'])),
            ('purchase_date', self.gf('django.db.models.fields.DateField')()),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='available', max_length=100)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tag_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('key_serial_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('combo', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('combo_update', self.gf('django.db.models.fields.DateField')()),
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
            ('capacity', self.gf('django.db.models.fields.IntegerField')(default=15)),
        ))
        db.send_create_signal('app', ['Station'])

        # Adding model 'Ride'
        db.create_table('app_ride', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Student'])),
            ('bike', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rides', to=orm['app.Bike'])),
            ('checkout_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('checkin_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('checkout_station', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='checkouts', to=orm['app.Station'])),
            ('checkin_station', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='checkins', null=True, to=orm['app.Station'])),
            ('num_users', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('app', ['Ride'])

        # Adding model 'Page'
        db.create_table('app_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('app', ['Page'])

        # Adding model 'Comment'
        db.create_table('app_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Student'], null=True, blank=True)),
            ('ride', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Ride'], null=True, blank=True)),
            ('is_problem', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Comment'])


    def backwards(self, orm):
        
        # Deleting model 'Plan'
        db.delete_table('app_plan')

        # Deleting model 'Payment'
        db.delete_table('app_payment')

        # Deleting model 'Manufacturer'
        db.delete_table('app_manufacturer')

        # Deleting model 'Student'
        db.delete_table('app_student')

        # Removing M2M table for field plan on 'Student'
        db.delete_table('app_student_plan')

        # Deleting model 'Bike'
        db.delete_table('app_bike')

        # Deleting model 'Station'
        db.delete_table('app_station')

        # Deleting model 'Ride'
        db.delete_table('app_ride')

        # Deleting model 'Page'
        db.delete_table('app_page')

        # Deleting model 'Comment'
        db.delete_table('app_comment')


    models = {
        'app.bike': {
            'Meta': {'object_name': 'Bike'},
            'bike_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'combo': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'combo_update': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_serial_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Manufacturer']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'}),
            'tag_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'app.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_problem': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ride': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Ride']", 'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Student']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
        'app.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['app.Plan']"}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '100'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments'", 'to': "orm['app.Student']"})
        },
        'app.plan': {
            'Meta': {'object_name': 'Plan'},
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'Details coming soon!'", 'max_length': '150'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
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
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '39.9529399'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '-75.1905607'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'app.student': {
            'Meta': {'object_name': 'Student'},
            'at_desk': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'grad_year': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2013, 2, 25)'}),
            'last_two': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'living_location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'penncard': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'plan': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['app.Plan']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'waiver_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['app']
