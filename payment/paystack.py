from django.conf import settings
import requests

class Paystack:
	def __init__(self):
		self.sk = settings.PAYSTACK_SECRET_KEY
		return None
	
	def Initiate_transaction(self, user_email:str, amount:float):
		url = "https://api.paystack.co/transaction/initialize"

		headers = {
			"Authorization": f"Bearer {self.sk}",
			"Content-Type": "application/json"
			}
		data = {
			"email": f"{user_email}",
			"amount": f"{round(amount * 100, 2)}",
			"currency": "NGN",
			"callback_url": "https://dqcmdqv5-8000.uks1.devtunnels.ms/payment/verify"
			}
		response = requests.post(url, headers=headers, json=data)
		return response
	
	def verify_transaction(self, ref_code):
		url = f"https://api.paystack.co/transaction/verify/{ref_code}"
		
		headers = {
			"Authorization": f"Bearer {self.sk}",
			"Content-Type": "application/json"
			}
		response = requests.get(url=url, headers=headers)
		
		if response.status_code == 200:
			response_data = response.json()
			return response_data
		return response.json()
            
    

    