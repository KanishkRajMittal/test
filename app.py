# app.py
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/potd', methods=['POST','GET'])
def POTD():
    try:
        # Run your Python script using subprocess
        result = subprocess.run(['python3', 'potd.py'], capture_output=True, text=True)
        output = result.stdout
        return jsonify({'success': True, 'output': output})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)

#https://profile-mfru.onrender.com/update
