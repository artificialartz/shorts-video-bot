from flask import Flask, request, jsonify
from video_bot import create_video

app = Flask(__name__)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.get_json()
    topic = data.get('topic')
    script = data.get('script')

    if not topic or not script:
        return jsonify({'error': 'Missing topic or script'}), 400

    video_url = create_video(topic, script)
    return jsonify({'video_url': video_url}), 200

if __name__ == '__main__':
    app.run()