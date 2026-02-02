# Voice Agent Prompt Generator

Generate production-ready voice agent system prompts for any business. Deploy to VAPI, Retell, or any voice AI platform.

## What It Does

Takes your business information and generates a complete system prompt with:
- Custom persona and personality
- Industry-specific conversation flows
- Step-by-step task instructions
- Escalation protocols
- Professional guardrails

## Quick Start

```bash
# Clone the repo
git clone https://github.com/CloudAIX/voice-agent-starter.git
cd voice-agent-starter

# Run with example
python3 generate_prompt.py --example

# Interactive mode
python3 generate_prompt.py --interactive
```

## Usage

### Interactive Mode

```bash
python3 generate_prompt.py --interactive
```

Walks you through entering:
- Business name and type
- Agent name and personality
- Contact information
- Services offered

### From JSON Config

```bash
python3 generate_prompt.py --config my_business.json
```

Example config file:
```json
{
  "business_name": "Bright Smile Dental",
  "business_type": "medical",
  "agent_name": "Sarah",
  "personality": "warm, professional, and reassuring",
  "address": "456 Oak Street, Melbourne VIC 3000",
  "phone": "(03) 9555-1234",
  "email": "appointments@brightsmile.com.au",
  "website": "www.brightsmile.com.au",
  "services": "- General Dentistry\n- Cosmetic Dentistry\n- Emergency Care",
  "hours": "Monday to Friday: 8:00 AM – 6:00 PM\nSaturday: 9:00 AM – 1:00 PM"
}
```

### Example Mode

```bash
python3 generate_prompt.py --example
```

Generates a complete prompt for "Bella Italia Restaurant" to see the output format.

## Supported Business Types

| Type | Primary Task | Best For |
|------|--------------|----------|
| `restaurant` | Table reservations | Restaurants, cafes, bars |
| `medical` | Appointment scheduling | Clinics, dental, specialists |
| `professional_services` | Consultation booking | Law firms, accountants, consultants |
| `retail` | Customer inquiries | Stores, e-commerce support |
| `general` | General assistance | Any other business |

## Output

Generated prompts are saved to `./output/` with timestamps:

```
output/
├── bella_italia_restaurant_voice_agent_20260202_153045.md
├── bright_smile_dental_voice_agent_20260202_154512.md
└── ...
```

## Example Output

```markdown
# Persona:

You are Sofia, an AI voice assistant at Bella Italia Restaurant...

# Task:

Your primary task is to handle table reservations, answer menu questions...

# Restaurant Information:
...

# Handle Table Reservations Instructions:

1. Get customer name
   - "May I have your name for the reservation?"
   - *Wait for the answer before proceeding.*
...
```

## Deploying to Voice Platforms

### VAPI

```json
{
  "name": "Sofia",
  "voice": "nova",
  "model": "gpt-4-turbo",
  "systemPrompt": "[paste generated prompt]",
  "functions": ["endCall", "transferCall"]
}
```

### Retell

```json
{
  "agent_name": "Sofia",
  "llm_provider": "openai",
  "system_prompt": "[paste generated prompt]",
  "voice_id": "professional-female"
}
```

## Customization

Edit `generate_prompt.py` to:
- Add new business types in `BUSINESS_TEMPLATES`
- Modify conversation flows
- Add industry-specific rules

## License

MIT

---

Built by [GVRN-AI](https://gvrn-ai.com) | Part of the AI Automation toolkit
