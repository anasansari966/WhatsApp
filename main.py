import os
from flask import Flask, request, json
import requests
from dotenv import load_dotenv
from msgs.send_list_msg import (
    list_intent, welcome_message, job_role_list, payout_options_list, account_holder_name_prompt, send_text_message, receive
)
load_dotenv()

app = Flask(__name__)

token = os.getenv('TOKEN')
mytoken = os.getenv('MYTOKEN')

user_name = 'User'
user_states = {}

@app.route("/webhook", methods=["GET"])
def webhook_verification():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token1 = request.args.get("hub.verify_token")

    if mode == "subscribe" and token1 == mytoken:
        return challenge, 200
    else:
        return "", 403

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    body = request.get_json()
    print(json.dumps(body, indent=2))

    if request.json.get("object"):
        if (request.json.get("entry")
                and request.json["entry"][0].get("changes")
                and request.json["entry"][0]["changes"][0]
                and request.json["entry"][0]["changes"][0].get("value")
                and request.json["entry"][0]["changes"][0]["value"].get("messages")
                and request.json["entry"][0]["changes"][0]["value"]["messages"][0]):
            phone_number_id = request.json["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
            from_number = request.json["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

            url = f"https://graph.facebook.com/v15.0/{phone_number_id}/messages"
            headers = {
                "Content-type": "application/json",
                "Authorization": f"Bearer {token}",
            }

            user_state = user_states.get(from_number, "initial")

            try:
                msg_body = request.json["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                if user_state == "initial" and msg_body.lower() in ['hi', 'hello']:
                    data1 = list_intent()
                    resp1 = requests.post(url, headers=headers, data=data1)
                    user_states[from_number] = "language_selected"
                    print(resp1.text)
                    print("response code :" + str(resp1.status_code))
                elif user_state == "awaiting_anything":
                    thank_you_msg = send_text_message(from_number, "Thank you")
                    resp_thank_you = requests.post(url, headers=headers, data=thank_you_msg)
                    user_states[from_number] = "completed"
                    print(resp_thank_you.text)
                    print("response code for thank you message:" + str(resp_thank_you.status_code))
                else:
                    pass
            except:
                pass

            try:
                if user_state == "language_selected":
                    language_selected = request.json["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"]
                    welcome_msg = welcome_message(language_selected)
                    welcome_data = send_text_message(from_number, welcome_msg)
                    welcome_resp = requests.post(url, headers=headers, data=welcome_data)
                    user_states[from_number] = "awaiting_wd_code"
                    print(welcome_resp.text)
                    print("response code for welcome message:" + str(welcome_resp.status_code))
            except:
                pass

            try:
                if user_state == "awaiting_wd_code":
                    wd_code = request.json["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                    if wd_code.isdigit():  # Assuming WD Code is numeric
                        job_role_data = job_role_list()
                        resp2 = requests.post(url, headers=headers, data=job_role_data)
                        user_states[from_number] = "awaiting_job_role"
                        print(resp2.text)
                        print("response code for job role list:" + str(resp2.status_code))
            except:
                pass

            try:
                if user_state == "awaiting_job_role":
                    job_role_selected = request.json["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["button_reply"]["title"]
                    if job_role_selected:
                        # Prompt the user to type anything
                        prompt_text = f"You have selected {job_role_selected}. Please type anything to continue."
                        prompt_payload = send_text_message(from_number, prompt_text)
                        prompt_resp = requests.post(url, headers=headers, data=prompt_payload)
                        user_states[from_number] = "awaiting_anything"
                        print(prompt_resp.text)
                        print("response code for user input prompt:" + str(prompt_resp.status_code))
            except:
                pass

            try:
                if user_state == "awaiting_anything":
                    payout_option_selected = request.json["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"]
                    if payout_option_selected.lower() == "bank transfer":
                        # Prompt user to provide account details
                        account_details_prompt = account_holder_name_prompt()
                        account_details_resp = requests.post(url, headers=headers, data=account_details_prompt)
                        print(account_details_resp.text)
                        print("response code for account details prompt:" + str(account_details_resp.status_code))
                    elif payout_option_selected.lower() == "upi":
                        # Prompt user to provide their name
                        upi_name_prompt = send_text_message(from_number, "Please provide your name")
                        upi_name_resp = requests.post(url, headers=headers, data=upi_name_prompt)
                        print(upi_name_resp.text)
                        print("response code for UPI name prompt:" + str(upi_name_resp.status_code))
            except:
                pass
    return ('', 200)

@app.route("/")
def hello():
    return "Hello, this is webhook setup"

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')