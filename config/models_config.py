# Configuration centralisée des modèles ML
# Fashion Analytics Platform

MODEL_CONFIGS = {
    # Classification Models
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
        'description': 'Women Preference: Small accessories vs Nightwear',
        'category': 'customer_insights',
        'icon': 'fas fa-female',
        'color': 'primary'
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
        'description': 'Customer Behavior Classification',
        'category': 'customer_insights',
        'icon': 'fas fa-users',
        'color': 'info'
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
        'description': 'Customer Spending Level Prediction',
        'category': 'customer_insights',
        'icon': 'fas fa-wallet',
        'color': 'success'
    },

    'classification_high_risk_cancelling': {
        'model_file': 'classification_high_risk_cancelling.pkl',
        'encoders_file': None,
        'scaler_file': 'classification_high_risk_cancelling_scaler.pkl',
        'features': ['total_orders', 'total_cancelled', 'avg_quantity', 'avg_unit_price', 'unique_products', 'total_not_cancelled', 'age', 'gender_male'],
        'cat_features': [],
        'type': 'classification',
        'description': 'High Risk Cancelling Customer Classification',
        'category': 'risk_operations',
        'icon': 'fas fa-user-times',
        'color': 'danger'
    },

    'classification_potential_region': {
        'model_file': 'classification_potential_region.pkl',
        'encoders_file': None,
        'scaler_file': None,
        'features': [
            'age_std', 'age_mean', 'freq_mean', 'freq_std', 'n_customers',
            'rev_norm', 'sub_norm', 'prev_norm', 'freq_consistency',
            'rev_x_prev', 'sub_x_age', 'rev_x_sub'
        ],
        'cat_features': [],
        'type': 'classification',
        'description': 'Potential Region Classification',
        'category': 'risk_operations',
        'icon': 'fas fa-map-marker-alt',
        'color': 'warning'
    },

    # Regression Models
    'future_avg_basket': {
        'model_file': 'future_avg_basket.pkl',
        'encoders_file': None,
        'features': [
            'code_customer', 'hist_total_amount', 'hist_n_purchases', 'hist_avg_basket',
            'Age', 'Overall_review', 'Previous Purchases', 'avg_original_price',
            'avg_quantity', 'future_total_amount', 'future_n_purchases'
        ],
        'cat_features': [],
        'type': 'regression',
        'description': 'Future Average Basket Prediction',
        'category': 'sales_revenue',
        'icon': 'fas fa-shopping-cart',
        'color': 'primary',
        'derived_features': ['hist_total_amount', 'hist_n_purchases', 'hist_avg_basket', 'avg_original_price', 'avg_quantity'],
        'base_features': ['Age', 'Overall_review', 'Previous Purchases', 'Subscription Status', 'Payment Method', 'Frequency of Purchases', 'Preferred_size']
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
        'description': 'Recommended Product Price Prediction',
        'category': 'sales_revenue',
        'icon': 'fas fa-dollar-sign',
        'color': 'success'
    },

    'regression_state_revenue': {
        'model_file': 'regression_state_revenue.pkl',
        'encoders_file': None,
        'scaler_file': 'regression_state_revenue_scaler.pkl',
        'features': ['nb_orders', 'nb_customers', 'avg_basket', 'return_rate_pct', 'avg_age', 'pct_male', 'total_qty_sold'],
        'cat_features': [],
        'type': 'regression',
        'description': 'State Revenue Regression',
        'category': 'sales_revenue',
        'icon': 'fas fa-chart-line',
        'color': 'info'
    },

    'regression_failed_orders': {
        'model_file': 'regression_failed_orders_pct.pkl',
        'encoders_file': None,
        'scaler_file': None,
        'features': ['period_num'],
        'cat_features': [],
        'type': 'regression',
        'description': 'Failed Orders Percentage Prediction',
        'category': 'sales_revenue',
        'icon': 'fas fa-exclamation-triangle',
        'color': 'warning'
    },

    'future_purchases': {
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
        'description': 'Future Purchases Prediction',
        'category': 'risk_operations',
        'icon': 'fas fa-calculator',
        'color': 'secondary'
    },

    # Clustering Models
    'customer_clustering': {
        'model_file': 'clustering_customer_model.pkl',
        'encoders_file': None,
        'scaler_file': 'clustering_customer_scaler.pkl',
        'features_file': 'clustering_customer_features.pkl',
        'features': [
            'total_purchases', 'total_quantity', 'avg_unit_price', 'total_spent',
            'discount_rate', 'customer_lifetime_days', 'purchase_frequency',
            'avg_order_value', 'return_cancel_rate'
        ],
        'cat_features': [],
        'type': 'clustering',
        'description': 'Customer Clustering: 5 shopper segments',
        'category': 'customer_insights',
        'icon': 'fas fa-users-cog',
        'color': 'dark',
        'cluster_names': {
            0: 'Occasional Buyers',
            1: 'Regular Loyalists',
            2: 'Bargain Hunters',
            3: 'VIP Shoppers',
            4: 'Problem Customers'
        }
    }
}

# Navigation categories
NAVIGATION_CATEGORIES = {
    'dashboard_analytics': {
        'name': '📊 Dashboard & Analytics',
        'icon': 'fas fa-tachometer-alt',
        'models': []
    },
    'sales_revenue': {
        'name': '🛒 Sales & Revenue',
        'icon': 'fas fa-shopping-cart',
        'models': ['future_avg_basket', 'recommended_price', 'regression_state_revenue', 'regression_failed_orders']
    },
    'customer_insights': {
        'name': '👥 Customer Insights',
        'icon': 'fas fa-users',
        'models': ['women_preference', 'spending_level', 'classification_customer_behavior', 'customer_clustering']
    },
    'risk_operations': {
        'name': '🎯 Risk & Operations',
        'icon': 'fas fa-exclamation-triangle',
        'models': ['classification_high_risk_cancelling', 'classification_potential_region', 'future_purchases']
    }
}

# Data source configuration
DATA_SOURCES = {
    'sales_data': r"C:\Users\GSI\Desktop\DataWareHouse\Sales.xlsx",
    'customers_data': r"C:\Users\GSI\Desktop\DataWareHouse\Customers_f.xlsx",
    'products_data': r"C:\Users\GSI\Desktop\DataWareHouse\Products_f.xlsx"
}

# Application settings
APP_SETTINGS = {
    'name': 'Fashion Analytics Platform',
    'version': '1.0.0',
    'description': 'AI-powered analytics for fashion industry',
    'author': 'Fashion Analytics Team',
    'year': 2025
}