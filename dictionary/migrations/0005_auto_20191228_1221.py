# Generated by Django 3.0.1 on 2019-12-28 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_auto_20170905_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gloss',
            name='domhndsh',
            field=models.CharField(blank=True, choices=[('notset', 'No Value Set'), ('0.0', 'N/A'), ('0.1', 'Round'), ('0.2', 'Okay'), ('1.1', 'Point'), ('1.2', 'Hook'), ('2.1', 'Two'), ('2.2', 'Kneel'), ('2.3', 'Perth'), ('2.4', 'Spoon'), ('2.5', 'Letter-n'), ('2.6', 'Wish'), ('3.1', 'Three'), ('3.2', 'Mother'), ('3.3', 'Letter-m'), ('4.1', 'Four'), ('5.1', 'Spread'), ('5.2', 'Ball'), ('5.3', 'Flat'), ('5.4', 'Thick'), ('5.5', 'Cup'), ('6.1', 'Good'), ('6.2', 'Bad'), ('7.1', 'Gun'), ('7.2', 'Letter-c'), ('7.3', 'Small'), ('7.4', 'Seven'), ('8.1', 'Eight'), ('9.1', 'Nine'), ('10.1', 'Fist'), ('10.2', 'Soon'), ('10.3', 'Ten'), ('11.1', 'Write'), ('12.1', 'Salt'), ('13.1', 'Middle'), ('14.1', 'Rude'), ('15.1', 'Ambivalent'), ('16.1', 'Love'), ('17.1', 'Animal'), ('18.1', 'Queer')], max_length=10, null=True, verbose_name='Initial Dominant Handshape'),
        ),
        migrations.AlterField(
            model_name='gloss',
            name='final_domhndsh',
            field=models.CharField(blank=True, choices=[('notset', 'No Value Set'), ('0.0', 'N/A'), ('0.1', 'Round'), ('0.2', 'Okay'), ('1.1', 'Point'), ('1.2', 'Hook'), ('2.1', 'Two'), ('2.2', 'Kneel'), ('2.3', 'Perth'), ('2.4', 'Spoon'), ('2.5', 'Letter-n'), ('2.6', 'Wish'), ('3.1', 'Three'), ('3.2', 'Mother'), ('3.3', 'Letter-m'), ('4.1', 'Four'), ('5.1', 'Spread'), ('5.2', 'Ball'), ('5.3', 'Flat'), ('5.4', 'Thick'), ('5.5', 'Cup'), ('6.1', 'Good'), ('6.2', 'Bad'), ('7.1', 'Gun'), ('7.2', 'Letter-c'), ('7.3', 'Small'), ('7.4', 'Seven'), ('8.1', 'Eight'), ('9.1', 'Nine'), ('10.1', 'Fist'), ('10.2', 'Soon'), ('10.3', 'Ten'), ('11.1', 'Write'), ('12.1', 'Salt'), ('13.1', 'Middle'), ('14.1', 'Rude'), ('15.1', 'Ambivalent'), ('16.1', 'Love'), ('17.1', 'Animal'), ('18.1', 'Queer')], max_length=10, null=True, verbose_name='Final Dominant Handshape'),
        ),
        migrations.AlterField(
            model_name='gloss',
            name='final_subhndsh',
            field=models.CharField(blank=True, choices=[('notset', 'No Value Set'), ('0.0', 'N/A'), ('0.1', 'Round'), ('0.2', 'Okay'), ('1.1', 'Point'), ('1.2', 'Hook'), ('2.1', 'Two'), ('2.2', 'Kneel'), ('2.3', 'Perth'), ('2.4', 'Spoon'), ('2.5', 'Letter-n'), ('2.6', 'Wish'), ('3.1', 'Three'), ('3.2', 'Mother'), ('3.3', 'Letter-m'), ('4.1', 'Four'), ('5.1', 'Spread'), ('5.2', 'Ball'), ('5.3', 'Flat'), ('5.4', 'Thick'), ('5.5', 'Cup'), ('6.1', 'Good'), ('6.2', 'Bad'), ('7.1', 'Gun'), ('7.2', 'Letter-c'), ('7.3', 'Small'), ('7.4', 'Seven'), ('8.1', 'Eight'), ('9.1', 'Nine'), ('10.1', 'Fist'), ('10.2', 'Soon'), ('10.3', 'Ten'), ('11.1', 'Write'), ('12.1', 'Salt'), ('13.1', 'Middle'), ('14.1', 'Rude'), ('15.1', 'Ambivalent'), ('16.1', 'Love'), ('17.1', 'Animal'), ('18.1', 'Queer')], max_length=10, null=True, verbose_name='Final Subordinate Handshape'),
        ),
        migrations.AlterField(
            model_name='gloss',
            name='subhndsh',
            field=models.CharField(blank=True, choices=[('notset', 'No Value Set'), ('0.0', 'N/A'), ('0.1', 'Round'), ('0.2', 'Okay'), ('1.1', 'Point'), ('1.2', 'Hook'), ('2.1', 'Two'), ('2.2', 'Kneel'), ('2.3', 'Perth'), ('2.4', 'Spoon'), ('2.5', 'Letter-n'), ('2.6', 'Wish'), ('3.1', 'Three'), ('3.2', 'Mother'), ('3.3', 'Letter-m'), ('4.1', 'Four'), ('5.1', 'Spread'), ('5.2', 'Ball'), ('5.3', 'Flat'), ('5.4', 'Thick'), ('5.5', 'Cup'), ('6.1', 'Good'), ('6.2', 'Bad'), ('7.1', 'Gun'), ('7.2', 'Letter-c'), ('7.3', 'Small'), ('7.4', 'Seven'), ('8.1', 'Eight'), ('9.1', 'Nine'), ('10.1', 'Fist'), ('10.2', 'Soon'), ('10.3', 'Ten'), ('11.1', 'Write'), ('12.1', 'Salt'), ('13.1', 'Middle'), ('14.1', 'Rude'), ('15.1', 'Ambivalent'), ('16.1', 'Love'), ('17.1', 'Animal'), ('18.1', 'Queer')], max_length=10, null=True, verbose_name='Initial Subordinate Handshape'),
        ),
    ]
