import hashlib
import hmac
from typing import List

import requests

from ..constants import (
    C_DETAIL_TRANSACTION_PATH,
    C_LIST_TRANSACTION_PATH,
    C_REQUEST_TRANSACTION_PATH,
)


class ClosedPayment:
    def __init__(self, client) -> None:
        self.client = client

    def create_item(self, sku: str, name: str, price: int, quantity: int) -> dict:
        return {
            "sku": sku,
            "name": name,
            "price": price,
            "quantity": quantity,
        }

    def create_signature(self, amount: int, merchant_ref: str = None) -> str:
        merchant_ref = merchant_ref or ""
        signStr = "{}{}{}".format(self.client.merchant_code, merchant_ref, amount)
        signature = hmac.new(
            bytes(self.client.merchant_private_key, "latin-1"),
            bytes(signStr, "latin-1"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def request(
        self,
        method: str,
        amount: int,
        customer_name: str,
        customer_email: str,
        customer_phone: str,
        order_items: List[dict],
        merchant_ref: str = None,
        callback_url: str = None,
        return_url: str = None,
        expired_time: int = None,
    ) -> requests.Response:
        data = {
            "method": method,
            "amount": amount,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
        }
        i = 0
        for item in order_items:
            for k in item:
                data["order_items[" + str(i) + "][" + str(k) + "]"] = item[k]
            i += 1

        if merchant_ref:
            data["merchant_ref"] = merchant_ref

        signature = self.create_signature(amount, merchant_ref)
        data["signature"] = signature

        if callback_url:
            data["callback_url"] = callback_url
        if return_url:
            data["return_url"] = return_url
        if expired_time:
            data["expired_time"] = expired_time

        resp = self.client.api("POST", C_REQUEST_TRANSACTION_PATH, data=data)
        return resp

    def detail_transaction(self, reference: str) -> requests.Response:
        params = {"reference": reference}
        resp = self.client.api("GET", C_DETAIL_TRANSACTION_PATH, params=params)
        return resp

    def get_transaction(
        self,
        page: int = 1,
        per_page: int = 10,
        sort: str = "desc",
        reference: str = None,
        merchant_ref: str = None,
        method: str = None,
        status: str = None,
    ) -> requests.Response:
        params = {}
        if page:
            params["page"] = page

        if per_page:
            params["per_page"] = per_page

        if sort:
            params["sort"] = sort

        if reference:
            params["reference"] = reference

        if merchant_ref:
            params["merchant_ref"] = merchant_ref

        if method:
            params["method"] = method

        if status:
            params["status"] = status

        resp = self.client.api("GET", C_LIST_TRANSACTION_PATH, params=params)
        return resp
