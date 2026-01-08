# Guide de Test - Groupes d'Utilisateurs

## Setup Initial

1. Exécuter le script de configuration:
```bash
python manage.py shell < setup_users_and_groups.py
```

2. Démarrer le serveur:
```bash
python manage.py runserver
```

## Scénarios de Test

### Test 1: Admin accède au Dashboard ✅
1. Aller à `http://localhost:8000/accounts/login/`
2. Se connecter avec: `admin` / `admin123`
3. Cliquer sur Dashboard
4. **Résultat attendu**: Page de dashboard affichée

### Test 2: Admin accède à un modèle ML ✅
1. (Connecté en tant qu'Admin)
2. Aller à `http://localhost:8000/ml/women_preference/`
3. **Résultat attendu**: Formulaire du modèle affiché

### Test 3: Admin accède à Power BI ✅
1. (Connecté en tant qu'Admin)
2. Aller à `http://localhost:8000/ml/power_bi_dashboard/`
3. **Résultat attendu**: Dashboard Power BI affiché

### Test 4: Client accède aux modèles ML ✅
1. Se déconnecter (logout)
2. Se connecter avec: `client` / `client123`
3. Aller à `http://localhost:8000/ml/women_preference/`
4. **Résultat attendu**: Formulaire du modèle affiché

### Test 5: Client accède au Dashboard ❌
1. (Connecté en tant que Client)
2. Tenter d'accéder à `http://localhost:8000/accounts/dashboard/`
3. **Résultat attendu**: 
   - Message d'erreur: "Accès refusé. Vous avez été déconnecté."
   - Redirection vers la page de login

### Test 6: Client accède à Power BI ❌
1. Se reconnecter en tant que Client (`client` / `client123`)
2. Tenter d'accéder à `http://localhost:8000/ml/power_bi_dashboard/`
3. **Résultat attendu**:
   - Message d'erreur: "Accès refusé. Vous avez été déconnecté."
   - Redirection vers la page de login

## Vérification des Groupes en Django Admin

1. Aller à `http://localhost:8000/admin/`
2. Se connecter avec les credentials superuser (si disponible)
3. Vérifier les groupes dans "Authentication and Authorization" > "Groups"
4. Vérifier les utilisateurs et leurs groupes

## Résumé du Comportement

| Utilisateur | Dashboard | Modèles ML | Power BI |
|-----------|-----------|-----------|---------|
| Admin | ✅ Accès | ✅ Accès | ✅ Accès |
| Client | ❌ Déconnexion | ✅ Accès | ❌ Déconnexion |
| Non authentifié | ↗️ Login | ↗️ Login | ↗️ Login |

Legend:
- ✅ = Accès autorisé
- ❌ = Déconnexion automatique + Message d'erreur
- ↗️ = Redirection vers login
