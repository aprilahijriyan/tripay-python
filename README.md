# tripay

Tripay Client For Python (UNOFFICIAL)

Support:

* Sandbox & Production Mode
* Get Payment Instruction
* Fee Calculator
* Get Payment Channels
* Closed Payment

    * Helper to make order items
    * Automatic signature generation
    * Request payment
    * Detail transaction
    * List transaction

* Open Payment

    * Automatic signature generation
    * Request payment
    * Detail transaction
    * List transaction

* Easy to use

# Usage

Setup client:

```python
from tripay import TriPay

tripay = TriPay(
    api_key="DEV-xxx",
    merchant_code="xxx",
    merchant_private_key="xxx",
    debug=True # sandbox mode
)
```

Get Payment Instruction:

```python
tripay.get_payment_instruction("BRIVA").json()
```

Fee Calculator:

```python
tripay.fee_calculator(5000).json()
```

Get Payment Channels:

```python
tripay.get_payment_channel().json()
```

Closed Payment:

```python
# access to closed payments
cp = tripay.closed_payment

# creating items
items = []
items.append(
    cp.create_item(
        sku="099999888",
        name="sabun",
        price=2500,
        quantity=10
    )
)

# request payment
resp = cp.request(
    "BRIVA",
    2500 * 10,
    customer_name="Dadang",
    customer_email="someone@test.com",
    customer_phone="0899988234",
    order_items=items
).json()
print(resp)
```

Open Payment:

```python
# notes: for open payments currently does not support sandbox mode
tripay.debug = False

# access to open payments
op = tripay.open_payment

# request payment
resp = op.request("BCAVA").json()
print(resp)
```
