from django.contrib.auth.models import User, Group

# Créer/vérifier les groupes
admin_group, _ = Group.objects.get_or_create(name='Admin')
client_group, _ = Group.objects.get_or_create(name='Client')

# Vérifier et corriger admin
admin_user = User.objects.get(username='admin')
if not admin_user.groups.filter(name='Admin').exists():
    admin_user.groups.add(admin_group)
print(f"Admin: {list(admin_user.groups.values_list('name', flat=True))}")

# Vérifier et corriger client
client_user = User.objects.get(username='client')
if not client_user.groups.filter(name='Client').exists():
    client_user.groups.add(client_group)
print(f"Client: {list(client_user.groups.values_list('name', flat=True))}")

print("\n✓ Utilisateurs configurés correctement!")
