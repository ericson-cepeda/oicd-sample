from django.http import HttpResponse, HttpResponseRedirect
import json

from oic.oic import Client
from oic.oauth2 import rndstr
from oic.oic.message import AuthorizationResponse
from oic.utils.authn.client import ClientSecretPost


llave = 'f4sOu4LoJPDDyVZ4abPrfEq51E0a' #'1NqWfYRxI7BraM9F7EBva8dzHBYa'
secreto = 'fyX1eLbWZD9ImUSNIg28Ns2eIH0a' #'VwWRH3cLPj2xoVMFRbT0Q9ZLVpYa'
endpoint_autorizacion = 'https://190.184.205.151:9443/oauth2/authorize' #'https://localhost:9443/oauth2/authorize/'
endpoint_token = 'https://190.184.205.151:9443/oauth2/token' #'https://localhost:9443/oauth2/token/'
callback = 'http://localhost:8000/pedir-token/'


def inicio(request):
	return HttpResponse('<a href="/pedir-autorizacion/">Inicia Sesion</a>')


def pedir_autorizacion(request):
	cliente = Client()
	hapax = rndstr()
	estado = rndstr()
	parametros = {
		"authorization_endpoint": endpoint_autorizacion,
		"client_id": llave,
		"response_type": "code",
		"scope": ["openid"],
		"nonce": hapax,
		"redirect_uri": callback
	}
	resultado = cliente.do_authorization_request(
		state=estado,
		request_args=parametros
	)
	request.session['estado'] = estado
	return HttpResponseRedirect(resultado.headers['location'])


def pedir_token(request):
	cliente = Client(
		client_id=llave,
		client_authn_method={"client_secret_post": ClientSecretPost}
	)
	respuesta_cruda = json.dumps(dict(request.GET))
	respuesta = cliente.parse_response(AuthorizationResponse, info=respuesta_cruda)
	estado_recibido = respuesta['state']
	estado_almacenado = request.session['estado']
	if estado_recibido == estado_almacenado:
		codigo = respuesta['code']
		parametros = {
			"token_endpoint": endpoint_token,
			"code": codigo,
			"client_id": llave,
			"client_secret": secreto,
			"redirect_uri": callback
		}
		resultado = cliente.do_access_token_request(
			scope = ["openid"],
			state = estado_recibido,
			request_args = parametros,
			authn_method = "client_secret_post"
		)
		usuario = resultado['id_token']['sub']
		cedula = usuario[:usuario.find('@')]
		return HttpResponse("Bienvenido, usuario {}".format(cedula))
	else:
		return HttpResponse("Error: el estado enviado al endpoint de autorizacion no corresponde con el recibido.")