# LoLMaster

LoLMaster is a wrapper for Riot API.

## Requirements

Python version 3.6 or higher

```pip install pandas schedule requests```

## Configuration

You should initialize your API key and the target region by:

```python config.py -k KEY -r REGION```

---

You can also set API key and region by importing ```LolMaster.config```.

```Python
from api import config
config.set_key('RGAPI-...')
config.set_region('kr')
```

## Collecting high elo data
```p
python collect_high_elo_match.py -s SUMMONER_DIR -m MATCH_DIR
```
