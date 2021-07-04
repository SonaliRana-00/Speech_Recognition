from flask import Flask, app, render_template, request, redirect
import googletrans
import speech_recognition as sr
from googletrans import Translator




app= Flask(__name__)

@app.route("/" , methods= ["GET", "POST"])
def index():
    transcript = ""
    lang = ""
    convert_text=""
    dest_lang=""
    if request.method == "POST":
        print("FORM DATA RECIEVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audiofile = sr.AudioFile(file)
            with audiofile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            translator = Translator()
            dest_lang = request.form['language']
            lang = str(translator.detect(transcript))
            if dest_lang in googletrans.LANGCODES:
                l1 = googletrans.LANGCODES[dest_lang]
                convert_text = translator.translate(transcript, dest=l1)


            



    return render_template("index.html" , transcript= transcript, LANGUAGES = googletrans.LANGUAGES , lang = lang , convert_text = convert_text, dest_lang = dest_lang )



if __name__ == "__main__":
    app.run(debug=True)