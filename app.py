from flask import Flask,request, render_template
import requests
from config.app_config import site_key, secret_key

app = Flask(__name__, template_folder="./")
def verify(token):
    d={
        'secret':secret_key,
        'response':token,
    }
    url='https://www.google.com/recaptcha/api/siteverify'
    return requests.post(url,data=d).json()

@app.route('/',methods=['GET','POST'])
def recaptcha():
    if request.method == 'POST':
        token = request.values.get('g-recaptcha-response')
        result = verify(token)
        return result
    else:
        return render_template('web.html',site_key=site_key)

if __name__=='__main__':
    app.run(port=5000)
