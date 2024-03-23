from dataclasses import dataclass
import mmh3  # pip install mmh3
import numpy as np

@dataclass
class CountMinSketch2:
    tables: int
    buckets: int
        
    def __post_init__(self):
        self.x = np.zeros((self.tables, self.buckets))
    
    def increment(self, x: str) -> None:
        for table_idx in range(self.tables):
            b = self._get_bucket(x=x, table_idx=table_idx)
            self.x[table_idx, b] += 1
    
    def count(self, x: str) -> int:
        return min(
            self.x[table_idx, self._get_bucket(x=x, table_idx=table_idx)]
            for table_idx in range(self.tables)
        )
    
    def _get_bucket(self, x: str, table_idx: int) -> int:
        return mmh3.hash(key=x, seed=table_idx) % self.buckets