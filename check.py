import stripe

stripe.api_key = "sk_test_51QKvXIKv4WkeqP31vUXoXcYlAhYFemNfiGkLFfJAnaN7EsJu9B4Qt2KzB7GHDVADDugGSRRJIVhZnGWP8fwcUF2H00O8T0QzCO"  # Replace with your secret key

charge_id = "ch_3QNpwIKv4WkeqP312B2UXr3L"  # Replace with the actual charge ID

# Retrieve the charge
charge = stripe.Charge.retrieve(charge_id)

# Check if the charge is disputed
if charge['disputed']:
    print("Charge is disputed.")
    dispute_id = charge['dispute']
    print("Dispute ID:", dispute_id)
    dispute = stripe.Dispute.retrieve(dispute_id)
    print("Dispute Details:", dispute.reason)
else:
    print("Charge is not disputed.")
