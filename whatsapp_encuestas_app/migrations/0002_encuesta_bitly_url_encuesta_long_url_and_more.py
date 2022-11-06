# Generated by Django 4.1.3 on 2022-11-05 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp_encuestas_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuesta',
            name='bitly_url',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='long_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='encuesta',
            name='email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='whatsapp_encuestas_app.email'),
        ),
    ]