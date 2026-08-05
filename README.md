# CafeCore

A full-featured **cafe & restaurant management system** built with **Django 5**.

Includes menu, cart, orders, table reservations, reviews, favorites, and a complete admin dashboard.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

### Customer side
- Register / login / profile / password reset
- Product menu, categories, and search
- Session-based cart with coupon codes
- Order placement with simulated payment flow
- Table reservation with Jalali (Persian) calendar
- Reviews & ratings (admin approval required)
- Favorites list

### Admin dashboard (staff)
- Stats overview and Chart.js charts
- Manage orders, products, categories, and inventory
- Approve / reject reviews and reservations
- Coupon CRUD
- User management

## Tech stack

- Django 5.2
- SQLite or PostgreSQL
- jdatetime + jalali-datepicker
- Chart.js, Bootstrap Icons, Vazirmatn font

## Setup

```bash
git clone https://github.com/pedimmdi/cafecore.git
cd cafecore

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and set a SECRET_KEY

cd core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Site: http://127.0.0.1:8000
Dashboard: http://127.0.0.1:8000/dashboard/ (staff user)
Django Admin: http://127.0.0.1:8000/admin/


PostgreSQL (optional)
In .env:
DB_ENGINE=postgres
DB_NAME=cafecore
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

Then run migrate again.
Default is SQLite (DB_ENGINE=sqlite) so the project runs without PostgreSQL.


Tests
cd core
python manage.py test


Project structure
cafecore/
├── core/
│   ├── accounts/        # Auth & user profile
│   ├── menu/            # Products & categories
│   ├── orders/          # Cart & orders
│   ├── payments/        # Simulated payments
│   ├── reservations/    # Table reservations
│   ├── reviews/         # Product reviews
│   ├── favorites/       # Favorites
│   ├── dashboard/       # Staff dashboard
│   ├── pages/           # Home, about, contact
│   ├── siteconfig/      # Site settings
│   ├── static/
│   └── templates/
├── docs/
│   └── screenshots/     # Optional UI screenshots
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md


Screenshots
<image-card alt="Home" src="docs/screenshots/home.png" ></image-card>
<image-card alt="Menu" src="docs/screenshots/menu.png" ></image-card>
<image-card alt="Dashboard" src="docs/screenshots/dashboard.png" ></image-card>


License
This project is licensed under the MIT License — see the LICENSE file for details.
