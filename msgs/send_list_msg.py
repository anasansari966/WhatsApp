import requests
import json

url = "https://graph.facebook.com/v19.0/308267025701231/messages"

languages = ["English", "Hindi", "Gujarati", "Bengali", "Malayalam", "Telugu", "Marathi", "Odiya", "Tamil"]

def list_intent():
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "919667623696",
        "context": {
            "message_id": "<MSGID_OF_PREV_MSG>"
        },
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Please Select The language"
            },
            "body": {
                "text": "For continue the process select one language"
            },
            "footer": {
                "text": ""
            },
            "action": {
                "button": "language",
                "sections": [
                    {
                        "title": "Languages",
                        "rows": [
                            {
                                "id": f"language_{lang.lower()}",
                                "title": lang,
                                "description": None
                            }
                            for lang in languages
                        ]
                    }
                ]
            }
        }
    })

    return payload

def welcome_message(language):
    if language.lower() == 'english':
        return "Please provide your WD Code."
    elif language.lower() == 'hindi':
        return "कृपया अपना डब्ल्यूडी कोड प्रदान करें।"
    elif language.lower() == 'gujarati':
        return "કૃપા કરીને તમારો ડબલ્યુડી કોડ આપો."
    # Add more languages as needed

def job_role_list():
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "919667623696",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Please Select Your Job Role"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "distributor",
                            "title": "Distributor"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "supervisor_tl",
                            "title": "Supervisor/TL"
                        }
                    }
                ]
            }
        }
    })

    return payload

def payout_options_list():
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "919667623696",
        "context": {
            "message_id": "<MSGID_OF_PREV_MSG>"
        },
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Please Select How You Would Like to Receive Payout (Money)"
            },
            "body": {
                "text": "Choose your preferred payout option"
            },
            "footer": {
                "text": ""
            },
            "action": {
                "button": "payout_option",
                "sections": [
                    {
                        "title": "Payout Options",
                        "rows": [
                            {
                                "id": "bank_transfer",
                                "title": "Bank Transfer",
                                "description": None
                            },
                            {
                                "id": "upi",
                                "title": "UPI",
                                "description": None
                            }
                        ]
                    }
                ]
            }
        }
    })

    return payload

def account_holder_name_prompt():
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "919667623696",
        "context": {
            "message_id": "<MSGID_OF_PREV_MSG>"
        },
        "type": "text",
        "text": {
            "body": "Please provide the following details:\n\n1. Account Holder Name\n2. Account Number\n3. IFSC Code"
        }
    })

    return payload

def send_text_message(to_number, message_content):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message_content
        }
    })
    return payload