# Generated by Django 2.2.6 on 2019-11-09 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowerinfo',
            name='loanNumber',
        ),
        migrations.RemoveField(
            model_name='loaninfo',
            name='loanNumber',
        ),
        migrations.RemoveField(
            model_name='propertyinfo',
            name='loanNumber',
        ),
        migrations.AddField(
            model_name='loanrequests',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.BorrowerInfo'),
        ),
        migrations.AddField(
            model_name='loanrequests',
            name='loanInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.LoanInfo'),
        ),
        migrations.AddField(
            model_name='loanrequests',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.PropertyInfo'),
        ),
    ]
