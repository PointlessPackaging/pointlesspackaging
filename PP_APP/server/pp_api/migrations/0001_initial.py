# Generated by Django 3.0.5 on 2020-05-07 04:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import pp_api.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Packager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('brand_name', models.CharField(default='-1', max_length=50)),
                ('count', models.IntegerField()),
                ('score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PPUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
            ],
        ),
        migrations.CreateModel(
            name='ImagePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_img', django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=95, size=[600, 300], upload_to=pp_api.models.top_img_path)),
                ('side_img', django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=95, size=[600, 300], upload_to=pp_api.models.side_img_path)),
                ('infer_img', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=95, size=[600, 300], upload_to=pp_api.models.infer_img_path)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pp_api.PPUsers')),
            ],
        ),
        migrations.CreateModel(
            name='PredictedImagePost',
            fields=[
                ('img_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pp_api.ImagePost')),
                ('materials', models.CharField(blank=True, max_length=100, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('outer_size', models.IntegerField(blank=True, null=True)),
                ('inner_size', models.IntegerField(blank=True, null=True)),
                ('item_size', models.IntegerField(blank=True, null=True)),
                ('packager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pp_api.Packager')),
            ],
        ),
    ]
