# Generated by Django 3.2.9 on 2022-05-31 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rentorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='residue',
            name='owner',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='app.user'),
            preserve_default=False,
        ),
    ]
