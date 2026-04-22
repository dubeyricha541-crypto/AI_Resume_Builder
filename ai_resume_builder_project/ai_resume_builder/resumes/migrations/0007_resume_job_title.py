from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resumes", "0006_alter_resume_template"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="job_title",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
    ]
