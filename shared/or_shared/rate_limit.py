import time
def token_bucket_allow(redis, key, capacity, refill_per_sec):
    now = time.time()
    pipe = redis.pipeline()
    pipe.hget(key, "tokens")
    pipe.hget(key, "ts")
    tokens_s, ts_s = pipe.execute()
    tokens = float(tokens_s) if tokens_s is not None else float(capacity)
    ts = float(ts_s) if ts_s is not None else now
    elapsed = max(0.0, now - ts)
    tokens = min(float(capacity), tokens + elapsed * refill_per_sec)
    allowed = tokens >= 1.0
    if allowed:
        tokens -= 1.0
    pipe = redis.pipeline()
    pipe.hset(key, mapping={"tokens": tokens, "ts": now})
    pipe.expire(key, int(max(60, capacity / max(refill_per_sec, 1e-6))))
    pipe.execute()
    return allowed
