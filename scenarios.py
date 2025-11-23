import secrets
import time
import random
from loguru import logger
import math

# https://github.com/open-telemetry/opentelemetry-python/blob/546e47b0001b40ca777515325953106e81ed8dbd/opentelemetry-api/src/opentelemetry/trace/status.py#L22
# UNSET = 0
# OK = 1
# ERROR = 2
def get_span_status_int(input):
  if input.lower() == "ok":
    return 1
  if input.lower() == "error":
    return 2
  return 0

# Each span starts at a random time before now()
# Logic below looks convuluted
# But it basically gets the time now then generates
# a random time (converted and rouded to nanoseconds)
# and sets the start time to the past
# This provides some realistic span timings so they're not all just static
def generate_span_start_time():
    random_span_length_temp = random.random()
    span_start_time = time.time_ns()-round(random_span_length_temp*10000000)
    return span_start_time

############################################
#### INDIVIDUAL SCENARIOS
############################################


#### Scenario 1 - Low value trace: too few nodes ####
# This scenario models a trace with (randomly) between 1 and 3 spans
# The idea here is that a trace this short is unlikely to provide useful information
# thus should probably be sampled or dropped
# This trace is also very short in terms of end to end time. Suggesting it is low value
####
def scenario1_span_list(trace_id):
    spans = []

    number_of_spans_to_generate = random.randint(1,3)
    logger.info(f"Will generate {number_of_spans_to_generate} spans for this trace")
    index = 1

    while index <= number_of_spans_to_generate:

        span_start_time = generate_span_start_time()
        span_end_time = time.time_ns()
        
        span = {
                "traceId": trace_id,
                "spanId": secrets.token_hex(8),
                "name": "span",
                "kind": "SPAN_KIND_UNSPECIFIED",
                "start_time_unix_nano": span_start_time,
                "end_time_unix_nano": span_end_time,
                "droppedAttributesCount": 0,
                "attributes": [],
                "events": [],
                "droppedEventsCount": 0,
                "status": {
                    "code": get_span_status_int("OK")
                }
        }
        spans.append(span)
        index += 1

    # Return the spans and signal if you
    # want the span index positions to be appended to span name
    # Recommended value: True
    return spans, True

#### Scenario 2 - Errored trace: Trace contains spans with errors ####
# This scenario models a trace with (randomly) between 5 and 10 spans
# Some of the spans will contain errors
####
def scenario2_span_list(trace_id):
    spans = []

    number_of_spans_to_generate = random.randint(5,10)
    logger.info(f"Will generate {number_of_spans_to_generate} spans for this trace")
    index = 1

    while index <= number_of_spans_to_generate:
        span_start_time = generate_span_start_time()
        span_end_time = time.time_ns()

        span_status_code = 0 # Default to unset
        # 25% chance of it being OK or error
        # if random int is <= 5 then it's an error
        if random.randint(1,20) <= 5:
           span_status_code = get_span_status_int("ERROR")
        else:
           span_status_code = get_span_status_int("OK")
        
        span = {
                "traceId": trace_id,
                "spanId": secrets.token_hex(8),
                "name": "span",
                "kind": "SPAN_KIND_UNSPECIFIED",
                "start_time_unix_nano": span_start_time,
                "end_time_unix_nano": span_end_time,
                "droppedAttributesCount": 0,
                "attributes": [],
                "events": [],
                "droppedEventsCount": 0,
                "status": {
                    "code": span_status_code
                }
        }
        spans.append(span)
        index += 1

    # Return the spans and signal if you
    # want the span index positions to be appended to span name
    # Recommended value: True
    return spans, True

#### Scenario 3 - Chatty service ####
# This scenario models one service "serviceA" calling another "https://example.com" many times
# This signifies a chatty service
####
def scenario3_span_list(trace_id):
    spans = []

    number_of_spans_to_generate = random.randint(5,10)
    logger.info(f"Will generate {number_of_spans_to_generate} spans for this trace")
    index = 1

    while index <= number_of_spans_to_generate:
        span_start_time = generate_span_start_time()
        span_end_time = time.time_ns()
        
        span = {
                "traceId": trace_id,
                "spanId": secrets.token_hex(8),
                "name": "GET https://example.com",
                "kind": "SPAN_KIND_CLIENT",
                "start_time_unix_nano": span_start_time,
                "end_time_unix_nano": span_end_time,
                "droppedAttributesCount": 0,
                "attributes": [{
                    "key": "http.request.method",
                    "value": { "stringValue": "GET" }
                }, {
                    "key": "server.address",
                    "value": { "stringValue": "example.com" }
                }, {
                    "key": "server.port",
                    "value": { "intValue": 443 }
                }, {
                    "key": "url.full",
                    "value": { "stringValue": "https://example.com/serviceB" }
                }],
                "events": [],
                "droppedEventsCount": 0,
                "status": {
                    "code": get_span_status_int("OK")
                }
        }
        spans.append(span)
        index += 1

    # Return the spans and signal if you
    # want the span index positions to be appended to span name
    # Recommended value: True
    return spans, False

#### Scenario 4 - Chatty service ####
# This scenario models one service "badtrace" calling many other services many times "https://example.com/service1", "https://example2.com/service3"  etc. many times
# This signifies a chatty service where one client just hammers lots of external services
####
def scenario4_span_list(trace_id):
    spans = []

    number_of_spans_to_generate = 50
    logger.info(f"Will generate {number_of_spans_to_generate} spans for this trace")
    index = 1

    while index <= number_of_spans_to_generate:
        span_start_time = generate_span_start_time()
        span_end_time = time.time_ns()

        server_address = ""
        endpoint = ""
        span_name = ""
        path = ""

        # Generating 50 spans
        # So split them into 5 equal buckets
        # and call the endpoint based on the bucket number
        bucket = math.ceil(index / 10)

        # Regardless of the bucket
        # the URL path is always "/service1" or "/service2"
        # so we can "hardcode" this now
        server_address = ""
        endpoint = ""
        span_name = ""
        path = f"service{bucket}"

        if bucket == 1: server_address = "example.com"
        if bucket == 2: server_address = "example2.com"
        if bucket == 3: server_address = "example3.com"
        if bucket == 4: server_address = "example4.com"
        if bucket == 5: server_address = "example5.com"

        # Now that the `server_address` is known
        # set the `endpoint` and `span_name`
        endpoint = f"https://{server_address}"
        span_name = f"GET {endpoint}"
        
        span = {
                "traceId": trace_id,
                "spanId": secrets.token_hex(8),
                "name": span_name,
                "kind": "SPAN_KIND_CLIENT",
                "start_time_unix_nano": span_start_time,
                "end_time_unix_nano": span_end_time,
                "droppedAttributesCount": 0,
                "attributes": [{
                    "key": "http.request.method",
                    "value": { "stringValue": "GET" }
                }, {
                    "key": "server.address",
                    "value": { "stringValue": server_address }
                }, {
                    "key": "server.port",
                    "value": { "intValue": 443 }
                }, {
                    "key": "url.full",
                    "value": { "stringValue": f"{endpoint}/{path}" }
                }],
                "events": [],
                "droppedEventsCount": 0,
                "status": {
                    "code": get_span_status_int("OK")
                }
        }
        spans.append(span)
        index += 1

    # Return the spans and signal if you
    # want the span index positions to be appended to span name
    # Recommended value: True
    return spans, False
