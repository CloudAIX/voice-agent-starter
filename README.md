# Voice Agent Prompt Generator

Generate production-ready voice agent system prompts and VAPI configurations. Deploy to VAPI, Retell, or any voice AI platform with Make.com automation.

## Features

- Generate customized voice agent prompts for any business
- Export VAPI-ready JSON configurations
- Pre-built Make.com automation scenarios
- Industry-specific templates (restaurant, medical, professional services, retail)
- Structured data extraction for bookings/appointments

## Quick Start

```bash
# Clone the repo
git clone https://github.com/CloudAIX/voice-agent-starter.git
cd voice-agent-starter

# Generate example prompt
python3 generate_prompt.py --example

# Generate VAPI config
python3 export_vapi.py --example
```

## Usage

### 1. Generate System Prompt

```bash
# Interactive mode
python3 generate_prompt.py --interactive

# From config file
python3 generate_prompt.py --config examples/dental_clinic.json

# Example output
python3 generate_prompt.py --example
```

### 2. Export VAPI Configuration

```bash
# Generate VAPI-ready JSON
python3 export_vapi.py --config examples/dental_clinic.json

# Output includes:
# - Complete assistant configuration
# - Voice settings (ElevenLabs)
# - Transcription settings (Deepgram)
# - Structured data extraction schema
# - Webhook integration
```

### 3. Set Up Make.com Automation

```bash
# Import the scenario template
make_scenarios/vapi_webhook_handler.json
```

See [make_scenarios/README.md](make_scenarios/README.md) for setup instructions.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VOICE AGENT STACK                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │   VAPI      │────►│   LLM       │────►│  Make.com   │   │
│  │  (Voice)    │     │  (GPT-4o)   │     │ (Automation)│   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│        │                    │                    │          │
│        ▼                    ▼                    ▼          │
│   Phone Call         System Prompt         Calendar/CRM     │
│   Handling           + Analysis            Integration      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Supported Business Types

| Type | Primary Task | Auto-Extraction |
|------|--------------|-----------------|
| `restaurant` | Table reservations | Name, date, time, guests |
| `medical` | Appointment scheduling | Patient, date, time, reason |
| `professional_services` | Consultation booking | Client, date, matter type |
| `retail` | Customer inquiries | Summary, follow-up needed |
| `general` | General assistance | Summary, follow-up needed |

## Project Structure

```
voice-agent-starter/
├── generate_prompt.py      # Main prompt generator
├── export_vapi.py          # VAPI configuration exporter
├── examples/
│   ├── dental_clinic.json  # Medical example
│   └── law_firm.json       # Professional services example
├── make_scenarios/
│   ├── README.md           # Make.com setup guide
│   └── vapi_webhook_handler.json  # Importable scenario
└── output/                 # Generated files (git ignored)
    ├── prompts/            # System prompts
    └── vapi/               # VAPI configs
```

## Example Config

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
  "hours": "Monday to Friday: 8:00 AM – 6:00 PM",
  "voice_style": "professional_female",
  "webhook_url": "https://hook.make.com/YOUR_WEBHOOK_ID"
}
```

## Deployment Guide

### Step 1: Generate Configuration

```bash
python3 export_vapi.py --config your_business.json
```

### Step 2: Create VAPI Assistant

1. Sign up at [vapi.ai](https://vapi.ai)
2. Create new Assistant
3. Import the generated JSON from `output/vapi/`
4. Note: Replace `YOUR_MAKE_WEBHOOK_URL` with actual webhook

### Step 3: Set Up Make.com

1. Sign up at [make.com](https://make.com)
2. Create new Scenario → Import Blueprint
3. Upload `make_scenarios/vapi_webhook_handler.json`
4. Configure:
   - Click webhook module → Copy URL
   - Connect Google Calendar
   - Connect Gmail
   - Update email recipient
5. Turn on scenario
6. Paste webhook URL into VAPI assistant

### Step 4: Get Phone Number

1. In VAPI dashboard, go to Phone Numbers
2. Purchase or connect a number
3. Link to your assistant

### Step 5: Test

1. Call your VAPI phone number
2. Make a test reservation/appointment
3. Verify Make.com creates calendar event
4. Check email notification if follow-up needed

## Voice Options

| Style | Voice | Best For |
|-------|-------|----------|
| `professional_female` | Default | Medical, legal, business |
| `professional_male` | Alternative | Business, consulting |
| `friendly_female` | Warm tone | Restaurants, retail |
| `friendly_male` | Casual | Retail, general |

## Customization

### Add New Business Type

Edit `generate_prompt.py`:

```python
BUSINESS_TEMPLATES["spa"] = {
    "primary_task": "book spa appointments",
    "secondary_tasks": "answer service questions, explain treatments",
    "special_sections": [...],
    "flow_steps": [...]
}
```

### Modify Analysis Schema

Edit `export_vapi.py` → `create_analysis_schema()` to add custom fields for extraction.

### Extend Make.com Workflow

Add modules to the scenario for:
- CRM integration (HubSpot, Salesforce)
- SMS confirmations (Twilio)
- Slack notifications
- Airtable logging

## Pricing Reference

| Deliverable | Typical Price |
|-------------|---------------|
| Basic voice agent prompt | $500-1,000 |
| With VAPI + Make.com integration | $1,500-3,000 |
| Full deployment + testing | $3,000-5,000 |
| Ongoing maintenance (monthly) | $300-500 |

## License

MIT

---

Built by [GVRN-AI](https://gvrn-ai.com) | AI Voice Agent Solutions
