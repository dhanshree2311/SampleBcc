from flask import Flask, request, jsonify
import requests
import base64
import streamlit as st
import tempfile

app = Flask(__name__)
port = 5000

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)
        image = base64.b64encode(open(temp_file.name, 'rb').read()).decode('utf-8')
    
    payload = {'api_key': 'hNxL7WL0izjJWYujiYSe'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = 'https://detect.roboflow.com/bcc-stages-hm5pr/1'
    
    try:
        response = requests.post(url, params=payload, data=image, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    st.title('Skin Disease Classification')
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    
    if st.button('Classify'):
        if uploaded_file is not None:
            try:
                files = {'image': uploaded_file}
                response = requests.post(f'http://localhost:{port}/classify', files=files)
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.json()['error']}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please upload an image file")

if __name__ == '__main__':
    app.run(debug=True, port=port)
