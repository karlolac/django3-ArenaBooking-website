# ArenaBooking 🏟️

Web aplikacija za pregled sportskih dvorana i rezervaciju terena.  
Razvijeno u Django frameworku.

---

# Funkcionalnosti

## 👤 Obični korisnik
- Pregled dvorana i terena
- Rezervacija termina
- Otkazivanje vlastitih rezervacija
- Pregled aktivnih i prošlih rezervacija

## 🛡️ Moderator
- Pristup upravljačkoj ploči
- Odobravanje / odbijanje rezervacija

## 🔧 Admin (staff)
- Upravljanje korisnicima i grupama
- Može dodavati dvorane i terene
- Pregled aplikacije
- Može ući u formu rezervacije
- Ne može napraviti rezervaciju

---

# Test korisnici

| Uloga      | Username   | Lozinka         |
|------------|------------|-----------------|
| User       | marko      | Arenabooking1   |
| Moderator  | moderator2 | Arenabooking2   |
| Moderator  | moderator  | moderator       |
| Admin      | admin      | admin           |

---

# Instalacija (lokalno)

## 1️⃣ Kloniranje repozitorija

```bash
git clone https://gitlab.com/karlolac/django3-arenabooking-website.git
cd ArenaBooking

2️⃣ Virtual environment

python -m venv .venv
.venv\Scripts\activate

3️⃣ Instalacija ovisnosti

pip install django

4️⃣ Migracije baze

python manage.py makemigrations
python manage.py migrate

5️⃣ Kreiranje superusera (ako treba)

python manage.py createsuperuser

6️⃣ Pokretanje servera

python manage.py runserver

Aplikacija radi na:

http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/



Inicijalni push

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://gitlab.com/karlolac/django3-arenabooking-website.git
git push -u origin main


Autor

Karlo Lacković
Projekt za kolegij Programskog Inženjerstva