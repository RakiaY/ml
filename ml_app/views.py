from django.shortcuts import render
from django.conf import settings
import joblib
import os
import pandas as pd
import math

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
            },
            'classification_potential_region': {
                'model_file': 'classification_potential_region.pkl',
                'encoders_file': None,  # Manual one-hot encoding
                'features': [
                    'age_std', 'age_mean', 'freq_mean', 'freq_std', 'n_customers',
                    'rev_norm', 'sub_norm', 'prev_norm', 'freq_consistency',
                    'rev_x_prev', 'sub_x_age', 'rev_x_sub'
                ],
                'cat_features': [],  # Handled manually
                'type': 'classification',
                'description': 'Potential Region Classification'
            },
            'recommended_price': {
                'model_file': 'regression_model_y.pkl',
                'encoders_file': 'regression_model_y_encoder.pkl',
                'features': [
                    'SKU_encoded', 'num_purchases', 'quantity', 'date_flexibility', 'Estimated_Unit_Price',
                    'price_quantity', 'purchases_flexibility', 'price_purchases'
                ],
                'cat_features': [],
                'type': 'regression',
                'description': 'Recommended Product Price Prediction'
            },
            'spending_level': {
                'model_file': 'Classification_Spending_Level.pkl',
                'encoders_file': 'Classification_Spending_Level_encoders.pkl',
                'features': [
                    'Gender', 'Age', 'Frequency of Purchases', 'Payment Method', 'discount_rate', 'log_quantity',
                    'age_freq', 'discount_qty', 'Subscription_Status', 'avg_prev_per_age', 'avg_prev_by_freq', 'prev_per_age'
                ],
                'cat_features': ['Gender', 'Frequency of Purchases', 'Payment Method'],
                'type': 'classification',
                'description': 'Customer Spending Level Prediction'
            }
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
            # Fields for potential region model
            "age_std": float(request.POST.get('age_std', 0)),
            "age_mean": float(request.POST.get('age_mean', 0)),
            "freq_mean": float(request.POST.get('freq_mean', 0)),
            "freq_std": float(request.POST.get('freq_std', 0)),
            "n_customers": int(request.POST.get('n_customers', 1)),
            "rev_norm": float(request.POST.get('rev_norm', 0)),
            "sub_norm": float(request.POST.get('sub_norm', 0)),
            "prev_norm": float(request.POST.get('prev_norm', 0)),
            "freq_consistency": float(request.POST.get('freq_consistency', 0)),
            "rev_x_prev": float(request.POST.get('rev_x_prev', 0)),
            "sub_x_age": float(request.POST.get('sub_x_age', 0)),
            "rev_x_sub": float(request.POST.get('rev_x_sub', 0)),
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

def women_preference_view(request):
    predictions = {}
    if request.method == 'POST':
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
        }
        model_data = load_models()['women_preference']
        model = model_data['model']
        encoders = model_data['encoders']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        cat_cols = config.get('cat_features', [])
        for col in cat_cols:
            if encoders and col in encoders:
                le = encoders[col]
                df_input[col] = le.transform(df_input[col].astype(str))
        pred = model.predict(df_input)[0]
        predictions['women_preference'] = {
            'result': pred,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/women_preference.html', {'predictions': predictions})

def future_avg_basket_view(request):
    predictions = {}
    if request.method == 'POST':
        input_data = {
            "code_customer": request.POST.get('code_customer', ''),
            "hist_total_amount": float(request.POST.get('hist_total_amount', 0)),
            "hist_n_purchases": int(request.POST.get('hist_n_purchases', 0)),
            "hist_avg_basket": float(request.POST.get('hist_avg_basket', 0)),
            "Age": float(request.POST.get('age', 0)),
            "Overall_review": float(request.POST.get('overall_review', 0)),
            "Previous Purchases": int(request.POST.get('previous_purchases', 0)),
            "avg_original_price": float(request.POST.get('avg_original_price', 0)),
            "avg_quantity": float(request.POST.get('avg_quantity', 1)),
            "future_total_amount": float(request.POST.get('future_total_amount', 0)),
            "future_n_purchases": int(request.POST.get('future_n_purchases', 0)),
        }
        model_data = load_models()['future_avg_basket']
        model = model_data['model']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        pred = model.predict(df_input)[0]
        predictions['future_avg_basket'] = {
            'result': pred,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/future_avg_basket.html', {'predictions': predictions})

def potential_region_view(request):
    predictions = {}
    if request.method == 'POST':
        input_data = {
            "age_std": float(request.POST.get('age_std', 0)),
            "age_mean": float(request.POST.get('age_mean', 0)),
            "freq_mean": float(request.POST.get('freq_mean', 0)),
            "freq_std": float(request.POST.get('freq_std', 0)),
            "n_customers": int(request.POST.get('n_customers', 1)),
            "rev_norm": float(request.POST.get('rev_norm', 0)),
            "sub_norm": float(request.POST.get('sub_norm', 0)),
            "prev_norm": float(request.POST.get('prev_norm', 0)),
            "freq_consistency": float(request.POST.get('freq_consistency', 0)),
            "rev_x_prev": float(request.POST.get('rev_x_prev', 0)),
            "sub_x_age": float(request.POST.get('sub_x_age', 0)),
            "rev_x_sub": float(request.POST.get('rev_x_sub', 0)),
        }
        model_data = load_models()['classification_potential_region']
        model = model_data['model']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        pred = model.predict(df_input)[0]
        predictions['classification_potential_region'] = {
            'result': pred,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/potential_region.html', {'predictions': predictions})

def recommended_price_view(request):
    predictions = {}
    if request.method == 'POST':
        input_data = {
            "SKU_encoded": request.POST.get('sku_encoded', ''),
            "num_purchases": int(request.POST.get('num_purchases', 0)),
            "quantity": int(request.POST.get('quantity', 1)),
            "date_flexibility": float(request.POST.get('date_flexibility', 0)),
            "Estimated_Unit_Price": float(request.POST.get('estimated_unit_price', 0)),
        }
        # Compute derived features
        input_data["price_quantity"] = input_data["Estimated_Unit_Price"] * input_data["quantity"]
        input_data["purchases_flexibility"] = input_data["num_purchases"] * input_data["date_flexibility"]
        input_data["price_purchases"] = input_data["Estimated_Unit_Price"] * input_data["num_purchases"]
        
        model_data = load_models()['recommended_price']
        model = model_data['model']
        encoders = model_data['encoders']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        cat_cols = config.get('cat_features', [])
        if encoders:
            for col in cat_cols:
                df_input[col] = encoders.transform(df_input[col].astype(int))
        pred = model.predict(df_input)[0]
        predictions['recommended_price'] = {
            'result': pred,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/recommended_price.html', {'predictions': predictions})

def spending_level_view(request):
    predictions = {}
    if request.method == 'POST':
        input_data = {
            "Gender": '0' if request.POST.get('gender', '') == 'Male' else '1',
            "Age": int(request.POST.get('age', 0)),
            "Frequency of Purchases": {'Rarely': '0', 'Occasionally': '1', 'Frequently': '2'}.get(request.POST.get('frequency_of_purchases', ''), '0'),
            "Payment Method": {'Credit Card': '0', 'Debit Card': '1', 'PayPal': '2', 'Cash': '3'}.get(request.POST.get('payment_method', ''), '0'),
            "Subscription_Status": 1 if request.POST.get('subscription_status', '') == 'Yes' else 0,
            "Previous_Purchases": int(request.POST.get('previous_purchases', 0)),
            "Quantity": int(request.POST.get('quantity', 1)),
            "original_price": float(request.POST.get('original_price', 0)),
            "discount_amount": float(request.POST.get('discount_amount', 0)),
        }
        # Compute derived features
        discount_rate = input_data["discount_amount"] / input_data["original_price"] if input_data["original_price"] != 0 else 0
        log_quantity = math.log(input_data["Quantity"] + 1)
        freq_map = {'Rarely': 0, 'Occasionally': 1, 'Frequently': 2}
        freq_num = freq_map.get(input_data["Frequency of Purchases"], 0)
        age_freq = input_data["Age"] * freq_num
        discount_qty = discount_rate * input_data["Quantity"]
        avg_prev_per_age = input_data["Previous_Purchases"] / input_data["Age"] if input_data["Age"] > 0 else 0
        avg_prev_by_freq = input_data["Previous_Purchases"] / freq_num if freq_num > 0 else 0
        prev_per_age = input_data["Previous_Purchases"] / (input_data["Age"] + 1)
        avg_prev_per_age = input_data["Previous_Purchases"] / input_data["Age"] if input_data["Age"] > 0 else 0
        avg_prev_by_freq = input_data["Previous_Purchases"] / freq_num if freq_num > 0 else 0
        prev_per_age = input_data["Previous_Purchases"] / (input_data["Age"] + 1)
        
        input_data["discount_rate"] = discount_rate
        input_data["log_quantity"] = log_quantity
        input_data["age_freq"] = age_freq
        input_data["discount_qty"] = discount_qty
        input_data["avg_prev_per_age"] = avg_prev_per_age
        input_data["avg_prev_by_freq"] = avg_prev_by_freq
        input_data["prev_per_age"] = prev_per_age
        
        model_data = load_models()['spending_level']
        model = model_data['model']
        encoders = model_data['encoders']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        cat_cols = config.get('cat_features', [])
        if encoders and 'label_encoders' in encoders:
            for col in cat_cols:
                if col in encoders['label_encoders']:
                    le = encoders['label_encoders'][col]
                    df_input[col] = le.transform(df_input[col].astype(str))
        pred = model.predict(df_input)[0]
        predictions['spending_level'] = {
            'result': pred,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/spending_level.html', {'predictions': predictions})
