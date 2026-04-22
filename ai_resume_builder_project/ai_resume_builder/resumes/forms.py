from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ['user', 'template', 'slug', 'ats_score', 'created_at']
        widgets = {
            'full_name':        forms.TextInput(attrs={'class': 'form-control'}),
            'job_title':        forms.TextInput(attrs={'class': 'form-control'}),
            'email':            forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':            forms.TextInput(attrs={'class': 'form-control'}),
            'address':          forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'linkedin':         forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'portfolio':        forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourportfolio.com'}),
            'github':           forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'twitter':          forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/...'}),
            'career_objective': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'education':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills':           forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'certifications':   forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'experience':       forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'projects':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'achievements':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'languages':        forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'job_description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            # slug removed — it's excluded from the form, no widget needed
        }
