import numpy as np
def sev_from_thresholds(x, t1, t2, t3, higher_worse=True):
    s = np.zeros_like(x, dtype=np.uint8)
    if higher_worse:
        s[(x >= t1) & (x < t2)] = 1
        s[(x >= t2) & (x < t3)] = 2
        s[x >= t3] = 3
    else:
        s[(x < t1) & (x >= t2)] = 1
        s[(x < t2) & (x >= t3)] = 2
        s[x < t3] = 3
    return s
def composite_max(*sevs):
    out = sevs[0].copy()
    for s in sevs[1:]:
        out = np.maximum(out, s)
    return out.astype(np.uint8)
