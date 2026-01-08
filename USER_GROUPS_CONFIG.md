# Configuration des Groupes d'Utilisateurs

## Vue d'ensemble

Le système est configuré avec deux groupes d'utilisateurs:
- **Admin**: Accès complet à l'application
- **Client**: Accès aux modèles ML uniquement

## Scénarios d'accès

### 1. Admin se connecte
✅ Accès à TOUTES les pages:
- Dashboard (`/accounts/dashboard/`)
- Tous les modèles ML (`/ml/women_preference/`, etc.)
- Power BI Dashboard (`/ml/power_bi_dashboard/`)

### 2. Client se connecte
✅ Accès AUX MODÈLES ML uniquement:
- `/ml/women_preference/`
- `/ml/future_avg_basket/`
- `/ml/potential_region/`
- `/ml/recommended_price/`
- `/ml/spending_level/`
- `/ml/regression_failed_orders/`
- `/ml/classification_high_risk_cancelling/`
- `/ml/regression_state_revenue/`
- `/ml/classification_customer_behavior/`
- `/ml/future_purchases/`
- `/ml/customer_clustering/`
- `/ml/regional_clustering/`

❌ INTERDICTION - Dashboard:
- URL: `/accounts/dashboard/`
- Comportement: Déconnexion automatique + message "Accès refusé"

❌ INTERDICTION - Power BI:
- URL: `/ml/power_bi_dashboard/`
- Comportement: Déconnexion automatique + message "Accès refusé"

## Installation

### 1. Exécuter le script de configuration

**Sur PowerShell (Windows):**
```powershell
cmd /c "python manage.py shell < setup_users_and_groups.py"
```

**Sur bash/Linux/Mac:**
```bash
python manage.py shell < setup_users_and_groups.py
```

Cela va:
- Créer les groupes `Admin` et `Client`
- Créer un utilisateur de test Admin: `admin` / `admin123`
- Créer un utilisateur de test Client: `client` / `client123`

### 2. Décorateurs utilisés

#### `@admin_only`
- Restreint l'accès aux administrateurs uniquement
- Déconnecte et redirige les non-admins
- Appliqué à:
  - Dashboard (`/accounts/dashboard/`)
  - Power BI Dashboard (`/ml/power_bi_dashboard/`)

#### `@client_or_admin`
- Permet l'accès aux clients ET administrateurs
- Déconnecte et redirige les autres
- Appliqué à:
  - Tous les modèles ML

### 3. Fichiers modifiés

1. **accountsApp/decorators.py** (NOUVEAU)
   - Définit `@admin_only` et `@client_or_admin`

2. **accountsApp/views.py**
   - Dashboard: `@admin_only`

3. **ml_app/views.py**
   - Power BI: `@admin_only`
   - Tous les modèles: `@client_or_admin`

## Gestion des utilisateurs

### Ajouter un utilisateur à un groupe

```python
# Via Django admin
# Ou via shell:
from django.contrib.auth.models import User, Group

user = User.objects.get(username='username')
admin_group = Group.objects.get(name='Admin')
user.groups.add(admin_group)
```

### Vérifier le groupe d'un utilisateur

```python
from django.contrib.auth.models import User

user = User.objects.get(username='username')
print(user.groups.all())  # Affiche les groupes
```

## Messages d'erreur

Quand un utilisateur non-autorisé accède à une page protégée:
- Message: "Accès refusé. Vous avez été déconnecté."
- Action: Redirection automatique vers la page de login

## Architecture

```
Requête utilisateur
    ↓
Vérification authentification (@login_required)
    ↓
Vérification groupe (@admin_only ou @client_or_admin)
    ├─ ✅ Groupe autorisé → Accès à la page
    └─ ❌ Groupe non autorisé → Déconnexion + Redirection
```

## Notes de sécurité

- Les groupes sont gérés par Django contrib.auth
- Les permissions sont basées sur l'appartenance aux groupes
- Pas de stockage de tokens ou de sessions personnalisées
- Les messages d'erreur aident à l'UX sans révéler d'informations sensibles
