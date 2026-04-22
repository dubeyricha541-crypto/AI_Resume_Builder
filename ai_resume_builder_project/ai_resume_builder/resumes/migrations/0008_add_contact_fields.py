# Generated migration to add LinkedIn and other contact fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0007_resume_job_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='linkedin',
            field=models.URLField(blank=True, default='', help_text='LinkedIn profile URL'),
        ),
        migrations.AddField(
            model_name='resume',
            name='portfolio',
            field=models.URLField(blank=True, default='', help_text='Personal portfolio website'),
        ),
        migrations.AddField(
            model_name='resume',
            name='github',
            field=models.URLField(blank=True, default='', help_text='GitHub profile URL'),
        ),
        migrations.AddField(
            model_name='resume',
            name='twitter',
            field=models.URLField(blank=True, default='', help_text='Twitter/X profile URL'),
        ),
    ]
