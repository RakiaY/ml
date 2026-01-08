from django.contrib.auth.models import User, Group

print("\n=== VÉRIFICATION CLIENT ===\n")

# Vérifier client
try:
    client = User.objects.get(username='client')
    print(f"✓ Client existe: {client.username}")
    print(f"  Groupes actuels: {list(client.groups.values_list('name', flat=True))}")
    
    # Créer/obtenir le groupe Client
    client_group, _ = Group.objects.get_or_create(name='Client')
    
    # Ajouter le client au groupe
    client.groups.add(client_group)
    
    print(f"✓ Client ajouté au groupe 'Client'")
    print(f"  Groupes maintenant: {list(client.groups.values_list('name', flat=True))}")
    
except User.DoesNotExist:
    print("✗ Utilisateur client n'existe pas!")
    
print("\n=== VÉRIFICATION ADMIN ===\n")

try:
    admin = User.objects.get(username='admin')
    print(f"✓ Admin existe: {admin.username}")
    print(f"  Groupes actuels: {list(admin.groups.values_list('name', flat=True))}")
    
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    admin.groups.add(admin_group)
    
    print(f"✓ Admin dans le groupe 'Admin'")
    print(f"  Groupes maintenant: {list(admin.groups.values_list('name', flat=True))}")
    
except User.DoesNotExist:
    print("✗ Utilisateur admin n'existe pas!")

print("\n=== COMPLÉTÉ ===\n")
