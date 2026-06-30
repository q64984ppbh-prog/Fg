# other 
import asyncio
from data.config import client, url_bot
import requests
from config_reader import config

XROCKET_URL = "https://pay.xrocket.tg"

async def create_invoice(amount, asset):
    try:
        invoice = await client.create_invoice(
            amount=amount,
            asset=asset,
            description=f'💸 Пополнение баланса DuckWIN!',
            allow_anonymous=False,
            expires_in=300
        )
        return invoice
    except Exception as e:
        return None
    
async def check_invoice(invoice_id):
    try:
        invoices = await client.get_invoices()
        
        for invoice in invoices:
            if invoice.invoice_id == invoice_id:
                return {
                    'invoice_id': invoice.invoice_id,
                    'status': invoice.status,
                    'comment': invoice.comment
                }
                
        return None

    except Exception as e:
        return None
    
async def check_date_proverka(invoice_id):
    try:
        while True:
            invoice_status = await check_invoice(invoice_id)
            if invoice_status['status'] == 'paid':         
                return True
            
            elif invoice_status['status'] == 'expired':
                return False
            
            else:
                await asyncio.sleep(10)
    except Exception as e:
        pass

def create_xrocket_invoice(
    amount: float,
    payload: str,
):
    CREATE_INVOICE_URL = f"{XROCKET_URL}/tg-invoices"

    headers = {
        "Rocket-Pay-Key": f'{config.xrocket_token.get_secret_value()}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


    body = {
        "amount": amount,
        "currency": "USDT",
        "numPayments": 1,
        "description": "💸 Пополнение баланса Duck WIN!",
        "expiredIn": 300,
        "commentsEnabled": False,
        "payload": payload,
        "callbackUrl": url_bot,
    }

    try:
        response = requests.post(
            CREATE_INVOICE_URL,
            headers=headers,
            json=body,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            return None

        return data["data"]

    except requests.RequestException as e:
        print(e)
        return None

    except Exception as e:
        print(e)
        return None


def check_invoice_xrocket(invoice_id: int):
    url = f"{XROCKET_URL}/tg-invoices/{invoice_id}"

    headers = {
        "Rocket-Pay-Key": f'{config.xrocket_token.get_secret_value()}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()
        if not data.get("success"):
            return None

        invoice = data["data"]

        return {
            "invoice_id": invoice["id"],
            "status": invoice["status"],
            "comment": (
                invoice.get("payments", [{}])[-1].get("comment")
                if invoice.get("payments")
                else None
            ),
        }

    except Exception as e:
        return None
    
async def check_date_proverka_xrocket(
    invoice_id: int,
    sleep_time: int = 10
) -> bool:
    try:
        while True:
            invoice_status = check_invoice_xrocket(invoice_id)

            if not invoice_status:
                await asyncio.sleep(sleep_time)
                continue

            if invoice_status["status"] == "paid":
                return True

            if invoice_status["status"] == "expired":
                return False

            await asyncio.sleep(sleep_time)

    except Exception as e:
        return False