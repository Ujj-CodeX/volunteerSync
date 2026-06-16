# VolunteerSync 🤝

A volunteer coordination and management system built for **NayePankh Foundation** — enabling admins to raise volunteering requests and notify volunteers based on region, while volunteers can respond to requests in real time.

---

## 🚀 Features

### Admin
- Raise volunteering requests with title, description, region, area, and deadline
- Auto-notify matching volunteers via **Email + In-app notifications**
- View dashboard with total requests raised and total acceptances
- Print accepted volunteer list for any request
- Search volunteers and view detailed profiles

### Volunteer
- Receive real-time in-app and email notifications for new requests
- Accept or mark unavailability for each request
- Personal dashboard showing participation stats

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** Django Templates, Bootstrap 5
- **Database:** SQLite
- **Email:** Gmail SMTP
- **Auth:** Django RBAC (Admin / Volunteer roles)

---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/volunteerSync.git
cd volunteerSync

# 2. Install dependencies
pip install django

# 3. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Set admin role in shell
python manage.py shell
>>> from core.models import User
>>> u = User.objects.get(username='your_username')
>>> u.role = 'admin'
>>> u.save()
>>> exit()

# 6. Run server
python manage.py runserver
```

## 🔧 Email Setup

In `settings.py`:
```python
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

Generate Gmail App Password from: Google Account → Security → 2FA → App Passwords






## 👨‍💻 Built By

**Ujjawal Rauniyar**  
Python Backend Developer  
Submission for NayePankh Foundation — Python Development Internship