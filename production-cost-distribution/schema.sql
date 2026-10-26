CREATE TABLE request_cost (
    request_id     text PRIMARY KEY,
    model          text,
    input_tokens   int,
    output_tokens  int,
    steps          int,
    wall_ms        int,
    terminal_state text,
    created_at     timestamptz DEFAULT now()
);