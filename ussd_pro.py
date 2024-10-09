import os
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


        result = user_data.split('*')
        real_user_data_array = []

        if not session_id:
            return jsonify({'error': 'SESSIONID is missing'}), 400

        # Retrieve or initialize the session based on the provided SESSIONID
        if session_id not in sessions:
            sessions[session_id] = {'screen': 1, 'feeling': '', 'reason': ''}

        session = sessions[session_id]

        # Check the length of the array
        if len(result) > 2:
            # Ignore the first 2 elements and take the rest
            remaining_elements = result[3:]
            real_user_data_array = remaining_elements
            print(real_user_data_array)
            # accessing the selecting from the first screen directly
            if len(real_user_data_array) == 1:
                real_user_data_string = real_user_data_array[0].replace("#", "")
                print(real_user_data_string)
                
                session['screen'] = 2  # Set the screen to 2

                if real_user_data_string == '1':
                    session['feeling'] = 'Feeling fine'
                elif real_user_data_string == '2':
                    session['feeling'] = 'Feeling frisky'
                elif real_user_data_string == '3':
                    session['feeling'] = 'Not well'
                # Invalid input, repeat Screen 1
                else:
                    msg = "Invalid input. Please try again!\n\nHow are you feeling?\n1. Feeling fine\n2. Feeling frisky\n3. Not well"
                    response_data = {
                        "USERID": ussd_id,
                        "MSISDN": msisdn,
                        "USERDATA": user_data,
                        "MSG": msg,
                        "MSGTYPE": True
                    }
                    return jsonify(response_data)
            
                msg = f"Why are you {session['feeling']}?\n1. Money\n2. Relationship\n3. A lot"
                response_data = {
                    "USERID": ussd_id,
                    "MSISDN": msisdn,
                    "USERDATA": real_user_data_string,
                    "MSG": msg,
                    "MSGTYPE": True
                }
                return jsonify(response_data)
            

            elif len(real_user_data_array) == 2:

                # print(real_user_data_array)
                # Ignore the first 2 elements and take the rest
                remaining_elements = result[3:]
                real_user_data_array = remaining_elements
                print(real_user_data_array)

                real_user_data_sanitized_array = list(set(item.replace('#', '') for item in real_user_data_array))
                print(real_user_data_sanitized_array[-1])
                print(real_user_data_sanitized_array[0])

                session['screen'] = 3  # Set the screen to 3

                if real_user_data_sanitized_array[-1] == '1':
                    session['feeling'] = 'Feeling fine'
                elif real_user_data_sanitized_array[-1] == '2':
                    session['feeling'] = 'Feeling frisky'
                elif real_user_data_sanitized_array[-1] == '3':
                    session['feeling'] = 'Not well'
                else:
                    # Invalid input, repeat Screen 1
                    session['screen'] = 1  # Set the screen to 1
                    msg = "Invalid input. Please try again!\n\nHow are you feeling?\n1. Feeling fine\n2. Feeling frisky\n3. Not well"
                    response_data = {
                        "USERID": ussd_id,
                        "MSISDN": msisdn,
                        "USERDATA": user_data,
                        "MSG": msg,
                        "MSGTYPE": True
                    }
                    return jsonify(response_data)


                # Process the user's input from Screen 2
                if real_user_data_sanitized_array[0] == '1':
                    session['reason'] = 'because of money'
                elif real_user_data_sanitized_array[0] == '2':
                    session['reason'] = 'because of relationship'
                elif real_user_data_sanitized_array[0] == '3':
                    session['reason'] = 'because of a lot' 
                else:
                    # Invalid input, repeat Screen 1
                    session['screen'] = 2 
                    msg = f"Invalid input. Please try again!\n\n Why are you {session['feeling']}?\n1. Money\n2. Relationship\n3. A lot"
                    response_data = {
                        "USERID": ussd_id,
                        "MSISDN": msisdn,
                        "USERDATA": user_data,
                        "MSG": msg,
                        "MSGTYPE": True
                    }
                    return jsonify(response_data)
                
                # Move to Screen 3: Summarize the user's input
                msg = f"You are {session['feeling']} {session['reason']}."
                response_data = {
                    "USERID": ussd_id,
                    "MSISDN": msisdn,
                    "USERDATA": user_data,
                    "MSG": msg,
                    "MSGTYPE": True  # Final message, end session
                }

                print(session)

                msg = f"You are {session['feeling']} {session['reason']}."
                response_data = {
                    "USERID": ussd_id,
                    "MSISDN": msisdn,
                    "USERDATA": user_data,
                    "MSG": msg,
                    "MSGTYPE": False  # Final message, end session
                }
                return jsonify(response_data)


        # Initial request (first screen)  
        if msgtype:
            # Screen 1: Ask how the user is feeling
            msg = f"Welcome to {ussd_id} USSD Application.\nHow are you feeling?\n1. Feeling fine.\n2. Feeling frisky.\n3. Not well."
            session['screen'] = 1  # Set the screen to 1
            response_data = {
                "USERID": ussd_id,
                "MSISDN": msisdn,
                "USERDATA": user_data,
                "MSG": msg,
                "MSGTYPE": True  
            }
        else:
            # Handle the interaction based on the current screen
            if session['screen'] == 1:
                # Process the user's input from Screen 1
                if user_data == '1':
                    session['feeling'] = 'Feeling fine'
                elif user_data == '2':
                    session['feeling'] = 'Feeling frisky'
                elif user_data == '3':
                    session['feeling'] = 'Not well'
                else:
                    # Invalid input, repeat Screen 1
                    msg = "Invalid input. Please try again!\n\nHow are you feeling?\n1. Feeling fine\n2. Feeling frisky\n3. Not well"
                    response_data = {
                        "USERID": ussd_id,
                        "MSISDN": msisdn,
                        "USERDATA": user_data,
                        "MSG": msg,
                        "MSGTYPE": True
                    }
                    return jsonify(response_data)

                # Move to Screen 2: Ask why the user feels that way
                msg = f"Why are you {session['feeling']}?\n1. Money\n2. Relationship\n3. A lot"
                session['screen'] = 2  # Set the screen to 2
                response_data = {
                    "USERID": ussd_id,
                    "MSISDN": msisdn,
                    "USERDATA": user_data,
                    "MSG": msg,
                    "MSGTYPE": True
                }

            elif session['screen'] == 2:
                # Process the user's input from Screen 2
                if user_data == '1':
                    session['reason'] = 'because of money'
                elif user_data == '2':
                    session['reason'] = 'because of relationship'
                elif user_data == '3':
                    session['reason'] = 'because of a lot'
                else:
                    # Invalid input, repeat Screen 2
                    msg = f"Invalid input. Please try again!\n\n. Why are you {session['feeling']}?\n1. Money\n2. Relationship\n3. A lot"
                    response_data = {
                        "USERID": ussd_id,
                        "MSISDN": msisdn,
                        "USERDATA": user_data,
                        "MSG": msg,
                        "MSGTYPE": True
                    }
                    return jsonify(response_data)

                # Move to Screen 3: Summarize the user's input
                msg = f"You are {session['feeling']} {session['reason']}."
                response_data = {
                    "USERID": ussd_id,
                    "MSISDN": msisdn,
                    "USERDATA": user_data,
                    "MSG": msg,
                    "MSGTYPE": False  # Final message, end session
                }

                # End the session after Screen 3
                del sessions[session_id]
        print(response_data)
        return jsonify(response_data)

    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # Get the port from the environment variable
    app.run(host="0.0.0.0", port=port, debug=True)  # Bind to 0.0.0.0
