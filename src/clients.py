import logging
from web3 import Web3
from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON
from .config import CONFIG

log = logging.getLogger("PolyCopy.clients")

# Web3 setup
try:
    w3 = Web3(Web3.HTTPProvider(CONFIG.rpc_url))
    if not w3.is_connected():
        log.warning(f"RPC not responding at {CONFIG.rpc_url}")
    account = w3.eth.account.from_key("0x" + CONFIG.private_key.lstrip("0x"))
    MY_ADDRESS = account.address.lower()
    log.info(f"Wallet initialized: {MY_ADDRESS}")
except ValueError as e:
    log.error(f"Invalid private key: {e}")
    raise
except Exception as e:
    log.error(f"Failed to initialize Web3: {e}")
    raise

# CLOB client setup
try:
    clob = ClobClient(
        host="https://clob.polymarket.com",
        key=CONFIG.private_key,
        chain_id=POLYGON,
        signature_type=1,
    )
    log.info("CLOB client initialized")
except Exception as e:
    log.error(f"Failed to initialize CLOB client: {e}")
    raise
