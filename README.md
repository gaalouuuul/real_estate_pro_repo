# Real Estate Microservice API

API REST de gestion immobilière — Python / Flask / SQLite.

---

## Prérequis

- Python 3.10+
- pip

> Aucune installation de base de données nécessaire — SQLite est inclus avec Python.

---

## Installation et démarrage

```bash
# 1. Cloner le dépôt
git clone https://github.com/gaalouuuul/real_estate_pro_repo.git
cd real_estate_pro_repo

# 2. Créer et activer l'environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'API
python run.py
```

L'API démarre sur **http://localhost:5000**

---

## Documentation interactive (Swagger)

Ouvrez dans le navigateur :

```
http://localhost:5000/apidocs
```

Toutes les routes sont documentées et testables directement depuis l'interface Swagger.

---

## Données de démonstration

Pour peupler la base avec des données de test (utilisateurs, biens, pièces) :

```bash
python seed.py
```

Comptes créés :

| Email | Mot de passe | Rôle |
|---|---|---|
| admin@example.com | admin123 | admin |
| owner@example.com | owner123 | owner |
| viewer@example.com | viewer123 | user |

---

## Lancer avec Docker

```bash
docker compose up --build
```

L'API sera disponible sur **http://localhost:5000**

---

## Tests

```bash
pytest
```

---

## Flux de test recommandé

### 1. Créer un compte
```
POST /auth/register
```
```json
{
  "first_name": "Ahmed",
  "last_name": "Gaaloul",
  "email": "ahmed@test.com",
  "password": "secret123",
  "birth_date": "2000-01-01",
  "role": "owner"
}
```

### 2. Se connecter et récupérer le token JWT
```
POST /auth/login
```
```json
{
  "email": "ahmed@test.com",
  "password": "secret123"
}
```
Copiez le `access_token` reçu.

Dans Swagger, cliquez **Authorize** et entrez :
```
Bearer <votre_token>
```

### 3. Créer un bien immobilier
```
POST /properties
```
```json
{
  "name": "Bel appartement Paris",
  "description": "Lumineux, 3e étage",
  "city": "Paris",
  "property_type": "apartment",
  "price": 320000,
  "surface": 72
}
```

### 4. Consulter les biens d'une ville
```
GET /properties?city=Paris
```

### 5. Modifier son bien (propriétaire uniquement)
```
PUT /properties/1
```
```json
{
  "name": "Superbe appartement Paris",
  "price": 350000
}
```

### 6. Ajouter une pièce
```
POST /properties/1/rooms
```
```json
{
  "name": "Salon",
  "size": 28,
  "features": "parquet, balcon, exposition sud"
}
```

### 7. Modifier son profil
```
PUT /users/<id>
```
```json
{
  "first_name": "Alicia",
  "birth_date": "1992-03-21"
}
```

### 8. Faire une demande de visite
```
POST /properties/1/visit-requests
```
```json
{
  "requester_id": 1,
  "requested_at": "2026-04-10T14:00:00",
  "message": "Disponible l'après-midi"
}
```

---

## Endpoints complets

### Auth (public)
| Méthode | URL | Description |
|---|---|---|
| POST | `/auth/register` | Créer un compte |
| POST | `/auth/login` | Se connecter → JWT |

### Utilisateurs (authentifié)
| Méthode | URL | Description |
|---|---|---|
| GET | `/users/<id>` | Voir un profil |
| PUT | `/users/<id>` | Modifier ses informations (nom, prénom, date de naissance) |
| GET | `/users/<id>/properties` | Biens d'un utilisateur |
| GET | `/users/<id>/favorites` | Favoris d'un utilisateur |
| GET | `/users/<id>/visit-requests` | Demandes de visite d'un utilisateur |

### Biens immobiliers (authentifié)
| Méthode | URL | Description |
|---|---|---|
| GET | `/properties` | Lister les biens (filtres multiples) |
| POST | `/properties` | Créer un bien |
| GET | `/properties/<id>` | Détail d'un bien |
| PUT | `/properties/<id>` | Modifier un bien (propriétaire/admin) |
| DELETE | `/properties/<id>` | Archiver un bien (soft delete) |
| PATCH | `/properties/<id>/publish` | Publier un bien |
| PATCH | `/properties/<id>/unpublish` | Dépublier un bien |

### Pièces (authentifié)
| Méthode | URL | Description |
|---|---|---|
| POST | `/properties/<id>/rooms` | Ajouter une pièce |
| PUT | `/properties/<id>/rooms/<room_id>` | Modifier une pièce |
| DELETE | `/properties/<id>/rooms/<room_id>` | Supprimer une pièce |

### Favoris (authentifié)
| Méthode | URL | Description |
|---|---|---|
| POST | `/properties/<id>/favorite` | Ajouter aux favoris |
| DELETE | `/properties/<id>/favorite` | Retirer des favoris |

### Visites (authentifié)
| Méthode | URL | Description |
|---|---|---|
| POST | `/properties/<id>/visit-requests` | Demander une visite |
| PATCH | `/visit-requests/<id>/status` | Accepter / refuser une visite |
| GET | `/properties/<id>/visit-requests` | Lister les demandes d'un bien |

### Admin
| Méthode | URL | Description |
|---|---|---|
| GET | `/admin/stats` | Statistiques globales |
| GET | `/admin/audit-logs` | Logs d'audit |

---

## Filtres disponibles sur `GET /properties`

| Paramètre | Exemple | Description |
|---|---|---|
| `city` | `?city=Paris` | Filtrer par ville |
| `type` | `?type=apartment` | Type de bien |
| `status` | `?status=published` | Statut du bien |
| `search` | `?search=lumineux` | Recherche dans nom + description |
| `price_min` | `?price_min=100000` | Prix minimum |
| `price_max` | `?price_max=500000` | Prix maximum |
| `surface_min` | `?surface_min=50` | Surface minimum (m²) |
| `owner_id` | `?owner_id=2` | Biens d'un propriétaire |
| `min_rooms` | `?min_rooms=3` | Nombre minimum de pièces |
| `published_only` | `?published_only=true` | Biens publiés uniquement |
| `include_archived` | `?include_archived=true` | Inclure les biens archivés |
| `sort_by` | `?sort_by=price` | Trier par : `id`, `name`, `city`, `created_at`, `price`, `surface` |
| `sort_order` | `?sort_order=asc` | Ordre : `asc` ou `desc` |
| `page` | `?page=2` | Numéro de page |
| `per_page` | `?per_page=10` | Résultats par page |

---

## Architecture du code

```
app/
├── __init__.py          # Factory pattern + enregistrement des blueprints
├── extensions.py        # Instances SQLAlchemy, Redis...
├── models/              # Modèles SQLAlchemy (1 fichier par entité)
│   ├── user.py
│   ├── property.py
│   ├── room.py
│   ├── favorite.py
│   └── visit_request.py
├── services/            # Logique métier découplée des routes
│   ├── auth_service.py
│   ├── user_service.py
│   ├── property_service.py
│   └── visit_service.py
└── routes/              # Blueprints Flask (1 par ressource)
    ├── auth_routes.py
    ├── user_routes.py
    ├── property_routes.py
    ├── favorite_routes.py
    ├── visit_routes.py
    └── admin_routes.py
tests/                   # Tests pytest
seed.py                  # Données de démonstration
run.py                   # Point d'entrée
```

---

## Modèle de données

```
User                Property            Room
────────────        ────────────────    ──────────────
id                  id                  id
email               name                property_id (FK)
password_hash       description         name
first_name          city      ←filtre   size
last_name           property_type       features
birth_date          price
role                surface
                    status
                    owner_id (FK)
                    archived

VisitRequest        Favorite
────────────        ────────────
id                  id
property_id (FK)    user_id (FK)
requester_id (FK)   property_id (FK)
requested_at
status
message
```

---

## Sécurité

- Mots de passe hashés avec **bcrypt**
- Authentification **JWT** (HS256)
- **Ownership** : un propriétaire ne peut modifier que ses propres biens et pièces
- Les autres utilisateurs reçoivent un `403 Forbidden`
- **Soft delete** : les biens ne sont jamais supprimés physiquement (archivage logique)
- Gestion globale des erreurs : toutes les exceptions retournent du JSON propre

---

## Dépendances principales

| Package | Version | Rôle |
|---|---|---|
| Flask | 3.1.0 | Framework web |
| Flask-SQLAlchemy | 3.1.1 | ORM |
| flasgger | 0.9.7.1 | Documentation Swagger |
| bcrypt | 4.1.3 | Hash des mots de passe |
| pytest | 8.3.5 | Tests |