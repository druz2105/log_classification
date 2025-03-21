from fastapi import FastAPI, HTTPException

from classify import classify_logs
from utils.create_jira_issue import create_jira_issue
from utils.json_schema import LogMessage

log_classification_app = FastAPI()


@log_classification_app.post("/classify/")
async def check_severity_and_trigger_alarm(data: LogMessage):
    """
    Check the severity of a log message and trigger a Datadog alarm if necessary.
    
    This function is an endpoint in a FastAPI application that consumes a
    log message payload, determines its severity, and triggers a Datadog
    alert if the log severity is critical or high. It handles incoming data,
    processes it with classification logic, and sends the appropriate
    response. Any errors encountered in processing are handled appropriately.
    
    Example `curl` request:
        curl -X POST "http://127.0.0.1:3000/classify/" -H "Content-Type: application/json" \
        -d '{"log_type": "HTTP Error", "log_message": "Unauthorized access attempt detected", "process": "Web Server"}'
    
    :param data: The log message object containing the log type and log 
        message to be classified.
    :type data: LogMessage
    :return: A dictionary containing the severity level for the given log 
        message and the alarm status.
    :rtype: dict
    :raises HTTPException: If an unexpected error occurs during
        classification.
    """
    try:
        severity = classify_logs(data.log_type, data.log_message)
        response_jira = create_jira_issue(severity, data.log_type, data.log_message, data.process)
        print(response_jira)
        return {"severity": severity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
