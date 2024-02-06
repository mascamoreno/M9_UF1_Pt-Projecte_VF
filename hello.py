from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "FUNCIONA CORRECTAMENTE"

@app.route("/numero/<int:num>")
def numero(num):
    if num % 2 == 0:
        return "PAR"
    else:
        return "IMPAR"

@app.route("/edad/<nombre>/<int:edad>")
def hh(nombre=None, edad=None):
    year = 2023 + 100 - edad
    edad_futura = 100 - edad
    return render_template('WEB.html', age=edad_futura, name=nombre, year=year)

if __name__ == "__main__":
    app.run(debug=True)