# DREAMS ✦ your own little universe

Orzularni matn va ko'p rasm bilan joylaydigan platforma (Django + PostgreSQL).

## Ishga tushirish
```bash
python -m venv venv
venv\Scripts\activate            # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env           # keyin .env ichidagi parolni to'ldiring
```
PostgreSQL'da: `CREATE DATABASE dreams_db;`  (yoki .env ga `USE_SQLITE=1` yozing)
```bash
python manage.py makemigrations core users dreams
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test            # testlar
```

## Arxitektura
```
dreams_project/settings/  base.py (umumiy) · dev.py · prod.py
core/      TimeStampedModel, validators  (hamma applar uchun umumiy)
users/     Profile (signal bilan avtomatik), register/login/profil
dreams/    Dream, DreamImage, CRUD, feed, filtrlar
```
- `manage.py` -> `settings.dev`, `wsgi/asgi` -> `settings.prod`
- Ko'rinish qoidasi bitta joyda: `Dream.objects.visible_to(user)`
- Kelgusi applar (har biri alohida): social, collections, capsules, gamification, notifications, messaging, ai

## Reja
| # | Bosqich | Holat |
|---|---|---|
| 01 | Arxitektura va database | tayyor |
| 02 | Register, Login, Profile | tayyor |
| 03 | Dreams CRUD, ko'p rasm, bosqich/private | tayyor |
| 04 | Public Feed, Pinterest dizayn | tayyor (masonry + collage) |
| 05 | Like, Comment, Follow | keyingi |
| 06 | Collections, Bookmark | |
| 07 | Dream Universe | |
| 08 | Time Capsule, Secret Space | |
| 09 | AI Assistant | |
| 10 | XP, Levels, Achievements | |
| 11 | Notifications, Messages | |
| 12 | Xavfsizlik, testlar, deployment | |
