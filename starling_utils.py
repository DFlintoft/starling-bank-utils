from starling_api_tokens import token, accountUid
import requests


class StarlingTools:
    def __init__(self):
        self.api_endpoint = "https://api.starlingbank.com/api/v2/account"
        self.token = token
        self.accountID = accountUid
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        r = requests.get(f"{self.api_endpoint}s", headers=self.headers)
        if r == 200:
            print("Starling connection successful")
        else:
            self.__api_test(r)

    def __api_test(self, http_status: int):
        if http_status == 200:
            pass
        elif http_status == 401:
            raise ValueError("Invalid token provided")
        elif http_status == 403:
            raise ValueError(
                "Token provided is expired or request is outside of token's resource scope")
        else:
            raise ValueError(f"Error occured during handling of request: {http_status}")

    def get_account_balance(self):
        r = requests.get(
            f"{self.api_endpoint}s/{self.accountID}/balance", headers=self.headers)
        data = r.json()
        return {
            "main_balance (£)": data["effectiveBalance"]["minorUnits"] / 100,
            "total_funds (£)": data["totalEffectiveBalance"]["minorUnits"] / 100
        }

    def get_spaces_balance(self):
        r = requests.get(
            f"{self.api_endpoint}/{self.accountID}/spaces", headers=self.headers)
        data = r.json()
        return {f"{space['name']} (£)": f"{space['totalSaved']['minorUnits'] / 100}" for space in data["savingsGoals"]}
