from flask import Flask, request
import africastalking
import os

app = Flask(__name__)
username = "errands"
api_key = "dd1ce3edd9eee0ff3e5f2eeaf04111b2d59eac81739580a9973affa00d22ce18"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)
    
    #ussd logic
    if text == "":
        #main menu
        response = "CON What errand would you like to be done for?\n"
        response += "1. Need shopping done\n"
        response += "2. Need a parcel picked up\n"
        response += "3. Need to move house\n"
        response += "4. Need a handyman\n"
        response += "5. Need some cleaning done"
    elif text == "1":
        #sub menu 1
        response = "CON What would you like to check on your account?\n"
        response += "1. Account number"
        response += "2. Account balance"
    elif text == "2":
        #sub menu 1
        response = "END Your phone number is {}".format(phone_number)
    elif text == "3":
        try:
            #sending the sms
            sms_response = sms.send("Thank you for going through this tutorial", sms_phone_number)
            print(sms_response)
        except Exception as e:
            #show us what went wrong
            print(f"Houston, we have a problem: {e}")
    elif text == "1*1":
        #ussd menus are split using *
        account_number = "1243324376742"
        response = "END Your account number is {}".format(account_number)
    elif text == "1*2":
        account_balance = "100,000"
        response = "END Your account balance is USD {}".format(account_balance)
    else:
        response = "END Invalid input. Try again."

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))


