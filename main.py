from betting_tips import get_all_predictions
from twilio.rest import Client
import os

# === Twilio setup ===
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_NUMBER = 'whatsapp:+14155238886'
USER_NUMBER = 'whatsapp:+27788655765'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

print("🧠 Bot started — generating betting tickets...")

tips = get_all_predictions()
if not tips:
print("⚠️ No predictions fetched — using fallback tips.")
tips = [
"Over 1.5 – Team A vs Team B",
"BTTS – Team C vs Team D",
"Double Chance – Team E vs Team F"
]

ticket = "📅 BETSLIP\n\n" + "\n".join(f"• {t}" for t in tips)

print("\n✅ Ticket ready:\n" + ticket)

# === Send via WhatsApp ===
message = client.messages.create(
from_=TWILIO_NUMBER,
to=USER_NUMBER,
body=ticket
)
print("📲 WhatsApp message sent!")
