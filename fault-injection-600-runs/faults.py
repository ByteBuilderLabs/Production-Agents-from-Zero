import time

MODES = ["none", "exception", "malformed", "empty", "slow", "truncated", "poisoned"]
REPLACE = {"malformed": '{"total_usd": 250.0', "empty": "{}"}
MAX_TOKENS = {"truncated": 8}
SLOW_SECONDS = 30


def wrap(call_tool, mode):
    def wrapped(name, arg):
        if mode == "exception":
            raise RuntimeError("upstream tool returned 503")
        if mode == "slow":
            time.sleep(SLOW_SECONDS)
        if mode in REPLACE:
            return REPLACE[mode]
        return call_tool(name, arg)

    return wrapped
