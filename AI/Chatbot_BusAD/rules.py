
def generate_response(intent, knowledge_base):
    
    if intent is None or intent not in knowledge_base:
        return "Sorry, I don't have information about that. Ask me about Abu Dhabi buses or Hafilat cards."

    facts = knowledge_base[intent]

    if intent == "hafilat_card":
        locations = ", ".join(facts.get("purchase_locations", []))
        types = ", ".join(facts.get("card_types", []))
        return (f"{facts['description']} Available card types: {types}. "
                f"You can obtain one at: {locations}.")

    elif intent == "card_pricing":
        anonymous = facts.get("anonymous_card_price")
        personalized = facts.get("personalized_card_price")
        return (f"An anonymous Hafilat card costs {anonymous} AED and a personalized "
                f"card costs {personalized} AED.")

    elif intent == "operating_hours":
        return (f"For route 170, the first listed weekday departure from NYU Abu Dhabi "
                f"toward Al Zeina is {facts['route_170_start']} and the last is "
                f"{facts['route_170_end']}.")

    elif intent == "bus_routes":
        return f"Route 170: {facts['route_170']}."

    elif intent == "card_recharge":
        locations = ", ".join(facts.get("recharge_locations", []))
        online = facts.get("online_recharge")
        response = f"You can recharge your Hafilat card at: {locations}."
        if online:
            response += f" Online recharge: {facts.get('recharge_website')}."
        return response

    elif intent == "bus_fares":
        return (f"The stored fare information is a base fare of "
                f"{facts['base_fare']} {facts['currency']}, plus "
                f"{facts['distance_fare']} {facts['currency']} per kilometer, "
                f"up to {facts['maximum_fare']} {facts['currency']}.")

    elif intent == "bus_stops":
        return (f"The main bus station is {facts['main_bus_station']}. "
                f"Route 170 serves {facts['route_170_stop']}.")

    elif intent == "bus_schedules":
        return (f"For route 170 at NYU Abu Dhabi toward Al Zeina, the stored weekday "
                f"first departure is {facts['route_170_first_departure']} and the last "
                f"is {facts['route_170_last_departure']}. Check the official timetable "
                f"for exact departures: {facts['timetable_source']}.")

    return "Sorry, I don't have a response for you"