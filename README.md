# 🛒 Olcha API

Bu loyiha Django REST Framework asosida yozilgan e-commerce backend API hisoblanadi. Loyihada `Category`, `SubCategory`, `Product`, `Comment` modellariga oid CRUD imkoniyatlar mavjud. Shuningdek, foydalanuvchi autentifikatsiyasi JWT orqali amalga oshiriladi.

---

## 🚀 Demo (deploy qilingan API)
**Base URL:**  
https://api-olchaaa.onrender.com/

---

## ⚙️ Texnologiyalar

- Python 3.11+
- Django 5.x
- Django REST Framework
- PostgreSQL (Render)
- Simple JWT
- drf-spectacular (Swagger uchun)
- Gunicorn (production server)

---

## 🔐 JWT Authentication

### Token olish:
```http
POST /token/
