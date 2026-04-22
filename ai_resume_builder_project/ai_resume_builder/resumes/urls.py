from django.urls import path
from .docx_export import download_resume_docx_unified

from .views import (
    create_resume,
    ResumeListView, ResumeUpdateView, ResumeDeleteView, ResumeDetailView,
    download_resume_pdf, ats_analyzer, portfolio_view,
    dashboard, ai_suggestions, public_portfolio,
    ats_score_api,
    delete_resume_ajax,
    upload_resume_ats,
)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', create_resume, name='create_resume'),
    path('my/', ResumeListView.as_view(), name='my_resumes'),
    path('edit/<int:pk>/', ResumeUpdateView.as_view(), name='edit_resume'),
    path('delete/<int:pk>/', ResumeDeleteView.as_view(), name='delete_resume'),
    path('delete/<int:pk>/ajax/', delete_resume_ajax, name='delete_resume_ajax'),
    path('view/<int:pk>/', ResumeDetailView.as_view(), name='view_resume'),
    path('download/<int:pk>/', download_resume_pdf, name='download_resume_pdf'),
    path('download-docx/<int:pk>/', download_resume_docx_unified, name='download_resume_docx'),
    path('ats/<int:pk>/', ats_analyzer, name='ats_analyzer'),
    path('ats-score/', ats_score_api, name='ats_score_api'),
    path('check-upload/', upload_resume_ats, name='upload_resume_ats'),
    path('portfolio/<int:pk>/', portfolio_view, name='portfolio'),
    path('ai/<int:pk>/', ai_suggestions, name='ai_suggestions'),
    path('public/<slug:slug>/', public_portfolio, name='public_portfolio'),
]
