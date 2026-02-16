import logging
from .clients import w3, MY_ADDRESS, clob

log = logging.getLogger("PolyCopy.balance")


def get_usdc_balance() -> float:
    """Get USDC balance from wallet"""
    try:
        # USDC on Polygon mainnet
        usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9B1F9F033e5"
        # Simple balance check (would need ABI for full implementation)
        return 0.0
    except Exception as e:
        log.error(f"Failed to get USDC balance: {e}")
        return 0.0


def get_polymarket_balance() -> dict:
    """Get balance info from Polymarket"""
    try:
        balance_info = clob.get_balance()
        return balance_info
    except Exception as e:
        log.error(f"Failed to get Polymarket balance: {e}")
        return {}


def check_sufficient_balance(amount_usd: float) -> bool:
    """Check if we have sufficient balance"""
    try:
        balance = get_polymarket_balance()
        available = float(balance.get("balance", 0))
        return available >= amount_usd
    except Exception as e:
        log.error(f"Balance check failed: {e}")
        return False
