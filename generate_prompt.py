#!/usr/bin/env python3
"""
Voice Agent Prompt Generator
Generate customized voice agent system prompts for any business.

Usage:
    python generate_prompt.py
    python generate_prompt.py --interactive
    python generate_prompt.py --example
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

# Business type templates with industry-specific sections
BUSINESS_TEMPLATES = {
    "restaurant": {
        "primary_task": "handle table reservations",
        "secondary_tasks": "answer menu questions, provide hours and directions",
        "special_sections": [
            "Today's specials",
            "Dietary options (vegan, gluten-free, allergies)",
            "Parking information",
            "Private event capabilities",
            "Dress code (if applicable)"
        ],
        "flow_steps": [
            ("Get customer name", "May I have your name for the reservation?"),
            ("Get preferred date", "What date would you like to dine with us?"),
            ("Get preferred time", "And what time works best for you?"),
            ("Get party size", "How many guests will be joining?"),
            ("Confirm details", "Let me confirm: [name], party of [size], on [date] at [time]. Is that correct?"),
            ("Close", "Perfect! We look forward to seeing you. Is there anything else I can help with?")
        ]
    },
    "medical": {
        "primary_task": "schedule patient appointments",
        "secondary_tasks": "answer questions about services, handle prescription refill requests",
        "special_sections": [
            "Accepted insurance providers",
            "After-hours emergency protocols",
            "New patient vs existing patient flows",
            "Required documents for first visit"
        ],
        "flow_steps": [
            ("Verify patient", "May I have your name and date of birth please?"),
            ("Check patient status", "Are you an existing patient, or will this be your first visit?"),
            ("Get reason for visit", "What brings you in today?"),
            ("Offer available times", "I have availability on [dates]. What works best for you?"),
            ("Confirm appointment", "You're scheduled for [date] at [time] for [reason]. We'll see you then!"),
            ("Provide instructions", "Please arrive 15 minutes early and bring your insurance card.")
        ]
    },
    "professional_services": {
        "primary_task": "book consultations",
        "secondary_tasks": "answer general inquiries, explain service areas",
        "special_sections": [
            "Practice areas / services offered",
            "Consultation fees",
            "Required documents",
            "Confidentiality assurances"
        ],
        "flow_steps": [
            ("Get caller name", "May I have your name please?"),
            ("Understand need", "How can we help you today? What type of matter are you dealing with?"),
            ("Explain process", "For that type of matter, we typically start with a consultation. Would you like to schedule one?"),
            ("Schedule", "I have availability on [dates]. What works for your schedule?"),
            ("Confirm", "You're booked for [date] at [time]. Is there anything you'd like to bring or prepare?")
        ]
    },
    "retail": {
        "primary_task": "answer customer inquiries",
        "secondary_tasks": "provide store hours, check product availability, handle order status questions",
        "special_sections": [
            "Store locations and hours",
            "Return policy",
            "Current promotions",
            "Shipping information"
        ],
        "flow_steps": [
            ("Greet", "Thank you for calling [business]. How can I help you today?"),
            ("Handle inquiry", "[Address specific question]"),
            ("Offer additional help", "Is there anything else I can help you with?"),
            ("Close", "Thank you for calling. Have a great day!")
        ]
    },
    "general": {
        "primary_task": "assist callers with their inquiries",
        "secondary_tasks": "answer questions, schedule appointments, provide information",
        "special_sections": [
            "Services offered",
            "Pricing information",
            "Location and hours"
        ],
        "flow_steps": [
            ("Greet", "Thank you for calling. How can I help you today?"),
            ("Handle request", "[Address caller's needs]"),
            ("Confirm", "[Confirm any actions taken]"),
            ("Close", "Is there anything else I can assist with?")
        ]
    }
}


def generate_prompt(config: dict) -> str:
    """Generate a voice agent system prompt from configuration."""

    business_type = config.get("business_type", "general")
    template = BUSINESS_TEMPLATES.get(business_type, BUSINESS_TEMPLATES["general"])

    # Build the flow steps section
    flow_section = ""
    for i, (step_name, example) in enumerate(template["flow_steps"], 1):
        flow_section += f"""
{i}. {step_name}
   - "{example}"
   - *Wait for the answer before proceeding.*
"""

    # Build special sections if provided
    special_features = config.get("special_features", "")
    if not special_features and template["special_sections"]:
        special_features = "- " + "\n- ".join(template["special_sections"][:3])

    prompt = f"""# Persona:

You are {config.get('agent_name', 'Alex')}, an AI voice assistant at {config['business_name']}. You are in charge of communication with our customers. You are known for your {config.get('personality', 'professional, friendly, and helpful')} demeanor and extensive experience in providing high quality customer experience.

# Task:

Your primary task is to {template['primary_task']}, {template['secondary_tasks']}.

# {config['business_type'].title()} Information:

## Location:
{config.get('address', '[Address not provided]')} {f"({config.get('location_notes', '')})" if config.get('location_notes') else ''}

## Business Type:
{config.get('business_category', config['business_type'].title())}

## Services/Offerings:
{config.get('services', '- [Services to be added]')}

## Hours of Operation:
{config.get('hours', '- Monday to Friday: 9:00 AM – 5:00 PM')}

## Contact Information:
- Phone: {config.get('phone', '[Phone number]')}
- Email: {config.get('email', '[Email address]')}
- Website: {config.get('website', '[Website URL]')}

## Special Features:
{special_features}

# {template['primary_task'].title()} Instructions:
{flow_section}

# Ending the Call:

When the conversation is complete and the customer has no more questions, use the "endCall" function to end the call gracefully.

# Escalation and Assistance Request:

You can transfer the call to {config.get('escalation_contact', 'a manager')} using the "transferCall" function in these cases:

1. Customer directly requests to speak to a manager or human.
2. Customer is not satisfied with the service.
3. Request is outside your capabilities.
4. Emergency situations requiring immediate human attention.

# Rules and Limitations:

- Respond in a concise and professional manner.
- Keep responses short and relevant (1-2 sentences when possible).
- Always ask only ONE question at a time.
- Use conversational language with natural filler phrases ("Sure thing", "Let me check that for you").
- After providing a response, occasionally ask "Is there anything else I can help you with?"
- NEVER ask for phone number (you already have it from caller ID).
- NEVER mention internal functions, tools, or that you are an AI unless directly asked.
- NEVER be overly enthusiastic with every response.
- If you don't know something, say so honestly and offer to transfer to someone who can help.
{config.get('additional_rules', '')}
"""

    return prompt.strip()


def get_interactive_input() -> dict:
    """Gather business information interactively."""
    print("\n" + "="*60)
    print("  Voice Agent Prompt Generator")
    print("="*60 + "\n")

    config = {}

    # Required information
    config['business_name'] = input("Business name: ").strip()

    print("\nBusiness types: restaurant, medical, professional_services, retail, general")
    config['business_type'] = input("Business type [general]: ").strip().lower() or "general"

    config['agent_name'] = input("Agent name [Alex]: ").strip() or "Alex"
    config['personality'] = input("Agent personality [professional, friendly, and helpful]: ").strip() or "professional, friendly, and helpful"

    # Optional information
    print("\n--- Optional (press Enter to skip) ---\n")
    config['address'] = input("Business address: ").strip() or "[Address]"
    config['phone'] = input("Phone number: ").strip() or "[Phone]"
    config['email'] = input("Email: ").strip() or "[Email]"
    config['website'] = input("Website: ").strip() or "[Website]"
    config['hours'] = input("Hours (e.g., 'Mon-Fri 9-5'): ").strip() or "Monday to Friday: 9:00 AM – 5:00 PM"

    services = input("Main services (comma-separated): ").strip()
    if services:
        config['services'] = "\n".join(f"- {s.strip()}" for s in services.split(","))

    return config


def save_prompt(prompt: str, business_name: str, output_dir: Path = None) -> Path:
    """Save the generated prompt to a file."""
    if output_dir is None:
        output_dir = Path.cwd() / "output"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Create safe filename
    safe_name = "".join(c if c.isalnum() or c in "- " else "_" for c in business_name)
    safe_name = safe_name.replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{safe_name}_voice_agent_{timestamp}.md"
    filepath = output_dir / filename

    with open(filepath, "w") as f:
        f.write(prompt)

    return filepath


def run_example():
    """Generate an example prompt for a restaurant."""
    example_config = {
        "business_name": "Bella Italia Restaurant",
        "business_type": "restaurant",
        "agent_name": "Sofia",
        "personality": "warm, welcoming, and knowledgeable about Italian cuisine",
        "address": "123 Main Street, Melbourne VIC 3000",
        "location_notes": "Free parking behind the building",
        "business_category": "Italian Fine Dining",
        "services": """- Lunch service (12pm - 3pm)
- Dinner service (5pm - 10pm)
- Private event catering
- Takeaway available""",
        "hours": """- Tuesday to Thursday: 12:00 PM – 10:00 PM
- Friday & Saturday: 12:00 PM – 11:00 PM
- Sunday: 12:00 PM – 9:00 PM
- Monday: Closed""",
        "phone": "(03) 9555-1234",
        "email": "reservations@bellaitalia.com.au",
        "website": "www.bellaitalia.com.au",
        "special_features": """- Authentic Italian cuisine with imported ingredients
- Extensive wine list featuring Italian and Australian wines
- Gluten-free and vegetarian options available
- Private dining room for up to 20 guests
- Outdoor terrace seating (weather permitting)""",
        "escalation_contact": "the restaurant manager",
        "additional_rules": """- Maximum party size is 12 for regular bookings (larger groups need manager approval)
- Mention the daily specials if asked about recommendations
- For dietary restrictions, assure customers that the chef can accommodate most needs"""
    }

    return generate_prompt(example_config), example_config["business_name"]


def main():
    parser = argparse.ArgumentParser(description="Generate voice agent system prompts")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--example", "-e", action="store_true", help="Generate example prompt")
    parser.add_argument("--config", "-c", type=str, help="Path to JSON config file")
    parser.add_argument("--output", "-o", type=str, help="Output directory")

    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else None

    if args.example:
        print("\nGenerating example prompt for Bella Italia Restaurant...\n")
        prompt, business_name = run_example()
    elif args.config:
        with open(args.config) as f:
            config = json.load(f)
        prompt = generate_prompt(config)
        business_name = config["business_name"]
    elif args.interactive:
        config = get_interactive_input()
        prompt = generate_prompt(config)
        business_name = config["business_name"]
    else:
        # Default: show example
        print("No arguments provided. Use --help for options, or --example for a demo.\n")
        print("Running example mode...\n")
        prompt, business_name = run_example()

    # Save the prompt
    filepath = save_prompt(prompt, business_name, output_dir)

    print("="*60)
    print("  Generated Voice Agent Prompt")
    print("="*60)
    print(prompt)
    print("\n" + "="*60)
    print(f"Saved to: {filepath}")
    print("="*60)


if __name__ == "__main__":
    main()
