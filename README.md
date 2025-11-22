# badtrace

CLI to generate OpenTelemetry traces with known "bad patterns". Adding your own patterns is easy.

## Quick Start

```
python app.py \
  --endpoint=http://localhost:4318 \
  --service-name=badtrace \
  --trace-count=1 \
  --insecure=true \
  --scenario=scenario1
```

Note: This tool emits traces via HTTP(S). It is intended to be used with an [OpenTelemetry collector](https://opentelemetry.io/docs/collector)

## Scenarios

### Scenario 1 | Low value trace: too few nodes
<img width="1464" height="361" alt="Screenshot 2025-11-22 at 17 26 49" src="https://github.com/user-attachments/assets/b104dcaa-95ce-4f09-9aff-5721efa8edf7" />

This scenario models a trace with (randomly) between 1 and 3 spans.

A trace this short is unlikely to provide useful information thus should probably be sampled or dropped.
This trace is also very short in terms of end to end time, suggesting it is low value.

```
python app.py \
  --endpoint=http://localhost:4318 \
  --insecure=true \
  --scenario=scenario1
```

### Scenario 2 | Errored trace: Trace contains spans with errors

<img width="1464" height="404" alt="Screenshot 2025-11-22 at 17 29 48" src="https://github.com/user-attachments/assets/0af1d416-eb2e-4375-90ab-cb4a14db433e" />

This scenario models a trace with (randomly) between 5 and 10 spans. Some of the spans will contain errors.

### Scenario 3 | Chatty client with one server

This scenario models one service "serviceA" calling another "https://example.com" service many times.

This signifies a chatty service calling a single endpoint repeatedly.

### Scenario 4 | Chatty client with multiple servers

This scenario models one service "serviceA" calling multiple endpoints many times.

This signifies a client that is chatty to not only one, but multiple endpoints.
