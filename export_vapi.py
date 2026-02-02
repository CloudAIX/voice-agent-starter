#!/usr/bin/env python3
"""
VAPI Export Module
Export voice agent prompts in VAPI-ready JSON format.

Usage:
    python export_vapi.py --config examples/dental_clinic.json
    python export_vapi.py --example
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from generate_prompt import generate_prompt, BUSINESS_TEMPLATES

# Default VAPI configuration
VAPI_DEFAULTS = {
    "voice": {
        "model": "eleven_turbo_v2_5",
        "voiceId": "g1gkVFi2jgj2rTKdNDq7",  # Professional female
        "provider": "11labs",
        "stability": 0.6,
        "similarityBoost": 0.2,
        "useSpeakerBoost": True,
        "inputMinCharacters": 10
    },
    "model": {
        "model": "gpt-4o-mini",
        "provider": "openai",
        "temperature": 0.2
    },
    "transcriber": {
        "model": "nova-2",
        "language": "en",
        "provider": "deepgram"
    },
    "silenceTimeoutSeconds": 10,
    "responseDelaySeconds": 0.2,
    "llmRequestDelaySeconds": 0.1,
    "numWordsToInterruptAssistant": 1,
    "backgroundSound": "office",
    "backgroundDenoisingEnabled": True,
    "endCallFunctionEnabled": True,
    "clientMessages": ["voice-input"],
    "serverMessages": ["end-of-call-report"]
}

# Voice options
VOICE_OPTIONS = {
    "professional_female": "g1gkVFi2jgj2rTKdNDq7",
    "professional_male": "pNInz6obpgDQGcFmaJgB",
    "friendly_female": "EXAVITQu4vr4xnSDxMaL",
    "friendly_male": "VR6AewLTigWG4xSOukaG"
}


def create_vapi_config(config: dict, system_prompt: str) -> dict:
    """Create a complete VAPI assistant configuration."""

    agent_name = config.get("agent_name", "Assistant")
    business_name = config.get("business_name", "Business")
    voice_style = config.get("voice_style", "professional_female")

    # Build first message
    first_message = config.get(
        "first_message",
        f"Hi, this is {business_name}, {agent_name} speaking. How can I help you?"
    )

    # Build analysis schema based on business type
    analysis_schema = create_analysis_schema(config.get("business_type", "general"))

    vapi_config = {
        "name": f"{agent_name} - {business_name}",
        "voice": {
            **VAPI_DEFAULTS["voice"],
            "voiceId": VOICE_OPTIONS.get(voice_style, VOICE_OPTIONS["professional_female"])
        },
        "model": {
            **VAPI_DEFAULTS["model"],
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]
        },
        "transcriber": VAPI_DEFAULTS["transcriber"],
        "firstMessage": first_message,
        "silenceTimeoutSeconds": VAPI_DEFAULTS["silenceTimeoutSeconds"],
        "responseDelaySeconds": VAPI_DEFAULTS["responseDelaySeconds"],
        "llmRequestDelaySeconds": VAPI_DEFAULTS["llmRequestDelaySeconds"],
        "numWordsToInterruptAssistant": VAPI_DEFAULTS["numWordsToInterruptAssistant"],
        "backgroundSound": VAPI_DEFAULTS["backgroundSound"],
        "backgroundDenoisingEnabled": VAPI_DEFAULTS["backgroundDenoisingEnabled"],
        "endCallFunctionEnabled": VAPI_DEFAULTS["endCallFunctionEnabled"],
        "clientMessages": VAPI_DEFAULTS["clientMessages"],
        "serverMessages": VAPI_DEFAULTS["serverMessages"],
        "serverUrl": config.get("webhook_url", "YOUR_MAKE_WEBHOOK_URL"),
        "analysisPlan": {
            "structuredDataPrompt": "Extract the listed parameters from the call transcript.\n- Current date is: {{date}}\n- Current time is: {{time}}",
            "structuredDataSchema": analysis_schema
        },
        "messagePlan": {
            "idleMessages": [
                "Let me know if there's anything you need.",
                "Is there anything else I can help with?"
            ]
        }
    }

    return vapi_config


def create_analysis_schema(business_type: str) -> dict:
    """Create structured data extraction schema based on business type."""

    base_schema = {
        "type": "object",
        "properties": {
            "call_summary": {
                "description": "Brief summary of what the caller wanted.",
                "type": "string"
            },
            "follow_up_required": {
                "description": "TRUE if follow-up action is needed, otherwise FALSE.",
                "type": "boolean"
            }
        },
        "required": ["call_summary", "follow_up_required"]
    }

    if business_type == "restaurant":
        base_schema["properties"].update({
            "reservation": {
                "description": "TRUE if reservation was requested, otherwise FALSE.",
                "type": "boolean"
            },
            "reservation_name": {
                "description": "Name for the reservation.",
                "type": "string"
            },
            "reservation_date": {
                "description": "Date of reservation in yyyy-mm-dd format.",
                "type": "string"
            },
            "reservation_time": {
                "description": "Time of reservation in 24H format (e.g., 19:00).",
                "type": "string"
            },
            "reservation_guests": {
                "description": "Number of guests.",
                "type": "number"
            }
        })
        base_schema["required"].append("reservation")

    elif business_type == "medical":
        base_schema["properties"].update({
            "appointment": {
                "description": "TRUE if appointment was requested, otherwise FALSE.",
                "type": "boolean"
            },
            "patient_name": {
                "description": "Name of the patient.",
                "type": "string"
            },
            "appointment_date": {
                "description": "Date of appointment in yyyy-mm-dd format.",
                "type": "string"
            },
            "appointment_time": {
                "description": "Time of appointment in 24H format.",
                "type": "string"
            },
            "appointment_reason": {
                "description": "Reason for the appointment.",
                "type": "string"
            },
            "new_patient": {
                "description": "TRUE if this is a new patient, FALSE if existing.",
                "type": "boolean"
            }
        })
        base_schema["required"].append("appointment")

    elif business_type == "professional_services":
        base_schema["properties"].update({
            "consultation": {
                "description": "TRUE if consultation was requested, otherwise FALSE.",
                "type": "boolean"
            },
            "client_name": {
                "description": "Name of the potential client.",
                "type": "string"
            },
            "consultation_date": {
                "description": "Date of consultation in yyyy-mm-dd format.",
                "type": "string"
            },
            "matter_type": {
                "description": "Type of matter or service needed.",
                "type": "string"
            }
        })
        base_schema["required"].append("consultation")

    return base_schema


def save_vapi_config(vapi_config: dict, business_name: str, output_dir: Path = None) -> Path:
    """Save VAPI configuration to JSON file."""

    if output_dir is None:
        output_dir = Path.cwd() / "output" / "vapi"

    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in "- " else "_" for c in business_name)
    safe_name = safe_name.replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{safe_name}_vapi_config_{timestamp}.json"
    filepath = output_dir / filename

    with open(filepath, "w") as f:
        json.dump(vapi_config, f, indent=2)

    return filepath


def run_example():
    """Generate example VAPI config for restaurant."""

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
        "voice_style": "professional_female",
        "webhook_url": "https://hook.eu2.make.com/YOUR_WEBHOOK_ID"
    }

    return example_config


def main():
    parser = argparse.ArgumentParser(description="Export voice agent as VAPI configuration")
    parser.add_argument("--config", "-c", type=str, help="Path to JSON config file")
    parser.add_argument("--example", "-e", action="store_true", help="Generate example")
    parser.add_argument("--output", "-o", type=str, help="Output directory")

    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else None

    if args.example:
        config = run_example()
    elif args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        print("Use --example or --config <file.json>")
        print("Run with --help for more options.")
        return

    # Generate the system prompt
    system_prompt = generate_prompt(config)

    # Create VAPI configuration
    vapi_config = create_vapi_config(config, system_prompt)

    # Save to file
    filepath = save_vapi_config(vapi_config, config["business_name"], output_dir)

    print("=" * 60)
    print("  VAPI Configuration Generated")
    print("=" * 60)
    print(f"\nSaved to: {filepath}")
    print("\nNext steps:")
    print("1. Go to https://vapi.ai and create an account")
    print("2. Create a new Assistant")
    print("3. Import this JSON configuration")
    print("4. Replace YOUR_MAKE_WEBHOOK_URL with your actual webhook")
    print("5. Get a phone number and link it to this assistant")
    print("=" * 60)


if __name__ == "__main__":
    main()
