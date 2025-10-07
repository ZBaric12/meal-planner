# Meal Planner

Jednostavna full‑stack aplikacija za planiranje obroka.  
Frontend: **Angular** (standalone komponente, token interceptor)  
Backend: **FastAPI** (JWT, SQLAlchemy, SQLite)

---

## Sadržaj
- [Značajke](#značajke)
- [Preduvjeti](#preduvjeti)
- [Struktura projekta](#struktura-projekta)
- [Pokretanje — brzo](#pokretanje--brzo)
- [Backend (FastAPI)](#backend-fastapi)
- [Frontend (Angular)](#frontend-angular)
- [Konfiguracija](#konfiguracija)
- [API sažetak](#api-sažetak)
- [Česta pitanja / problemi](#česta-pitanja--problemi)
- [Licenca](#licenca)

---

## Značajke
- Registracija i prijava (JWT Bearer token)
- CRUD nad obrocima (datum, naziv, kalorije)
- Filtriranje obroka po rasponu datuma
- SQLite baza (`app.db`), tablice se kreiraju automatski
- Token interceptor i guard za rute

---

## Preduvjeti
- **Python 3.11+** (preporuka 3.12)
- **Node.js 18+** i **npm**
- **Angular CLI** (16+)
- **Git**

---

## Struktura projekta
```
meal-planner/
├─ backend/
│  ├─ app/
│  │  ├─ main.py         # FastAPI aplikacija i rute
│  │  ├─ db.py           # SQLAlchemy engine, Session i Base
│  │  ├─ models.py       # SQLAlchemy modeli (User, Meal)
│  │  ├─ schemas.py      # Pydantic sheme (request/response)
│  │  ├─ auth.py         # JWT, hash lozinki, dependency-i
│  ├─ app.db             # SQLite baza (kreira se automatski)
│  └─ requirements.txt   # Python ovisnosti
└─ frontend/
   ├─ src/app/
   │  ├─ auth/           # Auth service + interceptor
   │  ├─ pages/
   │  │  ├─ login/       # Login/registracija (standalone)
   │  │  └─ dashboard/   # Lista + forma za obroke (standalone)
   │  └─ app-routing.module.ts
   └─ src/environments/environment.ts
```

---

## Pokretanje — brzo

### 1) Backend
**Windows (PowerShell)**
```powershell
cd backend
py -3 -m venv C:\venvs\mealplanner-backend
C:\venvs\mealplanner-backend\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**macOS/Linux**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend (dev server, bez SSR-a)
```bash
cd frontend
npm i
ng serve --open
# otvara http://localhost:4200
```

---

## Backend (FastAPI)
- Pokreće se na: `http://127.0.0.1:8000`
- CORS dopušta `http://localhost:4200`
- Baza: `backend/app.db` (SQLite).  
  Tablice se kreiraju automatski na startu preko:
  ```python
  # app/main.py
  Base.metadata.create_all(bind=engine)
  ```

**Reset baze:** ugasite server i obrišite `backend/app.db`.

Ako nedostaje validator za email:
```bash
pip install "pydantic[email]"
```

---

## Frontend (Angular)
- Pokreće se na: `http://localhost:4200`
- **Važno:** koristite `ng serve` (dev server).  
  Nemojte pokretati SSR (`dev:ssr`).

**Token interceptor** automatski dodaje header:
```
Authorization: Bearer <token>
```

---

## Konfiguracija

### Frontend `environment.ts`
`frontend/src/environments/environment.ts`
```ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000',
};
```

### Login format (FastAPI OAuth2)
Backend očekuje **`application/x-www-form-urlencoded`** s poljima:
- `username` — email
- `password` — lozinka

Frontend to šalje preko `AuthService.login(...)`.

---

## API sažetak

### Health
- `GET /healthz` → `{ "ok": true }`

### Autentikacija
- `POST /auth/register`
  ```json
  { "email": "user@example.com", "password": "tajna" }
  ```
  **Odgovor:** 201 Created

- `POST /auth/login`  
  Body: `username=<email>&password=<lozinka>`  
  **Odgovor:**
  ```json
  { "access_token": "...", "token_type": "bearer" }
  ```

- `GET /me` → korisnički profil (zahtijeva Bearer token)

### Meals
- `GET /meals?from_=YYYY-MM-DD&to=YYYY-MM-DD` → lista obroka
- `POST /meals`
  ```json
  { "date": "2025-10-07", "title": "Juha", "calories": 250 }
  ```
- `GET /meals/{id}` → detalji
- `PUT /meals/{id}` → djelomična izmjena (pošaljite samo polja koja mijenjate)
  ```json
  { "calories": 350 }
  ```
- `DELETE /meals/{id}` → 204 No Content

> Napomena: Backend kod izmjene koristi **`exclude_unset` + `exclude_none`**, pa nije potrebno slati sva polja.

---

## Licenca
MIT — slobodno koristite u edukativne svrhe.
