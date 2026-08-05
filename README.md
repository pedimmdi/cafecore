# CafeCore

A full-featured **cafe & restaurant management system** built with **Django 5**.

Includes menu, cart, orders, table reservations, reviews, favorites, and a complete staff dashboard with charts and CRUD for day-to-day cafe operations.

The UI is built with **custom HTML, CSS, and JavaScript** (no Bootstrap/Tailwind layout framework) — Bootstrap Icons and the Vazirmatn font are used for icons and typography only.

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

- **Backend:** Django 5.2, SQLite or PostgreSQL
- **Frontend:** Custom HTML / CSS / JS, Bootstrap Icons, Vazirmatn
- **Persian dates:** jdatetime + jalali-datepicker
- **Charts:** Chart.js

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
# Keep a copy of .env in this folder (python-decouple reads it from the working directory)
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

- Site: http://127.0.0.1:8000
- Dashboard: http://127.0.0.1:8000/dashboard/ (staff user)
- Django Admin: http://127.0.0.1:8000/admin/

### Demo data

```bash
cd core
python manage.py seed_demo
```

This command creates:

- Sample categories and products
- Demo coupon code `DEMO10` (10% off)
- A superuser if one does not already exist:
  - Email: `admin@cafecore.local`
  - Password: `Admin123!`

Safe to run more than once (`get_or_create` — it will not duplicate the same records).

> Change the demo password after first login if you use this beyond local testing.

### PostgreSQL (optional)

In `.env`:

```env
DB_ENGINE=postgres
DB_NAME=cafecore
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

Then run `migrate` again.

Default is SQLite (`DB_ENGINE=sqlite`) so the project runs without PostgreSQL.

## Tests

```bash
cd core
python manage.py test
```

## Project structure

```text
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
│   ├── pages/           # Home, about, contact (+ seed_demo)
│   ├── siteconfig/      # Site settings
│   ├── static/          # Custom CSS & JS
│   └── templates/       # Custom HTML templates
├── docs/
│   └── screenshots/
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

## Screenshots

![Home](docs/screenshots/home.png)

![Menu](docs/screenshots/menu.png)

![Dashboard](docs/screenshots/dashboard.png)

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
