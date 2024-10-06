from flask import Flask, request

app = Flask(__name__)

@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    session_id = request.values.get('sessionId')
    service_code = request.values.get('serviceCode')
    phone_number = request.values.get('phoneNumber')
    user_id = request.values.get('USERID')
    text = request.values.get('text', '')

    if text == '':
        # Screen 1: Welcome message and feelings
        response = f"CON Welcome to my {user_id} USSD Application.\n"
        response += "How are you feeling?\n"
        response += "1. Feeling fine\n"
        response += "2. Feeling frisky\n"
        response += "3. Not well"
    elif text == '1':
        # Screen 2 for feeling fine
        response = "CON Why are you feeling fine?\n"
        response += "1. Money issues\n"
        response += "2. Relationship\n"
        response += "3. A lot"
    elif text == '2':
        # Screen 2 for feeling frisky
        response = "CON Why are you feeling frisky?\n"
        response += "1. Money issues\n"
        response += "2. Relationship\n"
        response += "3. A lot"
    elif text == '3':
        # Screen 2 for not well
        response = "CON Why are you not well?\n"
        response += "1. Money issues\n"
        response += "2. Relationship\n"
        response += "3. A lot"
    elif text in ['1*1', '2*1', '3*1']:
        # Screen 3 for money issues
        feeling = "feeling fine" if text.startswith('1') else "feeling frisky" if text.startswith('2') else "not well"
        response = f"END You are {feeling} because of Money issues."
    elif text in ['1*2', '2*2', '3*2']:
        # Screen 3 for relationship
        feeling = "feeling fine" if text.startswith('1') else "feeling frisky" if text.startswith('2') else "not well"
        response = f"END You are {feeling} because of Relationship."
    elif text in ['1*3', '2*3', '3*3']:
        # Screen 3 for a lot
        feeling = "feeling fine " if text.startswith('1') else "feeling frisky" if text.startswith('2') else "not well"
        response = f"END You are {feeling} because of A lot."
    else:
        # Invalid input handling
        response = "END Invalid input. Please try again."

    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
