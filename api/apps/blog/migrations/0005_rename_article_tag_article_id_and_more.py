# Generated by Django 4.2 on 2023-04-16 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_tag_article_alter_tag_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='article',
            new_name='article_id',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='category',
            new_name='category_id',
        ),
    ]
