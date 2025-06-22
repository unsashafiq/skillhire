from django.urls import path
from . import views 

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('role/', views.role_selection, name='role_selection'),
    path('worker/register/', views.worker_register, name='worker_register'),

     path('support/', views.support_page, name='support_page'), 
     path('employer/', views.employer_main, name='employer_main'),
      
    path('worker/register/success/', views.worker_registration_success, name='worker-registration-success'),
    path('employer/signup/', views.employer_signup, name='employer-signup'),
   
    path('employer/login/', views.employer_login, name='employer-login'),

    path('employer/signup/success/', views.employer_signup_success, name='employer-signup-success'),
    path('employer/dashboard/', views.employer_dashboard, name='employer-dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('bookmark/<int:worker_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply-to-job'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('employer/applications/', views.employer_applications, name='employer_applications'),
    path('applications/<int:app_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('panel/dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('panel/employers/', views.admin_employer_dashboard, name='admin-employer-dashboard'),
    path('panel/workers/', views.admin_worker_dashboard, name='admin-worker-dashboard'),
    path('panel/support/', views.admin_support_inbox, name='admin-support-inbox'),
    path('admin/support/resolve/<int:message_id>/', views.mark_support_resolved, name='mark_support_resolved'),
    path('panel/employers/delete/<int:employer_id>/', views.delete_employer, name='delete_employer'),
    path('panel/employers/block-toggle/<int:employer_id>/', views.toggle_block_employer, name='toggle_block_employer'),
    path('panel/employers/<int:employer_id>/jobs/', views.view_employer_jobs, name='view_employer_jobs'),
    path('panel/employers/<int:employer_id>/bookmarks/', views.view_employer_bookmarks, name='view_employer_bookmarks'),
    path('panel/workers/delete/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    path('workers/', views.worker_list, name='worker_list'),
    path('panel/workers/edit/<int:worker_id>/', views.edit_worker, name='edit_worker'),
    path('panel/workers/block-toggle/<int:worker_id>/', views.toggle_block_worker, name='toggle_block_worker'),


]
