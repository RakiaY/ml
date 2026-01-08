"""
Script simple pour créer un Admin et un Client de test
Exécuter avec: python manage.py shell < create_test_users.py
"""

from django.contrib.auth.models import User, Group

print("\n" + "="*60)
print("Création des groupes et utilisateurs de test")
print("="*60 + "\n")

# Créer les groupes
admin_group, _ = Group.objects.get_or_create(name='Admin')
client_group, _ = Group.objects.get_or_create(name='Client')
print("✓ Groupes créés: Admin, Client")

# Supprimer les utilisateurs existants
User.objects.filter(username='admin').delete()
User.objects.filter(username='client').delete()
print("✓ Utilisateurs anciens supprimés (s'ils existaient)")

# Créer Admin
admin_user = User.objects.create_user(
    username='admin',
    password='admin123',
    email='admin@test.com',
    is_staff=True,
    is_superuser=True
)
admin_user.groups.add(admin_group)
print("\n✓ Admin créé:")
print(f"   Username: admin")
print(f"   Password: admin123")
print(f"   Groupe: Admin")

# Créer Client
client_user = User.objects.create_user(
    username='client',
    password='client123',
    email='client@test.com'
)
client_user.groups.add(client_group)
print("\n✓ Client créé:")
print(f"   Username: client")
print(f"   Password: client123")
print(f"   Groupe: Client")

# Vérification
print("\n" + "="*60)
print("Vérification:")
print("="*60)
for user in User.objects.all():
    groups = ', '.join([g.name for g in user.groups.all()]) or 'Aucun groupe'
    print(f"  {user.username}: {groups}")

print("\n✅ Configuration complète! Prêt à tester.\n")
