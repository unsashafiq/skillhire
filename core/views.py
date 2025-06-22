import re
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .forms import JobApplicationForm, WorkerForm, WorkerRegistrationForm
from django.contrib import messages
from .forms import ProblemReportForm
from .forms import EmployerSignupForm
from django.contrib.auth import authenticate, login
from .models import Application, Employer, JobPost, Worker, Bookmark
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import ApplicationForm
from .models import JobPost
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import SupportMessage



def normalize_phone(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Convert '03xxxxxxxxx' to '923xxxxxxxxx'
    if digits.startswith('03'):
        digits = '92' + digits[1:]

    return digits


def welcome(request):
    return render(request, 'core/welcome.html')

def role_selection(request):
    return render(request, 'core/role_selection.html')
def worker_register(request):
     return render(request, 'core/worker_register.html')
def support_page(request):
    if request.method == 'POST':
        form = ProblemReportForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/support_success.html')
        else:
            print("Form is invalid ❌")
            print(form.errors)  # 👈 Add this to debug
    else:
        form = ProblemReportForm()

    return render(request, 'core/support.html', {'form': form})

def employer_main(request):
    return render(request, 'core/employer_main.html') 

def worker_register(request):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)

            # Normalize phone number before saving
            original_phone = form.cleaned_data['phone']
            worker.phone = normalize_phone(original_phone)

            worker.save()

            # Save worker ID in session
            request.session['worker_id'] = worker.id

            return redirect('worker-registration-success')
        else:
            print("Form errors:", form.errors)
    else:
        form = WorkerRegistrationForm()

    return render(request, 'core/worker_register.html', {'form': form})


def worker_registration_success(request):
    return render(request, 'core/worker_registration_success.html')

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.set_password(form.cleaned_data['password'])
            employer.save()
            return redirect('employer-signup-success')
        else:
            print(form.errors)  # Add this to debug
    else:
        form = EmployerSignupForm()

    return render(request, 'core/employer_signup.html', {'form': form})

def employer_login(request):
    if request.method == 'POST':
        print("✅ Form submitted")

        email = request.POST.get('email') or  request.POST.get('username') # Still called 'username' due to form name
        password = request.POST.get('password')


        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            print("✅ Login successful")
            return redirect('employer-dashboard') # Temporary
        else:
            print("❌ Login failed")
            messages.error(request, "Invalid credentials.")

    return render(request, 'core/employer_login.html')


def employer_signup_success(request):
    return render(request, 'core/employer_signup_success.html')
def employer_dashboard(request):
    search_query = request.GET.get('search', '')

    if search_query:
        workers = Worker.objects.filter(skill__icontains=search_query)
    else:
        workers = Worker.objects.all()
    return render(request, 'core/employer_dashboard.html', {'workers': workers})
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.employer = request.user  # assign the logged-in user
            job_post.save()
            return render(request, 'core/post_job.html', {
                'success': True
            })
    else:
        form = JobPostForm()
    return render(request, 'core/post_job.html', {'form': form})



@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    worker = get_object_or_404(Worker, user=request.user)

    if Application.objects.filter(job=job, worker=worker).exists():
        return render(request, 'core/application_exists.html')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.worker = worker
            application.save()
            return render(request, 'core/application_success.html')
    else:
        form = ApplicationForm()

    return render(request, 'core/apply_to_job.html', {'form': form, 'job': job})
def job_list(request):
    jobs = JobPost.objects.all().order_by('-created_at')  # Show latest first
    return render(request, 'core/job_list.html', {'jobs': jobs})
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    worker = None

    # Check if user is a registered worker via session
    worker_id = request.session.get('worker_id')
    if worker_id:
        try:
            worker = Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist:
            worker = None

    form = JobApplicationForm()

    print("Worker ID in session:", request.session.get('worker_id'))
    print("Resolved worker object:", worker)

    return render(request, 'core/job_detail.html', {
        'job': job,
        'worker': worker,
        'form': form
    })

def apply_to_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    # Get worker from session
    worker_id = request.session.get('worker_id')
    if not worker_id:
        messages.error(request, "You must be registered as a worker to apply.")
        return redirect('worker_register')

    try:
        worker = Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        messages.error(request, "Registered worker not found. Please register again.")
        return redirect('worker_register')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            # ✅ No more phone processing needed here
            if Application.objects.filter(job=job, worker=worker).exists():
                 return render(request, 'core/already_applied.html')

            else:
                Application.objects.create(
                    job=job,
                    worker=worker,
                    message=form.cleaned_data['message']
                )
                messages.success(request, "Application submitted successfully!")
                return render(request, 'core/application_success.html')
    else:
        form = JobApplicationForm()

    return render(request, 'core/job_detail.html', {
        'job': job,
        'form': form,
        'worker': worker
    })
@login_required
def employer_applications(request):
    employer = request.user  # The logged-in employer

    # Get all job posts created by this employer
    jobs = JobPost.objects.filter(employer=employer)

    # Get all applications to those job posts
    applications = Application.objects.filter(job__in=jobs).select_related('job', 'worker')

    return render(request, 'core/employer_applications.html', {
        'applications': applications,
    })
@csrf_exempt
def toggle_bookmark(request, app_id):
    if request.method == 'POST':
        try:
            app = Application.objects.get(id=app_id)
            app.bookmarked = not app.bookmarked
            app.save()
            return JsonResponse({'bookmarked': app.bookmarked})
        except Application.DoesNotExist:
            return JsonResponse({'error': 'Application not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def admin_dashboard(request):
    employers = Employer.objects.all()
    workers = Worker.objects.all()
    support_messages = SupportMessage.objects.filter(resolved=False)
    latest_support = support_messages.order_by('-created_at').first()

    return render(request, 'admin_panel/dashboard.html', {
        'employer_count': employers.count(),
        'worker_count': workers.count(),
        'support_count': support_messages.count(),
        'latest_support': latest_support
    })
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def admin_employer_dashboard(request):
    employers = Employer.objects.all()
    return render(request, 'admin_panel/employers.html', {'employers': employers})


@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def admin_worker_dashboard(request):
    workers = Worker.objects.all()
    return render(request, 'admin_panel/workers.html', {'workers': workers})


@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def admin_support_inbox(request):
    unresolved_messages = SupportMessage.objects.filter(resolved=False).order_by('-created_at')
    resolved_messages = SupportMessage.objects.filter(resolved=True).order_by('-created_at')[:5]  # Optional: recent resolved
    return render(request, 'admin_panel/support_inbox.html', {
        'unresolved_messages': unresolved_messages,
        'resolved_messages': resolved_messages
    })
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def mark_support_resolved(request, message_id):
    message = get_object_or_404(SupportMessage, id=message_id)
    message.resolved = True
    message.save()
    return redirect('admin-support-inbox')
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def delete_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    employer.delete()
    messages.success(request, 'Employer deleted successfully.')
    return redirect('admin-employer-dashboard')

# Block/Unblock Employer
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def toggle_block_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    employer.is_blocked = not employer.is_blocked
    employer.save()
    action = 'unblocked' if not employer.is_blocked else 'blocked'
    messages.success(request, f'Employer has been {action}.')
    return redirect('admin-employer-dashboard')

# View Employer Jobs
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def view_employer_jobs(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    jobs = JobPost.objects.filter(employer=employer)
    return render(request, 'admin_panel/employer_jobs.html', {'employer': employer, 'jobs': jobs})

# View Employer Bookmarks
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def view_employer_bookmarks(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    bookmarks = Bookmark.objects.filter(employer=employer).select_related('worker')
    return render(request, 'admin_panel/employer_bookmarks.html', {
        'employer': employer,
        'bookmarks': bookmarks
    })
@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def delete_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    worker.delete()
    messages.success(request, 'Worker deleted successfully.')
    return redirect('admin-worker-dashboard')

@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def toggle_block_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    worker.is_blocked = not worker.is_blocked
    worker.save()
    status = 'unblocked' if not worker.is_blocked else 'blocked'
    messages.success(request, f'Worker has been {status}.')
    return redirect('admin-worker-dashboard')

@login_required
@user_passes_test(lambda u: hasattr(u, 'is_admin') and u.is_admin)
def edit_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Worker updated successfully.')
            return redirect('admin-worker-dashboard')
    else:
        form = WorkerForm(instance=worker)
    return render(request, 'admin_panel/edit_worker.html', {'form': form})
def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'admin_panel/worker_list.html', {'workers': workers})