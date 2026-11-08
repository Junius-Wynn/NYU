"""Small conversation memory for follow-up questions."""
import re


def create_context():
    return {"last_intent": None, "current_route": None, "current_destination": None}


def resolve_intent(user_input, detected_intent, context):
    """Use remembered topic for short follow-ups; explicit new topics take priority."""
    text = user_input.lower().strip(" ?!.,")
    if re.search(r"\b(?:route|bus)\s*170\b", text):
        context["current_route"] = "170"
    if "nyu" in text or "new york university" in text:
        context["current_destination"] = "NYU Abu Dhabi"
    if "al zeina" in text:
        context["current_destination"] = "Al Zeina"

    # Follow-ups can refer to a previously discussed route without naming it.
    followup = text.startswith(("and ", "what about ", "how about ", "its ", "when does it ", "where does it "))
    if followup and context["last_intent"] is not None:
        if any(word in text for word in ("route", "go", "destination")):
            return "bus_routes"
        if any(word in text for word in ("schedule", "timetable", "arrive", "departure", "frequency", "often")):
            return "bus_schedules"
        if any(word in text for word in ("start", "end", "operating", "hours", "stop running")):
            return "operating_hours"
        if any(word in text for word in ("stop", "station")):
            return "bus_stops"
        if any(word in text for word in ("fare", "cost", "price")):
            return "bus_fares"
        # E.g. 'and on Saturday?' retains the topic, though the KB may lack weekend facts.
        return context["last_intent"]
    return detected_intent


def update_context(intent, context):
    if intent is not None:
        context["last_intent"] = intent
        if intent in {"bus_routes", "bus_schedules", "operating_hours", "bus_stops"}:
            context["current_route"] = "170"  # The KB covers only route 170.
