"""
Script de diagnostic - Vérifier l'état exact des groupes et utilisateurs
Exécuter avec: python manage.py shell < diagnose.py
"""

from django.contrib.auth.models import User, Group

print("\n" + "="*60)
print("DIAGNOSTIC - GROUPES ET UTILISATEURS")
print("="*60 + "\n")

# 1. Vérifier les groupes
print("1. GROUPES DISPONIBLES:")
groups = Group.objects.all()
if groups:
    for group in groups:
        print(f"   ID: {group.id} | Nom: '{group.name}' | Users: {group.user_set.count()}")
else:
    print("   ⚠️  AUCUN GROUPE!")

# 2. Vérifier les utilisateurs
print("\n2. UTILISATEURS DISPONIBLES:")
users = User.objects.all()
if users:
    for user in users:
        print(f"\n   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Is Staff: {user.is_staff}")
        print(f"   Is Superuser: {user.is_superuser}")
        groups = user.groups.all()
        if groups:
            for group in groups:
                print(f"   ✓ Groupe: {group.name} (ID: {group.id})")
        else:
            print(f"   ⚠️  AUCUN GROUPE!")
else:
    print("   ⚠️  AUCUN UTILISATEUR!")

# 3. Vérifier que admin est bien dans le groupe Admin
print("\n3. VÉRIFICATION ADMIN:")
try:
    admin_user = User.objects.get(username='admin')
    admin_group = Group.objects.get(name='Admin')
    
    if admin_user.groups.filter(name='Admin').exists():
        print(f"   ✓ Admin EST dans le groupe Admin")
    else:
        print(f"   ⚠️  Admin N'EST PAS dans le groupe Admin!")
        print(f"   → Assignation...")
        admin_user.groups.add(admin_group)
        print(f"   ✓ Assigné!")
except User.DoesNotExist:
    print(f"   ⚠️  Utilisateur admin n'existe pas!")
except Group.DoesNotExist:
    print(f"   ⚠️  Groupe Admin n'existe pas!")

print("\n" + "="*60)
print("✅ Diagnostic terminé")
print("="*60 + "\n")
