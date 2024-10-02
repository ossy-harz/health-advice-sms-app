from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import google.generativeai as genai
import os

# Initialize Flask app
app = Flask(__name__)

# Configure the Google Generative AI with the API key from environment variable
genai.configure(api_key=os.environ["API_KEY"])

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_health_advice(query):
    """This function sends the query to Gemini via Google Generative AI and returns the response."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Provide health and first aid advice for: {query}")
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: Something went wrong while processing your request."

def send_sms(to_number, message):
    """Send an SMS using Twilio."""
    # Split the message into chunks if it's too long
    messages = [message[i:i + 1600] for i in range(0, len(message), 1600)]
    
    for msg in messages:
        try:
            client.messages.create(
                body=msg,
                from_=TWILIO_NUMBER,
                to=to_number
            )
        except Exception as e:
            print(f"Error sending message via Twilio: {e}")

@app.route("/sms", methods=['POST'])
def sms_reply():
    # Get the message the user sent
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')  # Get the sender's number

    # Generate AI response
    advice = get_health_advice(incoming_msg)

    # Send the generated advice back to the user
    send_sms(from_number, advice)

    return str(MessagingResponse())  # Return an empty Twilio response

if __name__ == "__main__":
    app.run(debug=True)
