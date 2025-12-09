# Django ATHM Demo

Example Django web app demonstrating [django-athm](https://github.com/django-athm/django-athm) integration for ATH Movil payments. Check it out live: [django-athm.dev](https://django-athm.dev).

For the full package documentation and feature list, see [django-athm](https://github.com/django-athm/django-athm).

## Feature Highlight

This demo showcases key features from django-athm. Here's where to find them:

### 1. Django Signals - `athm_tip/core/signals.py`
Comprehensive signal handlers demonstrating production patterns:
- **Rich logging**: All 4 signals (`payment_completed`, `payment_cancelled`, `payment_expired`, `refund_sent`) log sanitized payment data showing available fields
- **Admin notifications**: Emails sent to ADMINS on payment completion (console in dev, SES in prod)
- **PII safety**: Customer data sanitized in logs, full details only in admin emails
- **Duration tracking**: Cancelled/expired payments log time elapsed
- **Webhook data**: Completed payments show fees and net amounts from ATH Movil webhooks

### 2. Template Tag Integration - `templates/partials/athm_button.html`
Quick-start payment button using the bundled `{% athm_button %}` template tag with zero-dependency JavaScript.

### 3. Payment Success Flow - `athm_tip/core/views.py`
- **tip_page** (line 10): Configures payment with items, success/failure URLs, and metadata
- **thank_you** (line 51): Displays webhook-enriched payment data (fees, net amounts, customer info)

### 4. Webhook Event Display - `templates/thank_you.html:136-182`
Shows webhook events with idempotency tracking, demonstrating automatic deduplication and event history.

### 5. Webhook-Enriched Data - `templates/thank_you.html:93-108`
Displays transaction fees and net amounts that come from ATH Movil webhooks, not available in the initial payment response.

## Project Structure

```
demo/
├── athm_tip/
│   ├── core/
│   │   ├── signals.py     # Signal handlers for payment events
│   │   ├── views.py       # Payment and success views
│   │   └── urls.py        # URL routing
│   └── theme/             # Tailwind CSS theme app
├── config/
│   ├── settings/          # Django settings (base, production)
│   └── urls.py
├── templates/
│   ├── tip.html           # Payment page with athm_button
│   ├── thank_you.html     # Success page with webhook data
│   └── partials/          # Reusable template fragments
└── static/                # Static assets (images, animations)
```

**Stack:**
- [Django](https://djangoproject.com) 5.2
- [django-tailwind](https://django-tailwind.readthedocs.io) with [DaisyUI](https://daisyui.com) components
- [django-athm](https://github.com/django-athm/django-athm) for ATH Movil payments

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- ATH Movil Business account with API credentials

## Setup

1. Clone and install dependencies:

```bash
git clone https://github.com/django-athm/demo.git
cd demo
uv sync
```

2. Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your values:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key |
| `ATHM_PUBLIC_TOKEN` | Yes | ATH Movil public API token |
| `ATHM_PRIVATE_TOKEN` | Yes | ATH Movil private API token |
| `DEBUG` | No | Enable debug mode (default: false) |
| `ALLOWED_HOSTS` | No | Comma-separated hosts (default: localhost,127.0.0.1) |

3. Run migrations and start the server:

```bash
uv run python manage.py migrate
uv run python manage.py tailwind dev
```

4. Visit http://127.0.0.1:8000/
