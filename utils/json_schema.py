from pydantic import BaseModel


class LogMessage(BaseModel):
    """
    This is a value object that should be used to validate LogMessages.
    """
    log_type: str
    log_message: str
    process: str
