from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Resume(models.Model):
    ATS_TEMPLATE = 'minimalist'
    TEMPLATE_CHOICES = [
        ('minimalist', 'Minimalist'),
        ('dynamic',    'Dynamic'),
        ('creative',   'Creative'),
        ('essential',  'Essential'),
        ('modest',     'Modest'),
        ('bold',       'Bold'),
    ]

    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default=ATS_TEMPLATE)

    full_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200, blank=True, default="")
    email     = models.EmailField()
    phone     = models.CharField(max_length=20)
    address   = models.TextField(blank=True)
    
    # Additional contact information
    linkedin  = models.URLField(blank=True, default="", help_text="LinkedIn profile URL")
    portfolio = models.URLField(blank=True, default="", help_text="Personal portfolio website")
    github    = models.URLField(blank=True, default="", help_text="GitHub profile URL")
    twitter   = models.URLField(blank=True, default="", help_text="Twitter/X profile URL")

    # Optional profile photo
    photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True)

    career_objective = models.TextField()
    education        = models.TextField()
    skills           = models.TextField()

    certifications = models.TextField(blank=True)
    experience     = models.TextField(blank=True)
    projects       = models.TextField(blank=True)
    achievements   = models.TextField(blank=True)
    languages      = models.TextField(blank=True)

    job_description = models.TextField(blank=True, null=True)
    ats_score       = models.IntegerField(default=0)

    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.template:
            self.template = self.ATS_TEMPLATE
        if not self.slug:
            unique_id = uuid.uuid4().hex[:6]
            self.slug = slugify(f"{self.user.username}-{unique_id}")
        super().save(*args, **kwargs)

    # ── Helpers for templates ──────────────────────────
    def edu_entries(self):
        """Parse pipe-separated education lines into dicts."""
        entries = []
        for line in (self.education or '').splitlines():
            parts = line.split('|')
            if len(parts) >= 2:
                entries.append({
                    'degree':      parts[0] if len(parts) > 0 else '',
                    'institution': parts[1] if len(parts) > 1 else '',
                    'start':       parts[2] if len(parts) > 2 else '',
                    'end':         parts[3] if len(parts) > 3 else '',
                })
        return entries

    def exp_entries(self):
        """Parse pipe-separated experience lines into dicts."""
        entries = []
        for line in (self.experience or '').splitlines():
            parts = line.split('|')
            if len(parts) >= 2:
                entries.append({
                    'title':   parts[0] if len(parts) > 0 else '',
                    'company': parts[1] if len(parts) > 1 else '',
                    'start':   parts[2] if len(parts) > 2 else '',
                    'end':     parts[3] if len(parts) > 3 else '',
                    'desc':    parts[4] if len(parts) > 4 else '',
                })
        return entries

    def skills_list(self):
        return [s.strip() for s in (self.skills or '').split(',') if s.strip()]
