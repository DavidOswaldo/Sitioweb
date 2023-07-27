import os
from flaskext.mysql import MySQL  # se importa Mysql
from flask import Flask  # SE IMPORTAN LAS LIBRERIAS DEL FLASK
# request y dierect recepcionan y redireccion la informacion
from flask import render_template, request, redirect,session    #sesiones para que se pueden guarar
from flask import send_from_directory  #nos permite la obtenrr la informacion de la imagen
app = Flask(__name__)

app.secret_key="DEVOLOTECA"



from datetime import datetime # se importa la aplicacion de imageb y no se contraponga la imagen con el tiempo

# Realizando la conexion con la base de datos

# se genera la variable que va realizar la conexion
mysql = MySQL(app)
# donde se encuentra la base de datos, #creando la conexion se nesecita el usuario y contraseña
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'  # usuario de la base de datos
# password de usuario de la base de datos
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sitio'  # nombre de la base de datos
mysql.init_app(app)  # iniciando la conexion


# SE REALIZA EL RENDER DE HTML EN LAS CABECERAS DEL MENU, se genera la rutas de navegacion
@app.route('/')
def inicio():
    return render_template('sitio/index.html')  # ruta de acceeso del render

# ruta donde se van a mostrar las imagenes del sitio cargadas
@app.route('/imgs/<imagen>')
def imagenes(imagen): #funcion
    print(imagen)
    return send_from_directory(os.path.join('Templates/sitio/imgs'),imagen)

# carga del archivo css
@app.route("/css/<archivocss>")
def css_link(archivocss):
    return send_from_directory(os.path.join('Templates/sitio/css'),archivocss)




@app.route('/libros')
def libros():
    
    conexion = mysql.connect()  # variable para saber si se conecto la base de datos
    cursor = conexion.cursor()  # almacena o ejecuta la funcion
    cursor.execute("SELECT * FROM libros")  # ejecutla la consulta en la tabla
    libros= cursor.fetchall() # esta variable a almacena toda la informacion que esta en la base de datos
    conexion.commit()
    print(libros)
    return render_template('sitio/libros.html',libros=libros)
    




@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')


@app.route('/admin/')
def admin_index():
    
     #evalua que si existe login en variables de sesion accede , si no existe no permira el acceso 
    if not 'login' in session:
        return redirect("/admin/login")
    
    return render_template('admin/index.html')

# login sencillo
@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

#LOGIN

@app.route ('/admin/login',methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario'] #recibe los datos del formulario se envia la informacion
    _password=request.form['txtPassword']
    print(_usuario)
    print(_password)
    
    #se valida la informacion que se envia 
    if _usuario=="admin" and _password =="123":
        #variable de sesion el cual validara si el usuario se registro
        session["login"]=True
        session["usuario"]="Administrador"
        return redirect ("/admin")
    
    
    return render_template('admin/login.html',mensaje="Acceso denagado")

#cierre de sesion 
@app.route('/admin/cerrar')
def admind_login_cerrar():
    session.clear()
    return redirect('/admin/login')
    

@app.route('/admin/libros')
def admin_libros():
    
    #evalua que si existe login en variables de sesion accede , si no existe no permira el acceso 
    if not 'login' in session:
        return redirect("/admin/login")
    
    
    conexion = mysql.connect()  # variable para saber si se conecto la base de datos
    cursor = conexion.cursor()  # almacena o ejecuta la funcion
    cursor.execute("SELECT * FROM libros")  # ejecutla la consulta en la tabla
    # esta variable a recurperar toda la informacion que esta en la base de datos
    libros = cursor.fetchall()
    conexion.commit()
    print(libros)

    # se agregan la variable de libros para que sea leida dentro del template
    return render_template('admin/libros.html', libros=libros)

# ruta que recepciona todo lo que envie el metodo POST, biene del formulario llenado


@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    if not 'login' in session:
     return redirect("/admin/login")
    

    # request toma la cadena de caracter que se pone el formulario form
    # request file toma el archivo que se adjunta

    _nombre = request.form['txtnombre']
    _url = request.form['txtURL']
    _archivo = request.files['txtimagen']
    
    
    #Variable de tiempo para que no se encimen las imagenes
    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%S') #formato de tiempo
    # cambia el nombre del archivo y se guarda el archivo en temporales de imagenes del sitio web
    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("Templates/sitio/imgs/"+nuevoNombre)
        
               
        
        
    # se ejecuta la conexion sql
    # se colcoa %s porque es datoa que va ingresar a la db, insercion de datos
    sql = "INSERT INTO libros(ID,NOMBRE,IMAGEN,URL) VALUES(NULL,%s,%s,%s);"
    # variable donde se remplazan los datos  de acuerdo al ordern que colocraon el qwerty
    datos = (_nombre,nuevoNombre, _url)
    conexion = mysql.connect()  # se abre la  conexion
    cursor = conexion.cursor()  # se genera un cursor
    cursor.execute(sql, datos)  # cursor ejecuta la instruccion sql
    conexion.commit()  # se realiza la intruccion

    print(_nombre)
    print(_url)
    print(_archivo)

    return redirect('/admin/libros')


# Borrado de registro de base

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():  # definicion de funcion
    _id = request.form['txtID']  # variable que recepciona el dato
    print(_id)
    
    #se guridad de login y valida si esta logeado
    if not 'login' in session:
        return redirect("/admin/login")    

    conexion = mysql.connect()  # variable para saber si se conecto la base de datos
    cursor = conexion.cursor()  # almacena o ejecuta la funcion
    # ejecutla la consulta en la tabla
    cursor.execute("SELECT imagen FROM libros WHERE id=%s", (_id)) # esta variable a recurperar toda la informacion que esta en la base de datos
    libros = cursor.fetchall()
    conexion.commit()
    print(libros)
    
    
    if os.path.exists("Templates/sitio/imgs/"+str(libros[0][0])):
        os.unlink("Templates/sitio/imgs/"+str(libros[0][0]))
        
        
        
        

    conexion = mysql.connect()  # variable para saber si se conecto la base de datos
    cursor = conexion.cursor()  # almacena o ejecuta la funcion
    cursor.execute("DELETE FROM libros WHERE id=%s", (_id))
    conexion.commit()
   
   
    return redirect('/admin/libros')  # regresea a la ruta


# Ruta de prueba para verificar la conexión
@app.route('/test')
def test():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Ejemplo de consulta
        cursor.execute('SELECT * FROM libros')
        data = cursor.fetchall()

        # Imprimir los resultados
        for row in data:
            print(row)

        return 'Conexión exitosa y consulta realizada correctamente.'
    except Exception as e:
        return f'Error de conexión: {str(e)}'


# condicional donde se correr filtros
if __name__ == 'main':
    app.run(debug=True)
