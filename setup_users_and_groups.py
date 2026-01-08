"""
Script d'initialisation des groupes et des utilisateurs de test
Exécuter avec: python manage.py shell < setup_users_and_groups.py
"""

from django.contrib.auth.models import User, Group, Permission

# Créer les groupes
admin_group, created = Group.objects.get_or_create(name='Admin')
client_group, created = Group.objects.get_or_create(name='Client')

# Ajouter toutes les permissions au groupe Admin
all_permissions = Permission.objects.all()
admin_group.permissions.set(all_permissions)

print("✓ Groupes créés avec succès!")
print(f"  - Admin: {admin_group.permissions.count()} permissions")
print(f"  - Client: {client_group.permissions.count()} permissions")

# Créer un utilisateur Admin de test (optionnel)
try:
    admin_user = User.objects.create_user(
        username='admin',
        password='admin123',
        email='admin@example.com',
        is_staff=True,
        is_superuser=True
    )
    admin_user.groups.add(admin_group)
    print("\n✓ Utilisateur Admin créé: admin / admin123")
except Exception as e:
    print(f"\n⚠ Admin existant ou erreur: {e}")

# Créer un utilisateur Client de test (optionnel)
try:
    client_user = User.objects.create_user(
        username='client',
        password='client123',
        email='client@example.com'
    )
    client_user.groups.add(client_group)
    print("✓ Utilisateur Client créé: client / client123")
except Exception as e:
    print(f"⚠ Client existant ou erreur: {e}")

print("\n" + "="*60)
print("Configuration complète!")
print("="*60)
print("\n🔐 Comportement attendu:")
print("  Admin:")
print("    - Accès à toutes les pages (dashboard, modèles, power_bi)")
print("\n  Client:")
print("    - Accès aux modèles ML uniquement")
print("    - Dashboard: ❌ Déconnexion automatique")
print("    - Power BI: ❌ Déconnexion automatique")
