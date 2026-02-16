# Advanced Polymarket Copy Bot

Automated trading bot that replicates trades from monitored Telegram users on Polymarket.

## Features

- 🤖 **Automated Trade Copying** - Real-time replication of trades from monitored users
- 🏖️ **Dry Run Mode** - Test without risking real money
- 💾 **State Persistence** - Automatic JSON-based state tracking
- 🔄 **Retry Logic** - Robust error handling with tenacity
- 📊 **Trade Statistics** - Track trades, volumes, and PnL
- 💪 **Health Checks** - Monitor RPC and CLOB connection health
- 🔐 **Secure Config** - Environment-based configuration with Pydantic validation

## Project Structure

```

## Installation

1. **Clone or create the project:**
   ```bash
   cd textpolymarket-copy-bot-advanced
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Set up data directory:**
   ```bash
   mkdir -p data
   ```

## Configuration

Edit `.env` with the following variables:

### Required
- `PRIVATE_KEY` - Your private key (without 0x prefix)
- `USER_ADDRESSES` - Comma-separated list of addresses to monitor

### Optional (with defaults)
- `RPC_URL` - Polygon RPC endpoint (default: polygon-rpc.com)
- `TRADE_MULTIPLIER` - Size multiplier (0.01-10.0, default: 1.0)
- `FETCH_INTERVAL` - Polling interval in seconds (default: 2.0)
- `SLIPPAGE_TOLERANCE_PCT` - Slippage tolerance % (default: 1.5)
- `MIN_ORDER_SIZE_USD` - Minimum order size (default: 5.0)
- `MAX_ORDER_SIZE_USD` - Maximum order size (default: 10000.0)
- `DRY_RUN` - Test mode without real trades (default: true)
- `STATE_FILE` - State persistence file (default: data/positions.json)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
- `RETRY_ATTEMPTS` - Number of retry attempts (default: 3)
- `RETRY_DELAY` - Delay between retries in seconds (default: 2.0)

## Usage

### Run the bot

```bash
python run.py
```

### With custom environment

```bash
python -m src.main
```

### Using environment variables

```bash
export PRIVATE_KEY=your_key
export USER_ADDRESSES=0xaddr1,0xaddr2
python run.py
```

## Features in Detail

### State Persistence
- Automatically saves all positions to `data/positions.json`
- Survives restarts - resumes from the last known state
- Can be manually edited or cleared

### Order Execution
- **Retry Logic**: Automatically retries failed orders up to `RETRY_ATTEMPTS` times
- **Size Scaling**: Applies multiplier and respects min/max limits
- **Dry Run**: Test orders without placing them (logs instead)

### Health Monitoring
- Periodic RPC and CLOB connection checks
- Graceful degradation on partial failures
- Automatic recovery with exponential backoff

### Trade Tracking
- Real-time statistics per market
- Trade count, total volume, last trade timestamp
- Periodic summary output to console

## Monitoring

The bot outputs detailed logs with:
- Trade execution confirmations
- Position tracking updates
- Health check results
- Error messages with context

Custom log level in `.env`:
```
LOG_LEVEL=DEBUG    # Most verbose
LOG_LEVEL=INFO     # Normal (recommended)
LOG_LEVEL=WARNING  # Only warnings/errors
LOG_LEVEL=ERROR    # Only errors
```

## Error Handling

The bot implements comprehensive error handling:
- **Network errors** → Automatic retry with exponential backoff
- **Insufficient balance** → Skip trade with warning
- **Duplicate positions** → Skip to prevent conflicts
- **Health failures** → Enter safe mode, wait for recovery

## Development

### Adding a new module

1. Create `src/module_name.py`
2. Use proper logging: `log = logging.getLogger("PolyCopy.module_name")`
3. Import CONFIG from config.py for settings
4. Add functions/classes, document with docstrings
5. Import in main.py if needed

### Testing

```bash
# Load configuration
from src.config import CONFIG
print(CONFIG.trade_multiplier)

# Test health check
from src.health import check_health
print(check_health())

# Check state
from src.tracker import tracker
print(tracker.get_all_positions())
```

## Performance Considerations

- **Fetch interval**: Decrease for faster response, increase to reduce API load
- **Trade multiplier**: Lower = less risk, higher = more capital deployment
- **Retry attempts**: More attempts = more resilient, slower failure detection
- **Max order size**: Critical safety limit - prevents catastrophic losses

## Security

⚠️ **Important:**
- Never commit `.env` with real credentials
- Use different keys for testing vs production
- Consider using hardware wallets for production
- Regularly audit `data/positions.json` for accuracy
- Test with `DRY_RUN=true` first

## Troubleshooting

### Bot won't start
```bash
# Check Python version (3.8+)
python --version

# Verify dependencies
pip list | grep -E "web3|pydantic|tenacity"

# Check .env file
cat .env | head -5
```

### Orders not executing
- Check `DRY_RUN` setting - if true, orders are simulated
- Verify wallet balance
- Check CLOB connection health: `LOG_LEVEL=DEBUG`

### State corruption
- Backup `data/positions.json`
- Can safely delete and restart with clean state
- Bot will recreate on next run

## Contributing

Improvements welcome! Areas:
- Real Telegram integration
- WebSocket support for faster updates
- Advanced position management
- Multi-account support
- Dashboard/API

## License

MIT

## Support

For issues or features, create an issue in the repository.

---

**Created**: 2026-02-16
**Version**: 1.0.0
