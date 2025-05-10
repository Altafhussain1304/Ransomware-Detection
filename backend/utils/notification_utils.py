from plyer import notification

def get_threat_level_color(prediction: str) -> str:
    """
    Returns a color string based on the threat prediction.
    """
    if prediction.lower() == "malicious":
        return "Red"
    elif prediction.lower() == "suspicious":
        return "Yellow"
    else:
        return "Green"

def send_desktop_alert(title: str, message: str, enabled: bool = True):
    """
    Sends a desktop notification if enabled.
    """
    if enabled:
        notification.notify(
            title=title,
            message=message,
            app_name="RansomSaver",
            timeout=5  # seconds
        )