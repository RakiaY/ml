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
                'scaler_file': None,
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
                'model_file': 'regression_recommended_price.pkl',
                'encoders_file': None,
                'scaler_file': 'regression_recommended_price_scaler.pkl',
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
            },
            'regression_failed_orders': {
                'model_file': 'regression_failed_orders_pct.pkl',
                'encoders_file': None,
                'scaler_file': None,
                'features': ['period_num'],
                'cat_features': [],
                'type': 'regression',
                'description': 'Failed Orders Percentage Prediction'
            },
            'classification_high_risk_cancelling': {
                'model_file': 'classification_high_risk_cancelling.pkl',
                'encoders_file': None,
                'scaler_file': 'classification_high_risk_cancelling_scaler.pkl',
                'features': ['total_orders', 'total_cancelled', 'avg_quantity', 'avg_unit_price', 'unique_products', 'total_not_cancelled', 'age', 'gender_male'],
                'cat_features': [],
                'type': 'classification',
                'description': 'High Risk Cancelling Customer Classification'
            },
            'regression_state_revenue': {
                'model_file': 'regression_state_revenue.pkl',
                'encoders_file': None,
                'scaler_file': 'regression_state_revenue_scaler.pkl',
                'features': ['nb_orders', 'nb_customers', 'avg_basket', 'return_rate_pct', 'avg_age', 'pct_male', 'total_qty_sold'],
                'cat_features': [],
                'type': 'regression',
                'description': 'State Revenue Regression'
            },
            'classification_customer_behavior': {
                'model_file': 'classification_customer_behavior.pkl',
                'encoders_file': 'classification_customer_behavior_encoders.pkl',
                'scaler_file': 'classification_customer_behavior_scaler.pkl',
                'features': [
                    'total_purchases', 'total_quantity', 'avg_unit_price', 'total_spent',
                    'discount_rate', 'customer_lifetime_days', 'purchase_frequency',
                    'avg_order_value', 'return_cancel_rate', 'Age', 'Overall_review',
                    'Previous Purchases', 'Gender_encoded', 'Preferred_size_encoded',
                    'Payment Method_encoded', 'Frequency of Purchases_encoded'
                ],
                'cat_features': ['Gender', 'Preferred_size', 'Payment Method', 'Frequency of Purchases'],
                'type': 'classification',
                'description': 'Customer Behavior Classification'
            }
            ,
            'ghada_regression': {
                'model_file': 'ghada_regression_model.pkl',
                'encoders_file': None,
                'scaler_file': 'ghada_regression_scaler.pkl',
                'features': [
                    'freq_per_month', 'discount_rate', 'recency_days', 'tenure_days',
                    'past_purchases', 'unique_products', 'total_spent', 'Overall_review',
                    'is_subscribed', 'purchases_per_month', 'discount_sensitivity', 'variety_index',
                    'monetary_intensity', 'recency_ratio', 'spend_per_product', 'discount_ratio',
                    'activity_intensity', 'recent_purchases', 'recent_spent', 'recent_unique_products'
                ],
                'cat_features': [],
                'type': 'regression',
                'description': 'Ghada Regression: Future Rate Prediction'
            },
            'customer_clustering': {
                'model_file': 'customer_clustering_model.pkl',
                'encoders_file': None,
                'scaler_file': 'customer_clustering_scaler.pkl',
                'features_file': 'customer_clustering_features.pkl',
                'features': [
                    'total_purchases', 'total_quantity', 'avg_unit_price', 'total_spent',
                    'discount_rate', 'customer_lifetime_days', 'purchase_frequency',
                    'avg_order_value', 'return_cancel_rate'
                ],
                'cat_features': [],
                'type': 'clustering',
                'description': 'Customer Clustering: 5 shopper segments'
            }
        }
        
        for name, config in model_configs.items():
            model_path = os.path.join(models_dir, config['model_file'])
            encoders = None
            scaler = None
            features = None
            if config.get('encoders_file'):
                encoders_path = os.path.join(models_dir, config['encoders_file'])
                encoders = joblib.load(encoders_path)
            if config.get('scaler_file'):
                scaler_path = os.path.join(models_dir, config['scaler_file'])
                scaler = joblib.load(scaler_path)
            if config.get('features_file'):
                features_path = os.path.join(models_dir, config['features_file'])
                features = joblib.load(features_path)
            _models[name] = {
                'model': joblib.load(model_path),
                'encoders': encoders,
                'scaler': scaler,
                'features': features,
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
            "SKU_encoded": float(request.POST.get('sku_encoded', 0)),
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
        scaler = model_data['scaler']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        df_input = df_input.astype(float)
        if hasattr(model, 'feature_names_in_'):
            df_input = df_input[model.feature_names_in_]
        # Apply scaling to numerical features
        if scaler:
            numerical_cols = [col for col in df_input.columns]
            df_input[numerical_cols] = scaler.transform(df_input[numerical_cols])
        pred = model.predict(df_input)[0]
        # Assuming pred is the discount percentage
        estimated_price = input_data["Estimated_Unit_Price"]
        # Cap the discount percentage between 0 and 100
        discount_percentage = max(0, min(100, pred))
        discount_amount = estimated_price * (discount_percentage / 100)
        recommended_price = estimated_price - discount_amount
        predictions['recommended_price'] = {
            'result': recommended_price,
            'discount_percentage': discount_percentage,
            'discount_amount': discount_amount,
            'estimated_price': estimated_price,
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

def regression_failed_orders_view(request):
    predictions = {}
    if request.method == 'POST':
        year = int(request.POST.get('year', 2025))
        # Compute period_num from year
        period_num = pd.Timestamp(f'{year}-01-01').timestamp()
        
        print(f"Year: {year}, Period_num: {period_num}")
        
        input_data = {
            "period_num": period_num
        }
        
        model_data = load_models()['regression_failed_orders']
        model = model_data['model']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        
        print(f"Input DataFrame: {df_input}")
        
        pred = model.predict(df_input)[0]
        
        print(f"Prediction: {pred}")
        
        predictions['regression_failed_orders'] = {
            'result': pred,
            'year': year,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/regression_failed_orders.html', {'predictions': predictions})

def classification_high_risk_cancelling_view(request):
    predictions = {}
    if request.method == 'POST':
        input_data = {
            "total_orders": int(request.POST.get('total_orders', 0)),
            "total_cancelled": int(request.POST.get('total_cancelled', 0)),
            "avg_quantity": float(request.POST.get('avg_quantity', 1)),
            "avg_unit_price": float(request.POST.get('avg_unit_price', 0)),
            "unique_products": int(request.POST.get('unique_products', 0)),
            "age": int(request.POST.get('age', 25)),
        }
        gender = request.POST.get('gender', 'Male')
        input_data["gender_male"] = 1 if gender == 'Male' else 0
        input_data["total_not_cancelled"] = input_data["total_orders"] - input_data["total_cancelled"]
        
        model_data = load_models()['classification_high_risk_cancelling']
        model = model_data['model']
        scaler = model_data['scaler']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        df_input = df_input.astype(float)
        if scaler:
            numerical_cols = [col for col in df_input.columns]
            df_input[numerical_cols] = scaler.transform(df_input[numerical_cols])
        pred = model.predict(df_input)[0]
        risk_label = "High Risk" if pred == 1 else "Low Risk"
        predictions['classification_high_risk_cancelling'] = {
            'result': risk_label,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/classification_high_risk_cancelling.html', {'predictions': predictions})

def regression_state_revenue_view(request):
    predictions = {}
    if request.method == 'POST':
        input_data = {
            "nb_orders": int(request.POST.get('nb_orders', 0)),
            "nb_customers": int(request.POST.get('nb_customers', 0)),
            "avg_basket": float(request.POST.get('avg_basket', 0)),
            "return_rate_pct": float(request.POST.get('return_rate_pct', 0)),
            "avg_age": float(request.POST.get('avg_age', 0)),
            "pct_male": float(request.POST.get('pct_male', 0)),
            "total_qty_sold": int(request.POST.get('total_qty_sold', 0)),
        }
        model_data = load_models()['regression_state_revenue']
        model = model_data['model']
        scaler = model_data['scaler']
        config = model_data['config']
        model_features = config['features']
        df_input = pd.DataFrame([{k: input_data[k] for k in model_features if k in input_data}], columns=model_features)
        df_input = df_input.astype(float)
        if scaler:
            numerical_cols = [col for col in df_input.columns]
            df_input[numerical_cols] = scaler.transform(df_input[numerical_cols])
        pred = model.predict(df_input)[0]
        predictions['regression_state_revenue'] = {
            'result': pred,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/regression_state_revenue.html', {'predictions': predictions})

def classification_customer_behavior_view(request):
    predictions = {}
    if request.method == 'POST':
        input_data = {
            "total_purchases": int(request.POST.get('total_purchases', 0)),
            "total_quantity": int(request.POST.get('total_quantity', 0)),
            "avg_unit_price": float(request.POST.get('avg_unit_price', 0)),
            "total_spent": float(request.POST.get('total_spent', 0)),
            "discount_rate": float(request.POST.get('discount_rate', 0)),
            "customer_lifetime_days": int(request.POST.get('customer_lifetime_days', 0)),
            "purchase_frequency": float(request.POST.get('purchase_frequency', 0)),
            "avg_order_value": float(request.POST.get('avg_order_value', 0)),
            "return_cancel_rate": float(request.POST.get('return_cancel_rate', 0)),
            "Age": int(request.POST.get('age', 25)),
            "Overall_review": float(request.POST.get('overall_review', 0)),
            "Previous Purchases": int(request.POST.get('previous_purchases', 0)),
            "Gender": request.POST.get('gender', ''),
            "Preferred_size": request.POST.get('preferred_size', ''),
            "Payment Method": request.POST.get('payment_method', ''),
            "Frequency of Purchases": request.POST.get('frequency_of_purchases', ''),
        }
        
        model_data = load_models()['classification_customer_behavior']
        model = model_data['model']
        encoders = model_data['encoders']
        scaler = model_data['scaler']
        config = model_data['config']
        model_features = config['features']
        
        # Create DataFrame with numerical features first
        numerical_features = [f for f in model_features if not f.endswith('_encoded')]
        df_input = pd.DataFrame([{k: input_data[k] for k in numerical_features}], columns=numerical_features)
        
        # Encode categorical features and add to DataFrame
        cat_cols = config.get('cat_features', [])
        for col in cat_cols:
            if encoders and col in encoders:
                le = encoders[col]
                encoded_col = col + '_encoded'
                try:
                    df_input[encoded_col] = le.transform([input_data[col]])
                except ValueError:
                    # If unseen label, use the first class
                    df_input[encoded_col] = le.transform([le.classes_[0]])
        
        # Ensure all features are present
        df_input = df_input.astype(float)
        
        # Apply scaling to all features
        if scaler:
            df_input = pd.DataFrame(scaler.transform(df_input), columns=df_input.columns, index=df_input.index)
        
        pred = model.predict(df_input)[0]
        
        # Map prediction to class name
        class_names = {
            0: 'Occasional Buyers',
            1: 'Regular Loyalists',
            2: 'Bargain Hunters',
            3: 'VIP Shoppers',
            4: 'Problem Customers'
        }
        class_name = class_names.get(pred, f'Class {pred}')
        
        predictions['classification_customer_behavior'] = {
            'result': class_name,
            'class_number': pred,
            'description': config['description'],
            'type': config['type']
        }
    return render(request, 'ml_app/classification_customer_behavior.html', {'predictions': predictions})


def regression_ghada_view(request):
    predictions = {}
    if request.method == 'POST':
        # Collect inputs for features (use 0 / reasonable defaults if missing)
        model_data = load_models().get('ghada_regression')
        if not model_data:
            return render(request, 'ml_app/regression_model_y.html', {'error': 'Model not loaded'})

        config = model_data['config']
        model = model_data['model']
        scaler = model_data['scaler']
        features = config['features']

        # Build input dict from POST
        input_data = {}
        for feat in features:
            # default to 0, try integer then float
            val = request.POST.get(feat, None)
            if val is None or val == '':
                input_data[feat] = 0.0
            else:
                try:
                    input_data[feat] = float(val)
                except Exception:
                    input_data[feat] = 0.0

        df_input = pd.DataFrame([input_data], columns=features)
        # Apply scaler if present
        if scaler:
            try:
                df_input = pd.DataFrame(scaler.transform(df_input), columns=df_input.columns, index=df_input.index)
            except Exception:
                # If scaler expects different ordering/cols, try numeric conversion
                df_input = df_input.astype(float)
        else:
            df_input = df_input.astype(float)

        pred = model.predict(df_input)[0]
        predictions['ghada_regression'] = {
            'result': pred,
            'description': config['description'],
            'type': config['type'],
            'year': request.POST.get('year', '')
        }

    return render(request, 'ml_app/regression_ghada.html', {'predictions': predictions})
