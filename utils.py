import requests
from loguru import logger
from scenarios import *

def build_spans(trace_id, scenario):
    if scenario == "scenario1":
        return scenario1_span_list(trace_id)
    if scenario == "scenario2":
       return scenario2_span_list(trace_id)
    if scenario == "scenario3":
       return scenario3_span_list(trace_id)
    if scenario == "scenario4":
       return scenario4_span_list(trace_id)
    # TODO: The rest of the scenarios

def build_trace(service_name, span_list):
    trace = {
        "resourceSpans": [
        {
            "resource": {
            "attributes": [
                {
                "key": "service.name",
                "value": {
                    "stringValue": service_name
                }
                }
            ]
            },
            "scopeSpans": [
            {
                "scope": {
                "name": "manual-test"
                },
                "spans": span_list
            }
            ]
        }
        ]
    }

    return trace

def send_trace(endpoint, trace):
    resp = requests.post(
        f"{endpoint}/v1/traces", 
        headers={ "Content-Type": "application/json" }, 
        json=trace,
        timeout=5 
    )
    print(f"Status Code: {resp.status_code}. Content: {resp.content}")

# This function takes an unsorted list of spans
# then sorts and renames them according to start time
# Note: Scenario implementers (YOU) do NOT need to call this
# You simply return the unsorted list to the app and the app code
# does the sort on your behalf
def sort_span_list(span_list, append_span_index):
    # Sort the list by 'start_time' and then rename the 'span' key
    sorted_span_list = sorted(span_list, key=lambda x: x['start_time_unix_nano'])

    # Append span index to span name only if
    # explicitly requested
    # Recommended value here for implementers: True
    if append_span_index:
        for i, span_dict in enumerate(sorted_span_list, start=1):
            span_dict['name'] = f"{span_dict['name']} {i}"
    
    return sorted_span_list
   
