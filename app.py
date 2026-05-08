from flask import Flask, render_template, request, url_for
from pathlib import Path
from comics import generator
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form.get('title', 'My Comic')
    prompts_raw = request.form.get('prompts', '')
    columns = int(request.form.get('columns', 2))
    # split prompts by newline, ignore empty lines
    prompts = [p.strip() for p in prompts_raw.splitlines() if p.strip()]
    if not prompts:
        prompts = ["Hello, world! This is a sample panel."]

    out_path = generator.generate_comic(prompts, title=title, columns=columns)
    # out_path is relative to project root; make a static URL
    filename = Path(out_path).name
    image_url = url_for('static', filename=f'outputs/{filename}')
    return render_template('result.html', image_url=image_url, title=title)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
