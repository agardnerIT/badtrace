import argparse
from loguru import logger
import sys
import secrets
from utils import *

BADTRACE_VERSION="0.1.0"

parser = argparse.ArgumentParser()

parser.add_argument('-ep', '--endpoint', required=True)
parser.add_argument('-sen', '--service-name', required=False, default="badtrace")
parser.add_argument('-s', '--scenario', required=False, default="scenario1")
parser.add_argument('-tc', '--trace-count', default=1)
parser.add_argument('-dr','--dry-run','--dry', required=False, default="False")
parser.add_argument('-insec', '--insecure', required=False, default="False")
parser.add_argument('-v', '--version', action="version", version=BADTRACE_VERSION)

args = parser.parse_args()

endpoint = args.endpoint
service_name = args.service_name
scenario = args.scenario
trace_count = int(args.trace_count)
dry_run = args.dry_run
allow_insecure = args.insecure

# First convert to boolean
ALLOW_INSECURE = False
if allow_insecure.lower() == "true":
  ALLOW_INSECURE = True

# First convert to boolean
DRY_RUN = True
if dry_run.lower() == "false":
  DRY_RUN = False

if endpoint.startswith("http://") and not ALLOW_INSECURE:
  logger.error("Endpoint is http:// (insecure). You MUST set '--insecure true'. Trace has NOT been sent.")
  sys.exit(1)

logger.info(f"[{service_name}] Will send {trace_count} trace(s) for {scenario} to endpoint: {endpoint}")

index = 1
while index <= trace_count:
    # Generate random trace ID
    trace_id = secrets.token_hex(16)

    span_list, will_append_span_index = build_spans(trace_id, scenario)

    span_list = sort_span_list(span_list=span_list, append_span_index=will_append_span_index)
    trace = build_trace(service_name, span_list)

    if not DRY_RUN:
        send_trace(endpoint, trace)
    
    index += 1
