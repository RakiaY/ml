"""
Script pour créer les groupes Admin et Client + utilisateurs de test
Exécuter avec: python manage.py shell < create_groups.py
"""

from django.contrib.auth.models import User, Group, Permission

print("\n" + "="*60)
print("RECRÉATION COMPLÈTE DES UTILISATEURS")
print("="*60 + "\n")

# Créer/vérifier les groupes
admin_group, _ = Group.objects.get_or_create(name='Admin')
client_group, _ = Group.objects.get_or_create(name='Client')

# SUPPRIMER les anciens utilisateurs
User.objects.filter(username__in=['admin', 'client']).delete()
print("✓ Anciens utilisateurs supprimés")

# CRÉER ADMIN
admin = User.objects.create_user(
    username='admin',
    password='admin123',
    is_staff=True,
    is_superuser=True
)
admin.groups.add(admin_group)
print(f"✓ Admin créé: {admin.username} - Groupes: {list(admin.groups.values_list('name', flat=True))}")

# CRÉER CLIENT
client = User.objects.create_user(
    username='client',
    password='client123'
)
client.groups.add(client_group)
print(f"✓ Client créé: {client.username} - Groupes: {list(client.groups.values_list('name', flat=True))}")

print("\n" + "="*60)
print("✅ CONFIGURATION COMPLÈTE")
print("="*60)
print("\nIdentifiants:")
print("  Admin:  admin / admin123")
print("  Client: client / client123")
print("\nRedémarrez le serveur et testez!\n")
