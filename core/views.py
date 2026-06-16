from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import User, VolunteerRequest, RequestResponse, Notification

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False)
    if user.role == 'admin':
        raised = VolunteerRequest.objects.filter(raised_by=user).order_by('-created_at')
        total_raised = raised.count()
        total_accepted = RequestResponse.objects.filter(
            request__in=raised, status='accepted'
        ).count()
        return render(request, 'admin_dashboard.html', {
            'raised': raised,
            'total_raised': total_raised,
            'total_accepted': total_accepted,
            'notifications': notifications,
        })
    else:
        my_responses = RequestResponse.objects.filter(volunteer=user).select_related('request')
        responded_ids = my_responses.values_list('request_id', flat=True)
        pending = VolunteerRequest.objects.exclude(id__in=responded_ids).order_by('-created_at')
        total_accepted = my_responses.filter(status='accepted').count()
        return render(request, 'volunteer_dashboard.html', {
            'my_responses': my_responses,
            'pending': pending,
            'total_accepted': total_accepted,
            'notifications': notifications,
        })

@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifs': notifs})

@login_required
def raise_request(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        region = request.POST['region']
        area = request.POST['area']
        deadline = request.POST['deadline']
        vr = VolunteerRequest.objects.create(
            title=title, description=description,
            region=region, area=area,
            deadline=deadline, raised_by=request.user
        )
        # Notify matching volunteers
        volunteers = User.objects.filter(role='volunteer', region=region)
        for v in volunteers:
            Notification.objects.create(
                user=v,
                message=f"New volunteering request in your area: {title} — Deadline: {deadline}"
            )
            try:
                send_mail(
                    subject=f"[VolunteerSync] New Request: {title}",
                    message=f"Hello {v.first_name},\n\nA new volunteering request has been raised in your region ({region}, {area}).\n\nTitle: {title}\nDescription: {description}\nDeadline: {deadline}\n\nLogin to VolunteerSync to respond.\n\nNayePankh Foundation",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[v.email],
                    fail_silently=True,
                )
            except:
                pass
        messages.success(request, f"Request raised! {volunteers.count()} volunteers notified.")
        return redirect('dashboard')
    return render(request, 'raise_request.html')

@login_required
def respond_request(request, pk):
    if request.user.role != 'volunteer':
        return redirect('dashboard')
    vr = get_object_or_404(VolunteerRequest, pk=pk)
    if request.method == 'POST':
        status = request.POST['status']
        RequestResponse.objects.update_or_create(
            volunteer=request.user, request=vr,
            defaults={'status': status}
        )
        msg = "accepted" if status == 'accepted' else "marked as unavailable"
        messages.success(request, f"You have {msg} this request.")
        return redirect('dashboard')
    return render(request, 'respond_request.html', {'vr': vr})

@login_required
def volunteer_list(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    query = request.GET.get('q', '')
    region = request.GET.get('region', '')
    volunteers = User.objects.filter(role='volunteer')
    if query:
        volunteers = volunteers.filter(username__icontains=query)
    if region:
        volunteers = volunteers.filter(region__icontains=region)
    return render(request, 'volunteer_list.html', {'volunteers': volunteers, 'query': query, 'region': region})

@login_required
def volunteer_detail(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    volunteer = get_object_or_404(User, pk=pk, role='volunteer')
    responses = RequestResponse.objects.filter(volunteer=volunteer).select_related('request')
    return render(request, 'volunteer_detail.html', {'volunteer': volunteer, 'responses': responses})