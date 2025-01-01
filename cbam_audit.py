from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for submissions
clients_data = {}

@app.route('/submit_data', methods=['POST'])
def submit_data():
    """Endpoint for clients to submit data for CBAM validation."""
    client_id = request.json.get('client_id')
    data = request.json.get('data')

    if not client_id or not data:
        return jsonify({'error': 'Client ID and data are required.'}), 400

    # Generate a unique submission ID
    submission_id = f"SUB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    clients_data[submission_id] = {
        'client_id': client_id,
        'data': data,
        'status': 'Pending',
        'timestamp': datetime.now().isoformat()
    }

    return jsonify({'submission_id': submission_id, 'status': 'Data submitted successfully.'}), 200

@app.route('/approve_submission', methods=['POST'])
def approve_submission():
    """Endpoint to approve a submission by ID."""
    submission_id = request.json.get('submission_id')

    if not submission_id or submission_id not in clients_data:
        return jsonify({'error': 'Submission ID not found.'}), 404

    # Approve the submission
    clients_data[submission_id]['status'] = 'Approved'
    certificate = f"CERT-{submission_id}"
    return jsonify({'submission_id': submission_id, 'certificate': certificate, 'status': 'Approved'}), 200

@app.route('/compliance_dashboard', methods=['GET'])
def compliance_dashboard():
    """Provide a summary of the compliance dashboard."""
    total_submissions = len(clients_data)
    approved_submissions = sum(1 for item in clients_data.values() if item['status'] == 'Approved')
    pending_submissions = total_submissions - approved_submissions

    return jsonify({
        'dashboard': {
            'total_submissions': total_submissions,
            'approved': approved_submissions,
            'pending': pending_submissions
        }
    }), 200

@app.route('/submission_status/<submission_id>', methods=['GET'])
def submission_status(submission_id):
    """Get the status of a specific submission."""
    if submission_id not in clients_data:
        return jsonify({'error': 'Submission ID not found.'}), 404

    return jsonify(clients_data[submission_id]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
