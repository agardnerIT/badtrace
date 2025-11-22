# badtrace

CLI to generate OpenTelemetry traces with known "bad patterns". Adding your own patterns is easy.

## Quick Start

```
python app.py \
  --endpoint=http://localhost:4318 \
  --service-name=badtrace \ # optional: defaults to "badtrace"
  --trace-count=1 \ # optional: defaults to 1
  --insecure=true \
  --scenario=scenario1
```

Note: This tool emits traces via HTTP(S). It is intended to be used with an [OpenTelemetry collector](https://opentelemetry.io/docs/collector)

## Scenarios

### Scenario 1 | Low value trace: too few nodes

```python
python app.py \
  --endpoint=http://localhost:4318 \
  --insecure=true \
  --scenario=scenario1
```

<img width="1464" height="361" alt="Screenshot 2025-11-22 at 17 26 49" src="https://github.com/user-attachments/assets/b104dcaa-95ce-4f09-9aff-5721efa8edf7" />

This scenario models a trace with (randomly) between 1 and 3 spans.

A trace this short is unlikely to provide useful information thus should probably be sampled or dropped.
This trace is also very short in terms of end to end time, suggesting it is low value.


### Scenario 2 | Errored trace: Trace contains spans with errors

```python
python app.py \
  --endpoint=http://localhost:4318 \
  --insecure=true \
  --scenario=scenario2
```

<img width="1464" height="404" alt="Screenshot 2025-11-22 at 17 29 48" src="https://github.com/user-attachments/assets/0af1d416-eb2e-4375-90ab-cb4a14db433e" />

This scenario models a trace with (randomly) between 5 and 10 spans. Some of the spans will contain errors.


### Scenario 3 | Chatty client with one server

```python
python app.py \
  --endpoint=http://localhost:4318 \
  --insecure=true \
  --scenario=scenario3
```

<img width="1466" height="429" alt="Screenshot 2025-11-22 at 17 38 12" src="https://github.com/user-attachments/assets/beeaa5ea-a9d5-4e58-be05-813af00056fe" />

This scenario models one service "serviceA" calling another "https://example.com" service many times.

This signifies a chatty service calling a single endpoint repeatedly.

### Scenario 4 | Chatty client with multiple servers

```python
python app.py \
  --endpoint=http://localhost:4318 \
  --insecure=true \
  --scenario=scenario4
```

<img width="1466" height="787" alt="Screenshot 2025-11-22 at 17 41 02" src="https://github.com/user-attachments/assets/b8b6df18-5c5b-478f-ae9f-57dd08092b3c" />

This scenario models one service "serviceA" calling multiple endpoints many times.

This signifies a client that is chatty to not only one, but multiple endpoints.

## Adding Scenarios

Adding scenarios is easy! Either create an issue describing the scenario (we'll need a sample trace in JSON format) or implement it yourself (PRs accepted).

#### Implemenation

Implement 1 function and add an `if` statement.

1. Build your function in scenarios.py which will return a list of spans
2. Add an `if` statement to the `build_spans` function in `utils.py`
