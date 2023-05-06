# Generated by Django 3.2.18 on 2023-05-06 12:13

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='images/users/pictures'),
        ),
    ]
