from collections import defaultdict
import time

trade_stats = defaultdict(lambda: {"count": 0, "total_size": 0.0, "last_trade": 0})


def record_trade(token_id: str, size: float):
    """Record a trade in statistics"""
    s = trade_stats[token_id]
    s["count"] += 1
    s["total_size"] += size
    s["last_trade"] = time.time()


def print_summary():
    """Print trading summary"""
    if not trade_stats:
        print("   No trades recorded yet.")
        return
    
    total_trades = sum(s["count"] for s in trade_stats.values())
    total_volume = sum(s["total_size"] for s in trade_stats.values())
    
    print(f"   Total Trades: {total_trades} | Total Volume: ${total_volume:.2f}")
    
    if total_trades > 0:
        print("   ")
        print("   Token Details:")
        for tid, data in trade_stats.items():
            last_time = time.ctime(data['last_trade'])
            print(
                f"   ├─ {tid[:10]}...{tid[-6:]}"
                f" | Trades: {data['count']} | Volume: ${data['total_size']:.2f} | Last: {last_time}"
            )


def get_stats():
    """Get raw stats dictionary"""
    return dict(trade_stats)
