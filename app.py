from flask import Flask, request, jsonify, render_template
import stripe
import joblib
import numpy as np
import pandas as pd
import os
app = Flask(__name__)
#dp_1QNpwJKv4WkeqP3163iwB43C
def format_string(text):
    words = text.split()
    if len(words) <= 2:
        # Capitalize the first letter of the entire text
        return text.capitalize()
    else:
        # Capitalize the first letter of each word
        return ' '.join(word.capitalize() for word in words)


# Configure Stripe with your API key
stripe.api_key = "sk_test_51QKvXIKv4WkeqP31vUXoXcYlAhYFemNfiGkLFfJAnaN7EsJu9B4Qt2KzB7GHDVADDugGSRRJIVhZnGWP8fwcUF2H00O8T0QzCO"

# Construct the absolute path to the .pkl file
current_dir = os.path.dirname(os.path.abspath(__file__))
encoder_path = os.path.join(current_dir, 'dynamic_encoders.pkl')

try:
    encoder = joblib.load(encoder_path)
    joblib.dump(encoder, "dynamic_encoders_py312.pkl", protocol=4)
except FileNotFoundError:
    print(f"Error: The file 'dynamic_encoders.pkl' was not found at {encoder_path}")
    # Handle the error appropriately, e.g., exit or raise
    raise
except Exception as e:
    print(f"Error loading 'dynamic_encoders.pkl': {e}")
    # Handle other unpickling errors
    raise

model = joblib.load('cc_tuned.pkl')
@app.route('/')
def home():
    # Read countries from countries.txt and convert it to a list
    countries = []
    with open('all.txt', 'r') as file:
        for line in file.readlines():
            # Split the line by comma and strip whitespace characters
           #
            country_name, country_code = line.strip().split(',')
            countries.append((country_name, country_code))

    return render_template('payment_form.html',countries=countries)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Get the Stripe token from the form    
    token = request.form['stripeToken']
    name=request.form['full_name']
    # Get other form fields
    billing_address_line1=request.form['billing_address_line1']
    billing_address_line2=request.form['billing_address_line2']
    country=request.form['country']
    city=request.form['city']
    state=request.form['state']
    postal_code=request.form['postal_code']
    currency=request.form['Currency']
    price=request.form['price']
    name=request.form['full_name']

    # Create a payment method using the token
    try:
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={"token": token},
            billing_details={
                "address":  {
                    "line1":  billing_address_line1,
                    "line2":  billing_address_line2,  # Optional
                    "city": city,
                    "state": state,
                    "postal_code":postal_code,
                    "country": country
                },
                "name":name,
            }
        )

        # Create a payment intent with return_url to handle redirects
        intent = stripe.PaymentIntent.create(
            amount= price,  # Example amount in cents (e.g., $50.00)
            currency=currency,
            payment_method=payment_method.id,
            confirm=True,
            # Add a return URL for the customer to be redirected after completing the payment
            return_url="http://127.0.0.1:5000/process_payment", # Replace with your actual return URL
        )
        print(intent)
        payment_intent=intent
        charge = stripe.Charge.retrieve(intent.latest_charge)
        print(charge)
        print(intent)
        fraud_report=6
        if charge['disputed']:
            print("Charge is disputed.")
            dispute_id = charge['dispute']
            print("Dispute ID:", dispute_id)
            dispute = stripe.Dispute.retrieve(dispute_id)
            print("Dispute Details:", dispute.reason)
            fraud_report = format_string(dispute.reason)
        

        # You can access details from the Payment Intent or Charge object
        
        print("Payment successful!")
#['amount', 'currency', 'created', 'captured', 'status', 'city', 'country', 'state', 'postal_code', 'card_brand', 'last4', 'exp_month', 'exp_year', 'cvc_check', 'risk_level', 'risk_score', 'network_status', 'seller_message', 'fraud_reason']
        transaction_details = {
            "amount": payment_intent.amount,
            "currency": payment_intent.currency ,  # Amount in the correct currency unit
            "created": payment_intent.created,
            "captured": charge.captured,
            "status": charge.status,
            "city": charge.billing_details.address.city ,
            "country": charge.billing_details.address.country,
            "state": charge.billing_details.address.state,
            "postal_code": charge.billing_details.address.postal_code,
            "card_brand": charge.payment_method_details.card.brand,
            "last4":charge.payment_method_details.card.last4,
            "exp_month":charge.payment_method_details.card.exp_month,
            "exp_year":charge.payment_method_details.card.exp_year,
            "cvc_check":charge.payment_method_details.card.checks.cvc_check,
            "risk_level":charge.outcome.risk_level,
            "risk_score":charge.outcome.risk_score,
            "network_status":charge.outcome.network_status,
            "seller_message":charge.outcome.seller_message,
            "fraud_reason":fraud_report,
        }
        encoded_features = []
        encoders = joblib.load('dynamic_encoders.pkl')
        for feature in ['currency','captured','status', 'city', 'country', 'state', 'card_brand','cvc_check','risk_level','network_status', 'seller_message', 'fraud_reason']:
            print(feature)
            try:
                encoder = encoders[feature]
                encoded = encoder.transform([transaction_details[feature]])
                encoded_features.append(encoded)
            except KeyError:
                print(f"Encoder for feature '{feature}' not found in the saved encoders.")
            except Exception as e:
                print(f"Error encoding feature '{feature}': {e}")# or encoder.transform(transaction_details[feature])
        print(encoded_features)
        encoded_features = np.concatenate(encoded_features).reshape(1, -1)
        print(f"Encoded features: {encoded_features}")
        try:
            fraud_reason=encoded_features[0][11]
        except Exception as e:
            fraud_reason=6
            
        columns=['amount','currency','created','captured','status','city','country','state','postal_code','card_brand','exp_month','exp_year','cvc_check','risk_level','risk_score',	'network_status','seller_message','fraud_reason']
        transaction_encoded={
            "amount": payment_intent.amount,
            "currency": encoded_features[0][0] ,  # Amount in the correct currency unit
            "created": payment_intent.created,
            "captured": encoded_features[0][1],
            "status":encoded_features[0][2],
            "city": encoded_features[0][3] ,
            "country":encoded_features[0][4],
            "state": encoded_features[0][5],
            "postal_code": charge.billing_details.address.postal_code,
            "card_brand":encoded_features[0][6],
            "exp_month":charge.payment_method_details.card.exp_month,
            "exp_year":charge.payment_method_details.card.exp_year,
            "cvc_check":encoded_features[0][7],
            "risk_level":encoded_features[0][8],
            "risk_score":charge.outcome.risk_score,
            "network_status":encoded_features[0][9],
            "seller_message":encoded_features[0][10],
            "fraud_reason":fraud_reason,
        }

        df_features = pd.DataFrame([transaction_encoded],columns=columns)
        print(model.feature_names_in_)  # If using a Scikit-learn model


        # 5. Make the prediction using the saved model
        prediction = model.predict(df_features)
        probability = model.predict_proba(df_features)[0][0]  # Fraud probability
        print(model.predict_proba(df_features)[0][0])
        print(model.predict_proba(df_features)[0][1])
        percentage = probability * 100
        # 6. Output the prediction
        print(f"Prediction: {prediction}")
        if prediction==1:
            fraud=" NO"
        else:
            stripe.Refund.create(
            intent.latest_charge,
            reason="fraudulent"
            )
            stripe.Charge.modify(
            intent.latest_charge,
            metadata={
                "fraud_probability": f"{percentage:.2f}%",
                "is_fraud": probability > 0.7
            }
            )
            fraud=" YES"

        return render_template('payment_form.html', payment_status="Payment successful!",fraud=fraud,reciept=charge.receipt_url)

    except stripe.error.CardError as e:
        print(e)
        print(e.user_message)
        return render_template('payment_form.html', payment_status=f"Payment declined: {e.user_message}",fraud='Yes',reciept="/payment_form.html")

if __name__ == "__main__":
    app.run(debug=True)
