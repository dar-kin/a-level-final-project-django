# Generated by Django 3.2 on 2021-04-23 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema', '0003_session_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='books_number',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BookedSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_sessions', to='cinema.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
