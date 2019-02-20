# Generated by Django 2.1.5 on 2019-02-20 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0011_auto_20190215_1339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('list', 'text')},
        ),
    ]
