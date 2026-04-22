from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0004_resume_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='resume_photos/'),
        ),
    ]
