from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-sonnet-5"
QUESTION = "What is the total for order A-1042 in EUR?"
EXPECTED = "225.00"

SYSTEM = (
    "You answer questions using tools. Reply with exactly ONE line.\n"
    "Use a tool:  CALL <tool> <argument>\n"
    "Tools:       get_order <order_id>, get_rate <currency_code>\n"
    "To answer:   ANSWER <number to two decimals>\n"
    "If you cannot complete the task: TASK_FAILED"
)


FIXTURE = {"A-1042": 250.00, "EUR": 0.90}


def get_order(order_id):
    return '{"total_usd": %.2f}' % FIXTURE[order_id]


def get_rate(currency):
    return '{"rate": %.2f}' % FIXTURE[currency]


TOOLS = {"get_order": get_order, "get_rate": get_rate}


def call_tool(name, arg):
    return TOOLS[name](arg)


def safe_call(line):
    parts = line.split() + ["", ""]
    try:
        return call_tool(parts[1], parts[2])
    except Exception as e:
        return "tool error: %s" % e


def ask(transcript, max_tokens):
    r = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=SYSTEM,
        messages=[{"role": "user", "content": transcript}],
    )
    return "".join(b.text for b in r.content if b.type == "text")


def run(question, max_tokens=1024):
    log = "Question: " + question
    for _ in range(5):
        text = ask(log + "\n\nYour next line:", max_tokens).strip()
        line = text.splitlines()[0].strip() if text else ""
        if line.startswith("CALL "):
            log += "\n%s\n-> %s" % (line, safe_call(line))
        elif line.startswith("ANSWER"):
            return line[6:].strip() or "TASK_FAILED"
        elif "TASK_FAILED" in line:
            return "TASK_FAILED"
        else:
            log += "\nInvalid reply: %s" % line
    return "TASK_FAILED"
