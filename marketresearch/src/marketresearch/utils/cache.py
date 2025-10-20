import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional

class SimpleCache:
    def __init__(self, cache_dir: str = "./cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        cache_file = self.cache_dir / f"{self._get_cache_key(key)}.json"
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)
            
            # Check if expired
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                cache_file.unlink()
                return None
            
            return cached['data']
        except:
            return None
    
    def set(self, key: str, data: Any):
        cache_file = self.cache_dir / f"{self._get_cache_key(key)}.json"
        cached_data = {
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cached_data, f)

# Global cache instance
research_cache = SimpleCache()