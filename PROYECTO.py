from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'se_la_saben_todos'

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="Jose Manuel",
    password="JoseManuel",
    database="usuario"
)
cursor = db.cursor()

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM login WHERE Email = %s AND Contraseña = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = user[1]
            return redirect(url_for('privado'))
        else:
            return render_template('login.html', message='Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO nommail (Nombre, contraseña) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/public-section')
def public():
    return render_template('dashboard.html')

# Ruta para el formulario de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        # Insertar el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO login (email, contraseña) VALUES (%s, %s)", (email, contraseña))
        db.commit()
        
        return redirect(url_for('registro_exitoso'))
    return render_template('registro.html')

# Ruta para la página de registro exitoso
@app.route('/registro_exitoso')
def registro_exitoso():
    return '¡Registro exitoso!'

@app.route('/privado')
def privado():
    return render_template('privado.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacto', methods=['POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        
        # Insertar el mensaje en la base de datos
        cursor.execute("INSERT INTO sugerencias (nombre, email, comentario) VALUES (%s, %s, %s)", (nombre, email, mensaje))
        db.commit()
        
        return 'Mensaje enviado correctamente'


if __name__ == '__main__':
    app.run(debug=True)