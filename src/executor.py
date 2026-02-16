import logging
from py_clob_client.clob_types import OrderArgs, OrderType
from .clients import clob
from .utils import clob_retry
from .config import CONFIG

log = logging.getLogger("PolyCopy.executor")


@clob_retry
def place_order(token_id: str, side_str: str, size: float, price: float) -> bool:
    """Place an order on Polymarket"""
    # Convert side string to constant (BUY or SELL)
    side = side_str.upper() if side_str.upper() in ('BUY', 'SELL') else 'BUY'

    order_args = OrderArgs(
        token_id=token_id,
        price=price,
        size=size,
        side=side,
        type=OrderType.LIMIT,
    )

    if CONFIG.dry_run:
        log.info(f"[DRY] Would place {side} {size:.4f} @ {price:.6f}")
        return True

    try:
        signed = clob.create_and_sign_order(order_args)
        resp = clob.post_order(signed)

        if "orderID" in resp:
            log.info(f"Order placed → ID: {resp['orderID']}")
            return True
        else:
            log.warning(f"Order failed: {resp}")
            return False
    except Exception as e:
        log.error(f"Order placement error: {e}")
        raise
