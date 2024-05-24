from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form-create-app', methods=['POST','GET'])
def form_create_app():
    if request.method == 'POST':
        appName = request.form['appName']
        listenersName = request.form.getlist('listenersName[]')
        listenersProto = request.form.getlist('listenersProto[]')
        listenersProtoPort = request.form.getlist('listenersProtoPort[]')
        treatmentsName = request.form.getlist('treatmentsName[]')
        sendersName = request.form.getlist('sendersName[]')
        dataToSend = {
            'appName' : appName,
            'listenersName' : listenersName,
            'listenersProto' : listenersProto,
            'listenersProtoPort' : listenersProtoPort,
            'treatmentsName' : treatmentsName,
            'sendersName' : sendersName
        }
        try:
            response = requests.post("http://api-admin:5000/create-app", json=dataToSend)
        except requests.exceptions.RequestException as err:
            return render_template('info.html', info_message="Error when sending to api ")
        data = response.json()
        if data['result'] == "0":
            success_list_message = ["Listener container(s) : OK","Treatment container(s) : OK", "Sender container(s) : OK"]
            return render_template('info.html', info_message_list=success_list_message, info_message ="App create and containers launch with success !")
        else: 
            return render_template('info.html', info_message=f"Error !!{data['result']}")
    else:
        return render_template('form-create-app.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)