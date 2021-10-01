import hashlib
import hmac

import requests

from ..constants import (
    O_PAYMENT_DETAIL_TRANSACTION_PATH,
    O_PAYMENT_LIST_TRANSACTION_PATH,
    O_REQUEST_TRANSACTION_PATH,
)


class OpenPayment:
    def __init__(self, client) -> None:
        self.client = client

    def create_signature(self, channel: str, merchant_ref: str = None):
        merchant_ref = merchant_ref or ""
        signStr = "{}{}{}".format(self.client.merchant_code, channel, merchant_ref)
        signature = hmac.new(
            bytes(self.client.merchant_private_key, "latin-1"),
            bytes(signStr, "latin-1"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def request(
        self, method: str, merchant_ref: str = None, customer_name: str = None
    ) -> requests.Response:
        data = {"method": method}
        if merchant_ref:
            data["merchant_ref"] = merchant_ref

        signature = self.create_signature(method, merchant_ref)
        data["signature"] = signature

        if customer_name:
            data["customer_name"] = customer_name

        resp = self.client.api("POST", O_REQUEST_TRANSACTION_PATH, data=data)
        return resp

    def detail_transaction(self, uuid: str) -> requests.Response:
        path = O_PAYMENT_DETAIL_TRANSACTION_PATH.format(uuid=uuid)
        resp = self.client.api("GET", path)
        return resp

    def get_transaction(
        self,
        uuid: str,
        reference: str = None,
        merchant_ref: str = None,
        start_date: str = None,
        end_date: str = None,
        per_page: int = None,
    ) -> requests.Response:
        path = O_PAYMENT_LIST_TRANSACTION_PATH.format(uuid=uuid)
        params = {}
        if reference:
            params["reference"] = reference

        if merchant_ref:
            params["merchant_ref"] = merchant_ref

        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        if per_page:
            params["per_page"] = per_page

        resp = self.client.api("GET", path)
        return resp
