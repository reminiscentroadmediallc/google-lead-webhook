import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/google-lead-webhook', methods=['POST'])
def receive_google_lead():
    api_key = os.getenv('GOOGLE_WEBHOOK_KEY')
    auth_header = request.headers.get('Authorization')

    # Validate Authorization header
    if auth_header != api_key:
        return json.dumps({'status': 'unauthorized'}), 403

    try:
        payload = request.get_json()

        # Handle both nested and flat formats
        lead = payload.get('lead', payload)

        lead_id = lead.get('lead_id')
        form_id = lead.get('form_id')
        user_data = lead.get('user_column_data', [])

        # Optional: print to server logs
        print("✅ Lead received:")
        print(json.dumps({
            "lead_id": lead_id,
            "form_id": form_id,
            "user_data": user_data
        }, indent=2))

        return json.dumps({'status': 'success'}), 200

    except Exception as e:
        print("❌ Error processing lead:", str(e))
        return json.dumps({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)