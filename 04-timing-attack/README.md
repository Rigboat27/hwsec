# Timing attack

`timing_oracle.py` is the target from the lab. It checks a guess against the stored password character by character and stops at the first mismatch. The `timing` value it returns is how far it got, which is what a real early-exit compare leaks through execution time.

`attack.py` recovers the password one position at a time. At position k, the right character is the only one that makes the check get past k. That takes at most |charset| × length queries.

```
$ python attack.py
password : tru5t_L4b!
queries  : 386
brute    : 94^10 = 5.39e+19 guesses in the worst case
```

(If there's no `password.txt`, it writes a demo one first.)

The fix is a compare that always touches every byte and folds the differences together, so the running time doesn't depend on where the first mismatch is. Python's `hmac.compare_digest` does this.
