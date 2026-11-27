# Caching with a hash table: memo and LRU cache

A cache can reuse work, such as a line count for a log segment.

    oldest [db] <-> [api] newest
    dict: db -> node db, api -> node api

The chain is ordered by use. The dict points to nodes in the chain.

**Example.** Hit db. The order becomes api then db. When full, a new key evicts api.

**Common mistake.** A saved zero or None can be a hit. Test for the key.

**Real work.** A server can keep recent results in memory. If source data changes,
it also needs a way to stop using an old result.

**Summary.** Memoization keeps results by input. LRU keeps a fixed number of recent
results. OrderedDict can track key order, and lru_cache can wrap a function.

## Model answer

The dict finds the node for a given key. On a cache hit, I move that node to the newest end. The oldest end gives me the next key to evict.
