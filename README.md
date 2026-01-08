# Fashion Analytics & ML Prediction Platform

Une plateforme complète d'analyse de données et de prédiction alimentée par l'IA pour l'industrie de la mode.

## 🎯 Vue d'ensemble

Cette plateforme fournit des outils d'analyse avancés et des modèles de machine learning pour :
- **Prédiction des ventes** et analyse du panier moyen
- **Segmentation client** automatisée
- **Analyse des risques** de cancellation
- **Optimisation des prix** de produits
- **Business Intelligence** interactive via Power BI

## 🚀 Fonctionnalités principales

### 📊 Dashboard & Analytics
- **Tableau de bord principal** : Vue d'ensemble des métriques clés
- **Power BI Analytics** : Business Intelligence interactive complète

### 🛒 Prédictions de ventes
- **Future Average Basket** : Prédiction du panier moyen futur d'un client
- **Recommended Price** : Optimisation des prix de produits
- **State Revenue** : Prévision des revenus par région
- **Failed Orders** : Analyse des commandes échouées

### 👥 Analyse client
- **Women Preferences** : Préférences des produits féminins
- **Spending Level** : Classification du niveau de dépense
- **Customer Behavior** : Analyse du comportement client
- **Customer Clustering** : Segmentation en 5 groupes de shoppers

### 🎯 Gestion des risques
- **High Risk Cancelling** : Prédiction des risques de cancellation
- **Regional Analysis** : Analyse des opportunités régionales

## 🛠️ Technologies utilisées

- **Backend** : Django 6.0
- **IA/ML** : Scikit-learn, XGBoost, CatBoost
- **Base de données** : SQLite (développement)
- **Frontend** : Bootstrap 5, Font Awesome
- **Visualisation** : Power BI, Chart.js
- **Déploiement** : Prêt pour production

## 📁 Structure du projet

```
plateforme/
├── apps/                    # Applications Django modulaires
├── config/                  # Configuration centralisée
├── docs/                    # Documentation
├── models/                  # Modèles ML sauvegardés
├── notebooks/               # Notebooks Jupyter par catégorie
│   ├── classification/
│   ├── regression/
│   └── clustering/
├── static/                  # Assets statiques
├── templates/               # Templates HTML
├── accountsApp/            # Gestion des utilisateurs
├── ml_app/                 # Application principale ML
└── plateforme/             # Configuration Django
```

## 🚀 Démarrage rapide

### Prérequis
- Python 3.8+
- pip
- Virtualenv (recommandé)

### Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd plateforme
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration de la base de données**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   - Ouvrez votre navigateur à `http://127.0.0.1:8000`
   - Connectez-vous avec vos identifiants

## 📖 Guide utilisateur

### Navigation
La plateforme est organisée en 4 catégories principales :

1. **📊 Dashboard & Analytics**
   - Vue d'ensemble et métriques clés
   - Accès au dashboard Power BI

2. **🛒 Sales & Revenue**
   - Prédictions de ventes et revenus
   - Analyses financières

3. **👥 Customer Insights**
   - Analyse du comportement client
   - Segmentation et préférences

4. **🎯 Risk & Operations**
   - Gestion des risques
   - Analyses opérationnelles

### Utilisation des modèles

Chaque modèle suit le même processus :
1. Accédez à la page du modèle via la navigation
2. Remplissez le formulaire avec les données requises
3. Cliquez sur "Predict" pour obtenir les résultats
4. Analysez les prédictions et insights fournis

## 🔧 Développement

### Ajouter un nouveau modèle

1. **Créer le notebook d'entraînement** dans `notebooks/[category]/`
2. **Sauvegarder le modèle** dans `models/`
3. **Ajouter la configuration** dans `ml_app/views.py`
4. **Créer l'URL** dans `ml_app/urls.py`
5. **Créer le template** dans `templates/ml_app/`

### Structure des modèles

Chaque modèle doit avoir :
- Un fichier `.pkl` du modèle entraîné
- Un fichier de configuration des features
- Un template HTML dédié
- Une fonction view dans `views.py`

## 📊 Modèles disponibles

| Modèle | Type | Description | Features |
|--------|------|-------------|----------|
| Future Avg Basket | Regression | Prédiction panier moyen | 11 features |
| Customer Clustering | Clustering | Segmentation clients | 9 features |
| Women Preference | Classification | Préférences produits | 19 features |
| High Risk Cancelling | Classification | Risque cancellation | 8 features |
| Recommended Price | Regression | Optimisation prix | 8 features |
| Et plus... | | | |

## 🔒 Sécurité

- Authentification utilisateur obligatoire
- Validation des données d'entrée
- Protection CSRF sur tous les formulaires
- Sanitisation des sorties

## 📈 Performance

- Calcul automatique des features dérivées
- Mise en cache des modèles chargés
- Optimisation des requêtes base de données
- Interface responsive

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence propriétaire. Tous droits réservés.

## 📞 Support

Pour toute question ou support :
- 📧 Email : support@fashion-analytics.com
- 📱 Téléphone : +1 (555) 123-4567
- 🐛 Issues : GitHub Issues

---

**Fashion Analytics Platform** - Powered by AI for Fashion Intelligence