from flask import Flask, request, jsonify, render_template 

app = Flask(__name__)

def ajouter_donnees_fichier(donnees):
    # Ouvrir le fichier en mode 'a' (append) pour ajouter les données à la fin
    with open('donnees.txt', 'a') as fichier:
        fichier.write(donnees + '\n')  # Ajouter les données suivies d'un saut de ligne

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recevoir-donnees', methods=['POST'])
def recevoir_donnees():
    if request.method == 'POST':
        donnees_recues = request.get_data(as_text=True)  # Récupérer les données POST
        ajouter_donnees_fichier(donnees_recues)  # Appeler la fonction pour ajouter les données au fichier
        return 'Données ajoutées au fichier avec succès'
    else:
        return 'Méthode non autorisée'
    

@app.route('/form', methods=['POST'])
def form():
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'message': request.form['message']
    }
    # Vous pouvez effectuer d'autres opérations ici avec les données reçues

    # Conversion des données en JSON
    json_data = jsonify(data)

    # Vous pouvez également envoyer les données à une autre URL ou effectuer d'autres actions ici

    return json_data, render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")