from pydantic import BaseModel, ConfigDict, field_validator
from dotenv import load_dotenv
import os
import sys
from typing import List
from pathlib import Path

# Load .env from project root
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
load_dotenv(env_file)

# Extract values from environment
_private_key = os.getenv("PRIVATE_KEY") or os.getenv("private_key")
_user_addresses_str = os.getenv("USER_ADDRESSES") or os.getenv("user_addresses")
_rpc_url = os.getenv("RPC_URL") or os.getenv("rpc_url") or "https://polygon-rpc.com"
_trade_multiplier = os.getenv("TRADE_MULTIPLIER") or os.getenv("trade_multiplier") or "1.0"
_fetch_interval = os.getenv("FETCH_INTERVAL") or os.getenv("fetch_interval") or "2.0"
_slippage_tolerance = os.getenv("SLIPPAGE_TOLERANCE_PCT") or os.getenv("slippage_tolerance_pct") or "1.5"
_min_order = os.getenv("MIN_ORDER_SIZE_USD") or os.getenv("min_order_size_usd") or "5.0"
_max_order = os.getenv("MAX_ORDER_SIZE_USD") or os.getenv("max_order_size_usd") or "10000.0"
_dry_run = os.getenv("DRY_RUN") or os.getenv("dry_run") or "true"
_state_file = os.getenv("STATE_FILE") or os.getenv("state_file") or "data/positions.json"
_log_level = os.getenv("LOG_LEVEL") or os.getenv("log_level") or "INFO"
_retry_attempts = os.getenv("RETRY_ATTEMPTS") or os.getenv("retry_attempts") or "3"
_retry_delay = os.getenv("RETRY_DELAY") or os.getenv("retry_delay") or "2.0"

# Parse user addresses
def _parse_user_addresses(addresses_str):
    if not addresses_str:
        return []
    if isinstance(addresses_str, list):
        return [a.strip().lower() for a in addresses_str if a.strip()]
    return [a.strip().lower() for a in addresses_str.split(",") if a.strip()]


class AppConfig(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    private_key: str
    user_addresses: List[str]
    rpc_url: str = "https://polygon-rpc.com"
    trade_multiplier: float = 1.0
    fetch_interval: float = 2.0
    slippage_tolerance_pct: float = 1.5
    min_order_size_usd: float = 5.0
    max_order_size_usd: float = 10000.0
    dry_run: bool = True
    state_file: str = "data/positions.json"
    log_level: str = "INFO"
    retry_attempts: int = 3
    retry_delay: float = 2.0

    @field_validator("trade_multiplier")
    @classmethod
    def validate_multiplier(cls, v):
        if not (0.01 <= v <= 100):
            raise ValueError("trade_multiplier must be between 0.01 and 100")
        return v

    @field_validator("fetch_interval")
    @classmethod
    def validate_fetch_interval(cls, v):
        if v <= 0.5:
            raise ValueError("fetch_interval must be > 0.5")
        return v

    @field_validator("slippage_tolerance_pct")
    @classmethod
    def validate_slippage(cls, v):
        if v < 0:
            raise ValueError("slippage_tolerance_pct cannot be negative")
        return v

    @field_validator("min_order_size_usd")
    @classmethod
    def validate_min_order(cls, v):
        if v < 1:
            raise ValueError("min_order_size_usd must be >= 1")
        return v

    @field_validator("max_order_size_usd")
    @classmethod
    def validate_max_order(cls, v):
        if v < 100:
            raise ValueError("max_order_size_usd must be >= 100")
        return v


# Initialize config with error handling
try:
    # Parse dry_run as boolean
    dry_run_bool = _dry_run.lower() in ('true', '1', 'yes') if isinstance(_dry_run, str) else bool(_dry_run)
    
    CONFIG = AppConfig(
        private_key=_private_key or "",
        user_addresses=_parse_user_addresses(_user_addresses_str) or [],
        rpc_url=_rpc_url,
        trade_multiplier=float(_trade_multiplier),
        fetch_interval=float(_fetch_interval),
        slippage_tolerance_pct=float(_slippage_tolerance),
        min_order_size_usd=float(_min_order),
        max_order_size_usd=float(_max_order),
        dry_run=dry_run_bool,
        state_file=_state_file,
        log_level=_log_level.upper(),
        retry_attempts=int(_retry_attempts),
        retry_delay=float(_retry_delay),
    )
    
    # Validate required fields
    if not CONFIG.private_key:
        raise ValueError("PRIVATE_KEY is required")
    if not CONFIG.user_addresses:
        raise ValueError("USER_ADDRESSES is required")
        
except Exception as e:
    print(f"❌ Configuration Error: {e}")
    print("\nPlease make sure .env file exists with required variables:")
    print("  - PRIVATE_KEY (required)")
    print("  - USER_ADDRESSES (required)")
    print("\nRun: cp .env.example .env && edit .env")
    sys.exit(1)
