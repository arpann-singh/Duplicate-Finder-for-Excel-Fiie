from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

def find_duplicates(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        duplicates = df[df.duplicated(keep=False)]
        if 'Name' in df.columns:
            duplicates = duplicates.sort_values(by='Name')
        else:
            duplicates = duplicates.sort_values(by=df.columns[0])
        return duplicates.to_dict(orient='records')
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return "Flask app is running"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        sheet_name = request.form.get('sheet_name')
        duplicates = find_duplicates(file_path, sheet_name)
        if isinstance(duplicates, str):  # Error handling
            return jsonify({'error': duplicates})
        return jsonify({'duplicates': duplicates})

if __name__ == "__main__":
    app.run(debug=True)
