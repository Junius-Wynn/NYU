from intents import patterns
from knowledge import knowledge_base
from intent_detection import detect_intent
from rules import generate_response
from context import create_context, resolve_intent, update_context
from conversation import detect_conversation_type, greeting, goodbye, help as help_response, fallback


def main():
    context = create_context()
    print(greeting())
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot:", goodbye())
            break
        if not user_input:
            print("Bot:", fallback())
            continue
        conversation_type = detect_conversation_type(user_input)
        if conversation_type == "goodbye":
            print("Bot:", goodbye())
            break
        if conversation_type == "greeting":
            response = greeting()
        elif conversation_type == "help":
            response = help_response()
        else:
            detected_intent = detect_intent(user_input, patterns)
            intent = resolve_intent(user_input, detected_intent, context)
            response = generate_response(intent, knowledge_base) if intent else fallback()
            update_context(intent, context)
        print("Bot:", response)


if __name__ == "__main__":
    main()
