# Generated by Django 3.1.3 on 2020-12-22 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopicModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topicname', models.CharField(max_length=100)),
                ('author_created', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'ordering': ['topicname'],
            },
        ),
        migrations.CreateModel(
            name='IdeaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.TextField()),
                ('member_name', models.CharField(blank=True, max_length=200, null=True)),
                ('topicname_idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic', to='brainstrom.topicmodel')),
            ],
            options={
                'ordering': ['idea'],
            },
        ),
    ]
