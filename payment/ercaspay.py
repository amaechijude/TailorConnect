from django.conf import settings
import requests

class Ercaspay:
    def __init__(self) -> None:
        self.sk = settings.ERCASPAY_SECRET_KEY
        self.base_url = "https://api.ercaspay.com/api/v1"
        return None

    def Initiate_transaction(self, amount:float, payment_reference:str, customer_name:str, customer_email:str,
                                customer_phone:str = None, redirect_url:str=None, descrption:str = None):
        """
        Initiates a payment transaction with the specified details.

        Parameters:
        amount (float): The amount to be charged for the transaction.
        payment_reference (str): A unique reference for the payment transaction.
        customer_name (str): The name of the customer making the payment.
        customer_email (str): The email address of the customer.
        customer_phone (str, optional): The phone number of the customer. Defaults to None.
        redirect_url (str, optional): The URL to redirect the customer after payment. Defaults to None.
        descrption (str, optional): A description of the transaction. Defaults to None.

        Returns:
                HttpsResponse.
        """
        url = f"{self.base_url}/payment/initiate"
        customer_names = customer_name if customer_name else "Firstname Lastname"

        headers = {
            "Authorization": f"Bearer {self.sk}",
            "Content-Type": "application/json"
        }

        json_body = {
            "amount": amount, # mandatory parameter
            "paymentReference": payment_reference, # mandatory parameter
            "paymentMethods": "bank-transfer,ussd", #optional parameter default to those on your dashboard
            "customerName": customer_names, # mandatory parameter
            "customerEmail": customer_email, # mandatory parameter
            "customerPhoneNumber": customer_phone, # optional parameter,
            "redirectUrl": redirect_url, # optional parameter
            "description": descrption, # optional parameter
            "currency": "NGN",
            # "feeBearer": "customer", # optional parameter
            # "metadata": { # optional parameter
            #     "firstname": 
            #     "lastname": 
            #     "email": 
            # }
        }

        response = requests.post(url, headers=headers, json=json_body)
        return response
    

    def Verify_transaction(self, transaction_ref: str) -> bool:
        """
        Verifies a transaction using the provided transaction reference.

        Parameters:
        transaction_ref (str): The unique reference of the transaction to be verified.

        Returns:
        bool: True if the transaction is successfully verified, False otherwise.
        """
        url = f"{self.base_url}/payment/transaction/verify/{transaction_ref}"

        headers = {
            "Authorization": f"Bearer {self.sk}",
            "Content-Type": "application/json"
            }

        response = requests.get(url, headers=headers)

        if response.status_code in [200, 201]:
            output = response.json()
            if output["requestSuccessful"] and output["responseCode"] == "success":
                return True
            return False
        return False