# Claude Code - Project Guide

## Running the Project

This project uses `uv` for Python package management and Django Tailwind for styling.

### Run Migrations

```bash
uv run python manage.py migrate
```

### Run Development Server

The project requires running Django with Tailwind in development mode on port 8002:

```bash
uv run python manage.py tailwind start
```

In a separate terminal:

```bash
uv run python manage.py runserver 8002
```

**Access the application:**
- Main site: http://127.0.0.1:8002/
- Tip showcase page: http://127.0.0.1:8002/tip/
- Admin: http://127.0.0.1:8002/admin/

### Environment Variables

Make sure to copy `.env.example` to `.env` and set:
- `SECRET_KEY` - Django secret key
- `ATHM_PUBLIC_KEY` - ATH Móvil public API key
- `ATHM_PRIVATE_KEY` - ATH Móvil private API key

## Project Structure

- `athm_tip/core/` - Main application logic
- `athm_tip/theme/` - Tailwind/DaisyUI theme configuration
- `templates/` - Django templates
- `config/` - Django settings and URL configuration
