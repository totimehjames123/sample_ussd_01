from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory session storage
sessions = {}

@app.route('/ussd', methods=['POST'])
def ussd():
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request body
            data = request.get_json(force=True)
        except Exception as e:
            return jsonify({'error': 'Invalid JSON'}), 400

        # Extract necessary USSD fields from the request
        ussd_id = data.get('USERID', '')
        msisdn = data.get('MSISDN', '')
        user_data = data.get('USERDATA', '')
        msgtype = data.get('MSGTYPE', True)  # True if first request, False if subsequent
        session_id = data.get('SESSIONID', '')  # Extract session ID from the incoming request

        if not session_id:
            return jsonify({'error': 'SESSIONID is missing'}), 400

        if session_id not in sessions:
            sessions[session_id] = {'screen': 1, 'feeling': '', 'reason': ''}

        session = sessions[session_id]

        if msgtype:
            msg = f"Welcome to {ussd_id} USSD Application.\nHow are you feeling?\n1. Feeling fine.\n2. Feeling frisky.\n3. Not well."
            session['screen'] = 1 
            response_data = {
                "USERID": ussd_id,
                "MSISDN": msisdn,
                "USERDATA": user_data,
                "SESSIONID": session_id,
                "MSG": msg,
                "MSGTYPE": True
            }
        else:
            if session['screen'] == 1:
                if user_data == '1':
                    session['feeling'] = 'Feeling fine'
                elif user_data == '2':
                    session['feeling'] = 'Feeling frisky'
                elif user_data == '3':
                    session['feeling'] = 'Not well'
                else:
                    msg = "Invalid input. Please try again!\n\nHow are you feeling?\n1. Feeling fine\n2. Feeling frisky\n3. Not well"
                    response_data = {
                        "USERID": ussd_id,
                        "MSISDN": msisdn,
                        "USERDATA": user_data,
                        "SESSIONID": session_id,
                        "MSG": msg,
                        "MSGTYPE": True
                    }
                    return jsonify(response_data)

                msg = f"Why are you {session['feeling']}?\n1. Money\n2. Relationship\n3. A lot"
                session['screen'] = 2  
                response_data = {
                    "USERID": ussd_id,
                    "MSISDN": msisdn,
                    "USERDATA": user_data,
                    "SESSIONID": session_id,
                    "MSG": msg,
                    "MSGTYPE": True
                }

            elif session['screen'] == 2:
                if user_data == '1':
                    session['reason'] = 'because of money'
                elif user_data == '2':
                    session['reason'] = 'because of relationship'
                elif user_data == '3':
                    session['reason'] = 'because of a lot'
                else:
                    msg = f"Invalid input. Please try again!\n\n. Why are you {session['feeling']}?\n1. Money\n2. Relationship\n3. A lot"
                    response_data = {
                        "USERID": ussd_id,
                        "MSISDN": msisdn,
                        "USERDATA": user_data,
                        "SESSIONID": session_id,
                        "MSG": msg,
                        "MSGTYPE": True
                    }
                    return jsonify(response_data)

                msg = f"You are {session['feeling']} {session['reason']}."
                response_data = {
                    "USERID": ussd_id,
                    "MSISDN": msisdn,
                    "USERDATA": user_data,
                    "SESSIONID": session_id,
                    "MSG": msg,
                    "MSGTYPE": False  
                }

                del sessions[session_id]  

        return jsonify(response_data)

    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
