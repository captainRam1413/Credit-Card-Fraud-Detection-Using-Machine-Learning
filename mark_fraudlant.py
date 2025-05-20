import stripe

stripe.api_key = "sk_test_51QKvXIKv4WkeqP31vUXoXcYlAhYFemNfiGkLFfJAnaN7EsJu9B4Qt2KzB7GHDVADDugGSRRJIVhZnGWP8fwcUF2H00O8T0QzCO"  # Replace with your secret key

charge_id = "ch_3QNreJKv4WkeqP312A1wxmGd"  # Replace with the actual charge ID

# Retrieve the charge
charge = stripe.Charge.retrieve(charge_id)
print(charge)
stripe.Charge.modify(
    charge_id,
    metadata={
        "fraud_status": "Flagged by AI Model",
        "fraud_score": "85",
    }
)

# Check if the charge is disputed
if charge['disputed']:
    print("Charge is disputed.")
    dispute_id = charge['dispute']
    print("Dispute ID:", dispute_id)
    dispute = stripe.Dispute.retrieve(dispute_id)
    print("Dispute Details:", dispute.reason)
else:
    stripe.Refund.create(
    charge=charge_id,
    reason="fraudulent"
    )
    stripe.Charge.modify(
    charge_id,
    metadata={
        "fraud_status": "Flagged by AI Model",
        "fraud_score": "85",
    }
    )

    print("Charge is not disputed.")
