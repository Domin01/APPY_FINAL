import requests
import os
from flask import Flask, render_template,abort,session,request
app = Flask(__name__)	
app.secret_key = 'root'
URL_BASE='https://pro-api.coinmarketcap.com/v1'
key=os.environ["Key"]
cabeceras= {'Accepts': 'application/json','X-CMC_PRO_API_KEY': key,}

def inicializa_sesion():
    if session.get("moneda")==None:
        return "USD"
    else:
        return session["moneda"]

@app.route('/',methods=["GET","POST"])
def inicio():
    session["moneda"]=inicializa_sesion()
    if request.method=="POST":
        # Venimos del formulario
        session["moneda"]=request.form.get("divisa")
    url='/cryptocurrency/listings/latest'
    parametros={'start':'1','limit':'10','convert':session["moneda"]}
    r=requests.get(URL_BASE+url,params=parametros,headers=cabeceras)
    if r.status_code == 200:
	    monedas=r.json()
	    return render_template("index.html",lista=monedas,parametros=parametros)
    else:
        abort(404)

@app.route('/convertir',methods=["GET"])
def convertir():
    session["moneda"]=inicializa_sesion()
    parametros={'start':'1','limit':'10','convert':session["moneda"]}
    return render_template("convertir.html",parametros=parametros)

@app.route('/listado',methods=["POST"])
def convertirlista():
    formulario=request.form.get("informacion")
    parametros={'start':'1','limit':'20'}
    url='/fiat/map'
    parametros["limit"] = formulario
    r=requests.get(URL_BASE+url,params=parametros,headers=cabeceras)
    if r.status_code == 200:
	    divisas=r.json()
	    return render_template("convertir.html",formulario=formulario,lista=divisas,parametros=parametros)
    else:
        abort(404)

@app.route('/about',methods=["GET","POST"])
def about():
    session["moneda"]=inicializa_sesion()
    parametros={'start':'1','limit':'10','convert':session["moneda"]}
    return render_template("about.html",parametros=parametros)

@app.route('/listadoabout',methods=["POST"])
def listadoabout():
    formulario=request.form.get("informacion")
    parametros={'start':'1','limit':'10','convert':session["moneda"]}
    url='/cryptocurrency/listings/latest'
    parametros["limit"] = formulario
    r=requests.get(URL_BASE+url,params=parametros,headers=cabeceras)
    if r.status_code == 200:
	    monedas=r.json()
	    return render_template("about.html",formulario=formulario,lista=monedas,parametros=parametros)
    else:
        abort(404)


@app.route('/detalles/<id>')
def detalles(id):
    session["moneda"]=inicializa_sesion()
    url='/cryptocurrency/listings/latest'
    parametros={'start':id,'limit':'1','convert':session["moneda"]}
    r=requests.get(URL_BASE+url,params=parametros,headers=cabeceras)
    if r.status_code == 200:
        monedas=r.json()
        return render_template("detalles.html",lista=monedas,parametros=parametros)
    else:
        abort(404)


app.run('0.0.0.0',debug=True)

#La aplicación web debe tener una vista tipo lista, donde se vea una lista de recursos de la API.
#Debe tener también una vista detalle, donde se vea información concreta de algún recurso de la API.
#Debe tener al menos un formulario para filtrar la información que se muestra.


#La aplicación web debe tener hoja de estilo.
#La aplicación web debe estar desplegada en Heroku.