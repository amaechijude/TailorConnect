# Generated by Django 5.0.6 on 2024-10-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_payment_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9999999999)),
                ('ref', models.CharField(max_length=300)),
                ('verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]