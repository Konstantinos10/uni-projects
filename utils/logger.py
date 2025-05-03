import datetime as dt
def log(message, log_file="log.txt"):
    """Logs a message to a specified log file."""
    with open(log_file, "a") as f:
        f.write(f"{dt.datetime.now()} {str(message)}\n")