import logging
import time
from typing import List, Dict, Any
from .config import CONFIG
from .executor import place_order
from .tracker import tracker
from .stats import record_trade
from .balance import check_sufficient_balance

log = logging.getLogger("PolyCopy.copier")


def fetch_user_trades(user_address: str) -> List[Dict[str, Any]]:
    """Fetch trades from monitored user"""
    # This would connect to Telegram/API to get user trades
    # For now, returning empty list as placeholder
    log.debug(f"Fetching trades for {user_address}")
    return []


def scale_order_size(original_size: float) -> float:
    """Scale order size according to multiplier and limits"""
    scaled = original_size * CONFIG.trade_multiplier
    scaled = max(scaled, CONFIG.min_order_size_usd)
    scaled = min(scaled, CONFIG.max_order_size_usd)
    return scaled


def check_position_exists(market_id: str, side: str) -> bool:
    """Check if we already have a position in this market"""
    position = tracker.get_position(market_id)
    return position.get("side") == side


def execute_copy_trade(market_id: str, token_id: str, side: str, original_size: float, price: float) -> bool:
    """Execute a copy trade"""
    
    # Check if sufficient balance
    scaled_size = scale_order_size(original_size)
    if not check_sufficient_balance(scaled_size):
        log.warning(f"Insufficient balance for {market_id}: need ${scaled_size:.2f}")
        return False

    # Check existing position
    if check_position_exists(market_id, side):
        log.info(f"Position already exists for {market_id} {side}, skipping")
        return False

    # Place the order
    success = place_order(token_id, side, scaled_size, price)
    
    if success:
        record_trade(token_id, scaled_size)
        tracker.set_position(market_id, {
            "side": side,
            "size": scaled_size,
            "price": price,
            "timestamp": time.time(),
            "token_id": token_id
        })
        log.info(f"Copy trade executed: {market_id} {side} {scaled_size:.4f} @ {price:.6f}")
        return True
    
    return False


def process_trades(trades: List[Dict[str, Any]]):
    """Process batch of trades"""
    for i, trade in enumerate(trades, 1):
        try:
            log.info(f"   [{i}/{len(trades)}] Processing: {trade.get('market_id', 'UNKNOWN')}")
            execute_copy_trade(
                market_id=trade["market_id"],
                token_id=trade["token_id"],
                side=trade["side"],
                original_size=trade["size"],
                price=trade.get("price", 0.5)
            )
        except Exception as e:
            log.error(f"Failed to process trade {trade}: {e}")
            continue
