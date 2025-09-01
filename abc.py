from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import get_rag_response

app = Flask(__name__)
CORS(app)  # Allow frontend access


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message')
    
    if not query:
        return jsonify({"error": "Message is required"}), 400
    
    try:
        answer = get_rag_response(query)
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
