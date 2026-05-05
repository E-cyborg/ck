# 🏨 Hotel Management System

A comprehensive web-based hotel management system that enables users to browse available hotel rooms, make bookings, and manage their reservations with ease. Built with Django, HTML, CSS, and JavaScript.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Core Features](#core-features)
- [Database Models](#database-models)
- [API Routes](#api-routes)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### User Features
- 🔐 **User Authentication**: Secure login and registration with OTP verification
- 🏠 **Room Browsing**: View all available rooms with detailed descriptions and pricing
- 📅 **Easy Booking**: Simple and intuitive booking interface with date selection
- 📱 **Room Gallery**: Photo gallery showcasing different room types with automatic image rotation
- 💬 **Guest Reviews**: Read and post comments/reviews for different room types
- 👤 **User Dashboard**: Manage personal bookings and account settings
- 📞 **Contact Support**: Get in touch with the hotel management team
- 💳 **Payment System**: Secure payment processing for room bookings

### Admin Features
- 📊 **Room Management**: Add, edit, and manage hotel rooms
- 📈 **Booking Tracking**: Monitor all bookings and reservations
- 📞 **Contact Messages**: View and respond to customer inquiries
- 🔄 **Availability Management**: Automatic room availability updates

---

## 📁 Project Structure

```
Hotel_Management/
├── Hotel_Management/          # Django project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Main URL routing
│   ├── asgi.py               # ASGI configuration
│   └── wsgi.py               # WSGI configuration
├── home/                      # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # Django forms
│   └── urls.py               # App URL routing
├── templates/                 # HTML templates
│   ├── root.html             # Base template
│   ├── home.html             # Homepage
│   ├── room.html             # Rooms listing
│   ├── booking.html          # Booking form
│   ├── det_room.html         # Room details
│   ├── pay.html              # Payment page
│   ├── login.html            # Login page
│   ├── sign.html             # Registration page
│   ├── otp.html              # OTP verification
│   ├── contact.html          # Contact form
│   ├── gallery.html          # Image gallery
│   ├── user.html             # User dashboard
│   └── 404.html              # Error page
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   ├── js/
│   │   └── script.js         # Main JavaScript
│   ├── image/                # Room images (organized by type)
│   ├── videos/               # Promotional videos
│   └── images/               # Additional images
├── manage.py                  # Django management script
├── db.sqlite3                # SQLite database
└── requirements.txt          # Python dependencies
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Backend** | Django 3.x+ |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Database** | SQLite3 |
| **Authentication** | Django Auth + OTP via Email |
| **Email Service** | Django Mail Backend |
| **Server** | Django Development Server / Gunicorn |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/E-cyborg/ck.git
cd ck/Hotel_Management
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django
# or if requirements.txt exists:
pip install -r requirements.txt
```

### Step 4: Configure Database
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to access the application.

---

## 📖 Usage

### For Users

1. **Register/Login**
   - Click "Sign Up" to create a new account
   - Verify your email with the OTP sent to your inbox
   - Or login with existing credentials

2. **Browse Rooms**
   - Visit the "Rooms" page to see all available hotels
   - Click on any room card to view detailed information
   - Check room availability calendar

3. **Make a Booking**
   - Select check-in and check-out dates
   - Choose number of rooms needed
   - Specify number of adults and children per room
   - Proceed to payment

4. **Track Bookings**
   - Access your dashboard to view booking history
   - Download booking confirmation

5. **Leave Reviews**
   - Share your experience by commenting on room types
   - Help other users make informed decisions

### For Administrators

1. **Access Admin Panel**: `http://localhost:8000/admin/`
2. **Manage Rooms**: Add/Edit/Delete room listings
3. **Track Bookings**: Monitor all reservations
4. **Manage Availability**: Update room status and availability

---

## 🗂️ Core Features Explained

### 1. **Authentication System** (`views.py`)
- OTP-based email verification for new users
- Secure login with username/email
- Session management
- User dashboard access

### 2. **Room Management** (`models.py`)
- Room types (Deluxe, Standard, Suite, etc.)
- Pricing and availability tracking
- Room capacity (adults/children)
- Image gallery per room type

### 3. **Booking System** (`main.py`, `views.py`)
- Date range selection with validation
- Room availability checking
- Guest information collection
- Automatic availability updates (daily background task)

### 4. **Background Tasks** (`main.py`)
- Automatic room status updates at midnight
- Room availability reset after checkout dates
- Uses threading for non-blocking execution

### 5. **Contact Management**
- Guest inquiry submission
- Email notifications to admin
- Inquiry tracking and response system

---

## 💾 Database Models

### User-Related Models
- **User** (Django built-in): Authentication and profile
- **User_Booked_Room_Details**: Booking records with guest information

### Room-Related Models
- **R_D** (Room Details): Room type, description, pricing, capacity
- **Rooms**: Individual room instances with availability status
- **Comment**: Guest reviews and ratings

### Support Models
- **Contact**: Customer inquiries and messages
- **temp**: Temporary data for bookings in progress

---

## 🔗 API Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Homepage |
| `/rooms/` | GET | Room listing |
| `/booking/<id>/` | GET, POST | Booking form for specific room |
| `/booking_details/<id>/` | GET | Review booking details |
| `/room_details/<id>/` | GET | Room details and reviews |
| `/contact/` | GET, POST | Contact form |
| `/login/` | GET, POST | User login |
| `/register/` | GET, POST | User registration |
| `/logout/` | GET | User logout |
| `/otp-verify/` | GET, POST | OTP verification |
| `/user-dashboard/` | GET | User profile dashboard |
| `/admin/` | GET | Admin panel |

---

## 🔄 Background Task System

The system includes an automatic room availability manager that:
- Runs daily at midnight
- Checks checkout dates against current date
- Updates room status to "available" after checkout
- Resets booking dates for reuse

```python
# Automatic task scheduling in main.py
# Ensures room availability is refreshed daily
```

---

## 📝 Image Organization

Room images should be organized as follows:
```
static/
└── image/
    ├── Deluxe/
    │   ├── 1.png
    │   ├── 2.png
    │   └── ...
    ├── Standard/
    │   ├── 1.png
    │   ├── 2.png
    │   └── ...
    └── Suite/
        ├── 1.png
        ├── 2.png
        └── ...
```

Images rotate automatically every 3 seconds on the frontend.

---

## 🎨 Frontend Components

### CSS Styling (`static/style.css`)
- Responsive design (mobile-first approach)
- Bootstrap integration for grid layout
- Custom color scheme and animations
- Notification system styling

### JavaScript (`static/script.js`)
- Dynamic image rotation for room galleries
- Form validation
- Interactive booking flow
- Notification handling

---

## 🚀 Future Enhancements

- [ ] Payment gateway integration (Razorpay/Stripe)
- [ ] Real-time availability calendar
- [ ] Email confirmations for bookings
- [ ] Invoice generation and PDF download
- [ ] Loyalty program for repeat customers
- [ ] SMS notifications
- [ ] Advanced search filters
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Analytics dashboard for admins

---

## 🐛 Known Issues

- Template tag error on line 74 of booking.html (requires debugging)
- View name 'otp-Verify' not properly mapped
- Some test data references in test files need cleanup

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or support regarding this project:
- Email: [Your Email]
- GitHub Issues: [Report Issues](https://github.com/E-cyborg/ck/issues)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- Django documentation and community
- Bootstrap framework for responsive design
- Contributors and testers

---

**Last Updated**: May 2026
**Version**: 1.0.0
**Status**: In Development

---

**Note**: This is a work in progress. Some features are still under development. Please report any issues or bugs you encounter.
