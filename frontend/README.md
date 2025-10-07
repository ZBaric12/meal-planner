Meal Planner

Jednostavna aplikacija za planiranje obroka (tjedni prikaz, dodavanje/uređivanje/brisanje), s loginom i token autentikacijom.

Frontend: Angular

Backend: FastAPI (Python), SQLite (SQLAlchemy), JWT (python-jose)

Sadržaj

Zahtjevi

Struktura projekta

Backend — pokretanje

Frontend — pokretanje

Brzi test (smoke test)

API kratki pregled

Napomene o bazi (SQLite)

Troubleshooting (česte greške)

Zahtjevi

Python 3.11+ (radi i na 3.12)

Node.js 18+

Angular CLI npm i -g @angular/cli (preporučeno)

Struktura projekta
meal-planner/
├─ backend/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py            # FastAPI aplikacija (CORS, rute)
│  │  ├─ db.py              # SQLAlchemy engine + Session + Base
│  │  ├─ models.py          # SQLAlchemy modeli
│  │  ├─ schemas.py         # Pydantic modeli (request/response)
│  │  ├─ auth.py            # JWT, hash lozinki, dependency-ji
│  │  └─ app.db             # (može postojati) SQLite baza
│  ├─ requirements.txt
│  └─ .env                  # SECRET_KEY=...
└─ frontend/
   ├─ src/
   │  ├─ app/...
   │  └─ environments/
   │     └─ environment.ts
   ├─ package.json
   └─ angular.json


Napomena: Lokacija baze je uz app/db.py — tipično backend/app/app.db. Ako je već postoji u korijenu backend/app.db, svejedno će raditi (ovisno o postavci u db.py).

Backend — pokretanje

U PowerShellu (Windows):

cd "C:\Users\Barić\Documents\meal-planner\backend"

# (1) Kreiraj i aktiviraj virtualno okruženje (lokalni venv)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# (2) Instaliraj pakete
pip install -r requirements.txt
# ako nema requirements.txt:
# pip install "fastapi>=0.111" "uvicorn[standard]" sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-multipart "pydantic" "email-validator"

# (3) .env (tajni ključ za JWT)
'SECRET_KEY=promijeni-ovaj-kljuc' | Out-File -Encoding utf8 -NoNewline .env

# (4) Pokreni API na http://localhost:8000
uvicorn app.main:app --reload --port 8000


FastAPI docs: http://localhost:8000/docs
Health-check: http://localhost:8000/healthz

Tablice se kreiraju automatski: u main.py postoji Base.metadata.create_all(bind=engine) koji će napraviti tablice ako ne postoje.

Frontend — pokretanje
cd "C:\Users\Barić\Documents\meal-planner\frontend"

# (1) Instalacija paketa
npm i

# (2) environment.ts (ako nedostaje, napravi datoteku)
# frontend/src/environments/environment.ts
# sadrži:
# export const environment = { production: false, apiUrl: 'http://localhost:8000' };

# (3) Pokreni Angular dev server
ng serve --open


Aplikacija se otvara na http://localhost:4200.

Brzi test (smoke test)

Otvori http://localhost:4200.

Registriraj novi korisnički račun (email + lozinka).

Prijavi se — token se sprema u localStorage.

U Dashboardu:

Filtriraj raspon datuma “Od/Do”.

Dodaj novi obrok (datum, naziv, kcal).

Uredi ili obriši postojeći.

U incognito prozoru bez tokena — pokušaj otvoriti dashboard → treba te preusmjeriti na login.

API kratki pregled

POST /auth/register — JSON: { "email": "a@b.com", "password": "lozinka" }
Vraća {"message": "OK"} ili grešku (npr. korisnik postoji).

POST /auth/login — form-data (OAuth2): username, password
Vraća { "access_token": "...", "token_type": "bearer" }.

GET /me — vrati podatke o trenutnom korisniku (treba Authorization: Bearer <token>).

GET /meals?from_=&to= — lista obroka u rasponu (autorizirano).

POST /meals — JSON: { "date": "...", "title": "...", "calories": 123 }
date prihvaća YYYY-MM-DD ili dd.mm.yyyy..

PUT /meals/{id} — ažuriranje postojećeg.

DELETE /meals/{id} — brisanje.

Sve rute su dokumentirane na http://localhost:8000/docs.