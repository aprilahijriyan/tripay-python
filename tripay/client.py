import requests

from .constants import (
    FEE_CALCULATOR_PATH,
    PAYMENT_CHANNEL_PATH,
    PAYMENT_INSTRUCTION_PATH,
)
from .payment.closed import ClosedPayment
from .payment.open import OpenPayment


class TriPay:
    def __init__(
        self,
        api_key: str,
        merchant_code: str,
        merchant_private_key: str,
        debug: bool = False,
    ) -> None:
        self.api_key = api_key
        self.merchant_code = merchant_code
        self.merchant_private_key = merchant_private_key
        self.debug = debug

    def get_url(self, path: str):
        url = "https://tripay.co.id/api"
        if self.debug:
            url += "-sandbox"

        url += "/" + path.lstrip("/")
        return url

    def api(
        self,
        method: str,
        path: str,
        data: dict = {},
        params: dict = {},
        headers: dict = {},
    ) -> requests.Response:
        url = self.get_url(path)
        headers.update({"Authorization": "Bearer " + self.api_key})
        resp = requests.request(method, url, data=data, params=params, headers=headers)
        return resp

    def get_payment_instruction(
        self,
        code: str,
        pay_code: str = None,
        amount: int = None,
        allow_html: int = None,
    ) -> requests.Response:
        params = {"code": code}

        if pay_code:
            params["pay_code"] = pay_code

        if amount:
            params["amount"] = amount

        if allow_html:
            params["allow_html"] = allow_html

        resp = self.api("GET", PAYMENT_INSTRUCTION_PATH, params=params)
        return resp

    def fee_calculator(self, amount: int, code: str = None) -> requests.Response:
        params = {"amount": amount}
        if code:
            params["code"] = code

        resp = self.api("GET", FEE_CALCULATOR_PATH, params=params)
        return resp

    def get_payment_channel(self, code: str = None) -> requests.Response:
        params = {}
        if code:
            params["code"] = code

        resp = self.api("GET", PAYMENT_CHANNEL_PATH, params=params)
        return resp

    @property
    def closed_payment(self) -> ClosedPayment:
        return ClosedPayment(self)

    @property
    def open_payment(self) -> OpenPayment:
        return OpenPayment(self)
