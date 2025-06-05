import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/google-lead-webhook', methods=['POST'])
def receive_google_lead():
    expected_key = os.getenv('GOOGLE_WEBHOOK_KEY')
    try:
        payload = request.get_json()

        # ✅ Google sends the key in JSON payload, not headers
        received_key = payload.get('google_key')

        if not received_key or received_key != expected_key:
            return json.dumps({'status': 'unauthorized'}), 403

        lead_id = payload.get('lead_id')
        form_id = payload.get('form_id')
        user_data = payload.get('user_column_data', [])

        # Log the payload (optional)
        print("✅ Google Ads Test Lead Received:")
        print(json.dumps({
            "lead_id": lead_id,
            "form_id": form_id,
            "user_data": user_data
        }, indent=2))

        return json.dumps({'status': 'success'}), 200

    except Exception as e:
        print("❌ Error processing Google Ads lead:", str(e))
        return json.dumps({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)