import psycopg
from dataclasses import dataclass, astuple

DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/postgres"  # local demo DB


@dataclass
class RequestCost:  # one row per request, field order = column order
    request_id: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    steps: int = 0
    wall_ms: int = 0
    terminal_state: str = "error"  # assume the worst until the loop proves otherwise


def write_row(rc: RequestCost) -> None:
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            "INSERT INTO request_cost VALUES (%s, %s, %s, %s, %s, %s, %s)", astuple(rc)
        )
