import logging
from .clients import w3, clob

log = logging.getLogger("PolyCopy.health")


def check_health():
    """Check health of RPC and CLOB connections"""
    try:
        # Check CLOB connection
        clob.get_markets()
        clob_ok = True
    except Exception as e:
        log.debug(f"CLOB health check: {e}")
        clob_ok = False

    rpc_ok = w3.is_connected()

    if not rpc_ok:
        log.debug("RPC connection check failed")

    status = "healthy" if (rpc_ok and clob_ok) else "degraded" if (rpc_ok or clob_ok) else "error"

    return {
        "status": status,
        "rpc_connected": rpc_ok,
        "clob_ok": clob_ok
    }
