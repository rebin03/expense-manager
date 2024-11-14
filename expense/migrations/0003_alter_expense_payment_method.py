# Generated by Django 5.1.3 on 2024-11-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='payment_method',
            field=models.CharField(choices=[(None, 'Select'), ('card', 'Card'), ('cash', 'Cash'), ('upi', 'UPI')], default='Select', max_length=10),
        ),
    ]