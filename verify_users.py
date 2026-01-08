"""
Script pour VÉRIFIER et CORRIGER les groupes et utilisateurs
Exécuter avec: python manage.py shell < verify_users.py
"""

from django.contrib.auth.models import User, Group

print("\n" + "="*60)
print("VÉRIFICATION DES GROUPES ET UTILISATEURS")
print("="*60 + "\n")

# Vérifier et créer les groupes
print("1. GROUPES:")
admin_group, created = Group.objects.get_or_create(name='Admin')
client_group, created = Group.objects.get_or_create(name='Client')
print(f"   ✓ Admin groupe (ID: {admin_group.id})")
print(f"   ✓ Client groupe (ID: {client_group.id})")

# Vérifier les utilisateurs
print("\n2. UTILISATEURS ACTUELS:")
if User.objects.exists():
    for user in User.objects.all():
        groups = list(user.groups.all())
        group_names = ', '.join([g.name for g in groups]) if groups else 'AUCUN GROUPE ⚠️'
        print(f"   - {user.username}: {group_names}")
else:
    print("   Aucun utilisateur!")

# Supprimer et recréer les utilisateurs
print("\n3. RECRÉATION DES UTILISATEURS:")
User.objects.filter(username__in=['admin', 'client']).delete()
print("   ✓ Anciens utilisateurs supprimés")

# Créer Admin
admin_user = User.objects.create_user(
    username='admin',
    password='admin123',
    email='admin@test.com',
    is_staff=True,
    is_superuser=True
)
admin_user.groups.add(admin_group)
admin_user.save()
print(f"   ✓ Admin créé et assigné au groupe Admin")

# Créer Client
client_user = User.objects.create_user(
    username='client',
    password='client123',
    email='client@test.com'
)
client_user.groups.add(client_group)
client_user.save()
print(f"   ✓ Client créé et assigné au groupe Client")

# Vérification finale
print("\n4. VÉRIFICATION FINALE:")
for user in User.objects.all():
    groups = list(user.groups.all())
    group_names = ', '.join([g.name for g in groups])
    print(f"   ✓ {user.username}: {group_names}")

print("\n" + "="*60)
print("✅ Configuration complète et vérifiée!")
print("="*60)
print("\nIdentifiants de test:")
print("  Admin:  admin / admin123")
print("  Client: client / client123")
print("\nRedémarrez le serveur et testez!\n")
