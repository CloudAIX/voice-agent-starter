# Make.com Scenario Templates

Import these scenarios into Make.com to automate actions after voice agent calls.

## Available Scenarios

### 1. vapi_webhook_handler.json

Handles end-of-call reports from VAPI voice agents.

**What it does:**
- Receives webhook when call ends
- Routes based on call outcome:
  - **Reservation made** → Creates Google Calendar event
  - **Follow-up required** → Sends email notification

**Setup:**
1. Go to [Make.com](https://make.com) and create account
2. Create new scenario → Import from file
3. Upload `vapi_webhook_handler.json`
4. Configure modules:
   - Click webhook module → Copy webhook URL
   - Connect Google Calendar
   - Connect Gmail
   - Update email recipient
5. Turn on scenario
6. Paste webhook URL in your VAPI assistant's `serverUrl` field

## Customization Ideas

### Add CRM Integration
Add a module after the webhook to:
- Create/update contact in HubSpot, Salesforce, or Airtable
- Log call details and outcomes

### Add SMS Confirmation
Add Twilio module to:
- Send reservation confirmation to caller
- Send reminder 24 hours before appointment

### Add Slack Notification
Add Slack module to:
- Alert team channel for urgent calls
- Log all calls for review

## Webhook Data Structure

VAPI sends this data to your webhook:

```json
{
  "message": {
    "type": "end-of-call-report",
    "call": {
      "id": "call_abc123",
      "customer": {
        "number": "+1234567890"
      },
      "duration": 180
    },
    "transcript": "Full call transcript...",
    "analysis": {
      "summary": "Caller requested a table reservation for 4 people on Friday at 7pm.",
      "structuredData": {
        "reservation": true,
        "reservation_name": "John Smith",
        "reservation_date": "2024-02-15",
        "reservation_time": "19:00",
        "reservation_guests": 4,
        "follow_up_required": false
      }
    }
  }
}
```

## Testing

1. Use VAPI's test call feature
2. Check Make.com scenario execution history
3. Verify calendar event / email was created
