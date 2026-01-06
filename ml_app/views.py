from django.shortcuts import render
from django.conf import settings
import joblib
import os
import pandas as pd

# Load models (lazy loading)
_models = {}

def load_models():
    if not _models:
        models_dir = os.path.join(settings.BASE_DIR, 'models')
        
        # List of models to load (add them gradually)
        model_configs = {
            'women_preference': {
                'model_file': 'women_preference_model.pkl',
                'encoders_file': 'women_preference_model_encoders.pkl',
                'features': [
                    "Age", "Gender", "Zip_code", "Preferred_size", "Overall_review",
                    "Subscription Status", "Previous Purchases", "Payment Method", "Frequency of Purchases",
                    "n_women_purchases", "n_orders", "n_unique_sku", "avg_price", "std_price",
                    "min_price", "max_price", "avg_quantity", "n_unique_style", "n_unique_color"
                ],
                'cat_features': ["Gender", "Zip_code", "Preferred_size", "Subscription Status", "Payment Method", "Frequency of Purchases"],
                'type': 'classification',
                'description': 'Women Preference: Small accessories vs Nightwear'
            },
            'future_avg_basket': {
                'model_file': 'future_avg_basket.pkl',
                'encoders_file': None,  # No encoders for this model
                'features': [
                    'code_customer', 'hist_total_amount', 'hist_n_purchases', 'hist_avg_basket',
                    'Age', 'Overall_review', 'Previous Purchases', 'avg_original_price',
                    'avg_quantity', 'future_total_amount', 'future_n_purchases'
                ],
                'cat_features': [],  # No categorical features
                'type': 'regression',
                'description': 'Future Average Basket Prediction'
            }
            # Add other models here, e.g.:
            # 'model3': {...}
        }
        
        for name, config in model_configs.items():
            model_path = os.path.join(models_dir, config['model_file'])
            encoders = None
            if config['encoders_file']:
                encoders_path = os.path.join(models_dir, config['encoders_file'])
                encoders = joblib.load(encoders_path)
            _models[name] = {
                'model': joblib.load(model_path),
                'encoders': encoders,
                'config': config
            }
    return _models

def predict_view(request):
    predictions = {}
    if request.method == 'POST':
        # Retrieve all form data
        input_data = {
            "Age": float(request.POST.get('age', 0)),
            "Gender": request.POST.get('gender', ''),
            "Zip_code": request.POST.get('zip_code', ''),
            "Preferred_size": request.POST.get('preferred_size', ''),
            "Overall_review": float(request.POST.get('overall_review', 0)),
            "Subscription Status": request.POST.get('subscription_status', ''),
            "Previous Purchases": int(request.POST.get('previous_purchases', 0)),
            "Payment Method": request.POST.get('payment_method', ''),
            "Frequency of Purchases": request.POST.get('frequency_of_purchases', ''),
            "n_women_purchases": int(request.POST.get('n_women_purchases', 1)),
            "n_orders": int(request.POST.get('n_orders', 1)),
            "n_unique_sku": int(request.POST.get('n_unique_sku', 1)),
            "avg_price": float(request.POST.get('avg_price', 50)),
            "std_price": float(request.POST.get('std_price', 0)),
            "min_price": float(request.POST.get('min_price', 50)),
            "max_price": float(request.POST.get('max_price', 50)),
            "avg_quantity": float(request.POST.get('avg_quantity', 1)),
            "n_unique_style": int(request.POST.get('n_unique_style', 1)),
            "n_unique_color": int(request.POST.get('n_unique_color', 1)),
            # New fields for future_avg_basket model
            "code_customer": request.POST.get('code_customer', ''),
            "hist_total_amount": float(request.POST.get('hist_total_amount', 0)),
            "hist_n_purchases": int(request.POST.get('hist_n_purchases', 0)),
            "hist_avg_basket": float(request.POST.get('hist_avg_basket', 0)),
            "avg_original_price": float(request.POST.get('avg_original_price', 0)),
            "future_total_amount": float(request.POST.get('future_total_amount', 0)),
            "future_n_purchases": int(request.POST.get('future_n_purchases', 0)),
            # Add other fields as needed for future models
        }

        models = load_models()
        for name, model_data in models.items():
            model = model_data['model']
            encoders = model_data['encoders']
            config = model_data['config']
            
            # Select relevant features for this model
            model_features = config['features']
            df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
            
            # Encode categorical features
            cat_cols = config.get('cat_features', [])
            for col in cat_cols:
                if encoders and col in encoders:
                    le = encoders[col]
                    df_input[col] = le.transform(df_input[col].astype(str))
            
            # Predict
            pred = model.predict(df_input)[0]
            predictions[name] = {
                'result': pred,
                'description': config['description'],
                'type': config['type']
            }

    return render(request, 'ml_app/predict.html', {'predictions': predictions})
