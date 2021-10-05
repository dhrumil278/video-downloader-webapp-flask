from flask import Flask, url_for,  render_template, redirect, send_file, request, session
from pytube import YouTube
import youtube_dl

app = Flask(__name__)
app.config['SECRET_KEY'] = '27820012782001Ads##'


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/youtube", methods=['POST','GET'])
def youtube():
    if request.method == 'POST':
        session['link'] =request.form.get('url')
        url = YouTube(session['link'])
        return render_template('see_video.html',url=url)
    return render_template('youtube.html')

@app.route("/see_video",methods=['POST','GET'])
def see_video():
    if request.method == 'POST':
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        filename = video.download()
        return send_file(filename , as_attachment = True)
    return reditect(url_for('youtube.html'))

@app.route("/facebook")
def facebook():
    return render_template('facebook.html')

@app.route('/download', methods=["POST", "GET"])
def download():
	url = request.form["url"]
	print("Someone just tried to download", url)
	with youtube_dl.YoutubeDL() as ydl:
		url = ydl.extract_info(url, download=False)
		print(url)
		try:
			download_link = url["entries"][-1]["formats"][-1]["url"]
		except:
			download_link = url["formats"][-1]["url"]
		return redirect(download_link+"&dl=1")
        
if __name__ == "__main__":
    app.run(debug=True)