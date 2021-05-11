# Generated by Django 3.1.4 on 2021-03-08 16:21

from django.db import migrations, models
import django.db.models.deletion
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20210103_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='post.category'),
        ),
        migrations.AlterField(
            model_name='adminpost',
            name='category',
            field=models.ManyToManyField(related_name='articles', to='post.Category'),
        ),
        migrations.AlterField(
            model_name='adminpost',
            name='description',
            field=models.TextField(verbose_name=post.models.Category),
        ),
    ]
