# Instagram Clone

A full-featured Instagram Clone built with Django, featuring user authentication, posts, likes, comments, stories, direct messaging, reels, and more.

## Features

- **Authentication**: Register, login, logout, password reset via email
- **User Profiles**: Edit profile, upload photo, bio, website, followers/following
- **Posts**: Create, edit, delete posts with images and captions
- **Feed**: Infinite-scroll home feed showing posts from followed users
- **Likes & Comments**: Like/unlike posts, add and delete comments
- **Search**: Search users by username
- **Notifications**: Real-time notifications for follows, likes, and comments
- **Saved Posts**: Bookmark posts for later
- **Stories**: 24-hour expiring stories with images
- **Direct Messaging**: One-on-one conversations
- **Reels**: Upload and browse short video reels
- **Explore**: Discover new content
- **Responsive UI**: Bootstrap 5, mobile-friendly Instagram-like design

## Tech Stack

- **Backend**: Python 3.x, Django 4.2
- **Database**: SQLite (dev), PostgreSQL (production)
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Image Handling**: Pillow
- **Deployment**: PythonAnywhere, Render

## Project Structure

```
instagram-clone/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── instagram_clone/         # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                   # User accounts & profiles
│   ├── models.py            # Profile, Follow
│   ├── views.py             # Auth, profile, search
│   ├── forms.py             # Registration, profile update
│   ├── signals.py           # Auto-create profile
│   ├── urls.py
│   ├── admin.py
│   └── templates/users/
├── posts/                   # Posts, likes, comments
│   ├── models.py            # Post, Like, Comment, SavedPost
│   ├── views.py             # Feed, create, detail, explore
│   ├── forms.py             # PostForm, CommentForm
│   ├── urls.py
│   ├── admin.py
│   └── templates/posts/
├── notifications/           # Notifications system
│   ├── models.py            # Notification
│   ├── views.py
│   ├── urls.py
│   └── templates/notifications/
├── messaging/               # Direct messaging
│   ├── models.py            # Conversation, Message
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/messaging/
├── stories/                 # 24h stories
│   ├── models.py            # Story
│   ├── views.py
│   ├── urls.py
│   └── templates/stories/
├── reels/                   # Short video reels
│   ├── models.py            # Reel, ReelLike, ReelComment
│   ├── views.py
│   ├── urls.py
│   └── templates/reels/
├── templates/               # Base templates
│   ├── base.html
│   └── navbar.html
├── static/                  # Static assets
│   ├── css/style.css
│   └── js/main.js
└── media/                   # User uploads (gitignored)
    ├── profile_pics/
    ├── post_pics/
    ├── story_pics/
    └── reels/
```

## Quick Start

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/instagram-clone.git
cd instagram-clone

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py makemigrations users posts notifications messaging stories reels
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

### Run Tests

```bash
python manage.py test
```

## Deployment

### PythonAnywhere

1. Upload project to PythonAnywhere
2. Create virtual environment and install requirements
3. Set up Web app with WSGI configuration
4. Configure static/media files
5. Update `ALLOWED_HOSTS` and `SECRET_KEY` in `.env`

### Render

1. Push to GitHub
2. Create new Web Service on Render
3. Set build command: `pip install -r requirements.txt && python manage.py migrate`
4. Set start command: `gunicorn instagram_clone.wsgi`
5. Add environment variables from `.env.example`

## Screenshots

<!-- Add your screenshots here -->
| Feature | Screenshot |
|---------|-----------|
| Login | ![Login](screenshots/login.png) |
| Feed | ![Feed](screenshots/feed.png) |
| Profile | ![Profile](screenshots/profile.png) |
| Stories | ![Stories](screenshots/stories.png) |
| Messages | ![Messages](screenshots/messages.png) |

## License

MIT
