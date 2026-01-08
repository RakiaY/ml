import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plateforme.settings')
import django
django.setup()
from ml_app import views
print('Calling load_models...')
models = views.load_models()
print('Loaded models:')
for k,v in models.items():
    print('-', k, '->', 'model' in v and bool(v['model']))
    if v.get('scaler') is not None:
        print('   scaler:', type(v['scaler']))
    if v.get('features') is not None:
        print('   features:', v.get('features'))
