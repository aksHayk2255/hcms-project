from datetime import timedelta
from django.utils import timezone


def calculate_priority(title, description):

    text = (title + " " + description).lower()

    emergency_keywords = [
        "fire", "electric shock", "short circuit",
        "gas leak", "explosion", "smoke"
    ]

    high_keywords = [
        "water leakage", "severe damage",
        "ceiling collapse", "theft"
    ]

    medium_keywords = [
        "fan not working", "light not working",
        "wifi not working", "door broken"
    ]

    for word in emergency_keywords:
        if word in text:
            return "Emergency"

    for word in high_keywords:
        if word in text:
            return "High"

    for word in medium_keywords:
        if word in text:
            return "Medium"

    return "Low"


def calculate_sla_deadline(priority):
    now = timezone.now()

    if priority == "Emergency":
        return now + timedelta(hours=2)

    elif priority == "High":
        return now + timedelta(hours=6)

    elif priority == "Medium":
        return now + timedelta(hours=24)

    return now + timedelta(hours=72)