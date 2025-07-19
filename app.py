from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import yt_dlp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DOWNLOAD_FOLDER = "static/downloaded"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['url']
        if not youtube_url:
            flash('Please enter a YouTube URL.')
            return redirect(url_for('index'))

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                filename = ydl.prepare_filename(info)
                mp3_file = os.path.splitext(filename)[0] + '.mp3'
                title = info.get('title', 'audio')

            flash(f"Downloaded: {title}")
            return render_template('index.html', title=title, mp3_file=os.path.basename(mp3_file))

        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
