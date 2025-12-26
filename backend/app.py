import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/app', methods=['GET'])
def get_makefile_output():
    try:
        output = subprocess.check_output(['make'])
        return jsonify({'output': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Makefile execution failed with return code {e.returncode}'})

if __name__ == '__main__':
    app.run(debug=True)