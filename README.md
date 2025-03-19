# AuthorizationServerDjango
Usando OpenID connect


# El Authorization Code Flow

## Authorization Server (auth_server):
Es un servidor OIDC implementado con Django y el paquete oidc_provider. Este servidor se encarga de autenticar a los usuarios, emitir códigos de autorización y posteriormente tokens (Access Token, ID Token) y responder en el endpoint de UserInfo.

## Cliente OIDC (cliente_auth):
Es una aplicación cliente que utiliza la librería mozilla_django_oidc para iniciar el flujo de autenticación y para validar e intercambiar el código recibido por tokens. Este cliente, tras la autenticación, redirige al usuario a una página de bienvenida protegida.

# Inicio del Flujo en el Cliente
## Solicitud de Autenticación:
El usuario accede a una ruta protegida (por ejemplo, la raíz / del cliente, mapeada a welcome_view y decorada con @login_required).

## Configuración en cliente_auth:
En settings.py se define LOGIN_URL = '/oidc/authenticate/'.
Esto indica que, si el usuario no está autenticado, se redirige a la URL que inicia el proceso OIDC.

# Redirección al Endpoint OIDC del Cliente:
La aplicación cliente redirige al usuario a la URL /oidc/authenticate/ proporcionada por mozilla_django_oidc. Esta URL se encarga de iniciar el proceso de autenticación con el servidor de autorización.

# Solicitud de Autorización al Servidor:
Desde el cliente se genera una redirección al endpoint de autorización del servidor, normalmente con una URL de la forma:
[text](http://localhost:8000/oidc/authorize/?response_type=code&client_id=379909&redirect_uri=<URI_CALLBACK>&scope=openid+profile+email&state=<STATE>)

## Parámetros clave:
response_type=code: Indica que se usará el código de autorización.
client_id: Debe coincidir con el registrado (en este caso '379909').
redirect_uri: La URL a la que el servidor redirigirá con el código.
scope: Define qué información se solicitará (por ejemplo, openid, profile, email).
state: Un parámetro para prevenir ataques CSRF y mantener el estado de la solicitud.

# Validación de la Solicitud y Autenticación del Usuario:

## En auth_server:
El paquete oidc_provider intercepta la solicitud en /oidc/authorize/.
Si el usuario no está autenticado, se redirige al login de Django.

## Pantalla de Login:
Se muestra la plantilla templates/registration/login.html, donde el usuario introduce sus credenciales.
Una vez autenticado mediante django.contrib.auth, se establece la sesión del usuario.

# Generación del Código de Autorización:
Tras la autenticación (y, en flujos con consentimiento, después de aceptarlo), el servidor genera un authorization code.
Este código se asocia a la sesión del usuario y a la solicitud del cliente.

# Redirección al Cliente con el Código:

El servidor redirige al usuario a la redirect_uri especificada por el cliente, adjuntando el parámetro code y, opcionalmente, el parámetro state para vincular la solicitud.

[text](https://cliente-app.com/callback/?code=<AUTH_CODE>&state=<STATE>)

# Solicitud de Token desde el Cliente:
El cliente, de forma backend-to-backend, envía una solicitud HTTP POST al endpoint /oidc/token del servidor.
Parámetros enviados:
grant_type=authorization_code
code=<AUTHORIZATION_CODE>
redirect_uri=<URI_CALLBACK>
Credenciales del cliente (client_id y client_secret)

# Validación y Emisión de Tokens en el Servidor:
El servidor valida que el código recibido sea válido, que la redirect_uri coincida y que las credenciales del cliente sean correctas.
En respuesta, se emiten:
Access Token: Permite acceder a recursos protegidos.
ID Token: Contiene información (claims) acerca del usuario y está firmado con la clave RSA privada configurada en settings.py (la propiedad OIDC_RSA_PRIVATE_KEY).

# Llamada al Endpoint UserInfo:
Con el Access Token obtenido, el cliente puede realizar una petición al endpoint /oidc/userinfo para obtener información detallada sobre el usuario.

# Construcción de Claims en el Servidor:
La función oidc_userinfo definida en auth_server/views.py es la encargada de construir el diccionario de claims.

# Validación y Creación de Sesión en el Cliente:
La librería mozilla_django_oidc en el cliente se encarga de:
Validar el ID Token.
Extraer la información del usuario.
Crear o actualizar la sesión del usuario en el sistema, integrándose con el AUTHENTICATION_BACKENDS definido (incluyendo el backend propio oidc_auth.MyOIDCAuthenticationBackend).

# Acceso a Rutas Protegidas:
Con la sesión autenticada, el usuario puede acceder a rutas protegidas en el cliente.
Por ejemplo, la vista welcome_view (definida en cliente_auth/urls.py) muestra la página de bienvenida.


# Resumen y Consideraciones
En el authorization server, la clave RSA privada (OIDC_RSA_PRIVATE_KEY) se utiliza para firmar los ID Tokens, garantizando la seguridad e integridad de los tokens.
En el cliente, se configuran los endpoints de autorización, token, userinfo y JWKS del servidor, junto con el client_id y client_secret que deben coincidir con los registrados en el servidor.

Seguridad:

El parámetro state es fundamental para mitigar ataques CSRF.
La separación del proceso de autenticación (usuario ingresa credenciales en el servidor) del intercambio de tokens (realizado en el backend del cliente) añade una capa de seguridad al flujo.

# Librerías Utilizadas:
auth_server: Utiliza oidc_provider para ofrecer la infraestructura OIDC.
cliente_auth: Utiliza mozilla_django_oidc para gestionar el inicio de sesión y la integración OIDC en el lado del cliente.

# Esta documentación:
 Abarca todo el recorrido del Authorization Code Flow desde la solicitud inicial en el cliente, pasando por la autenticación y generación del código en el servidor, hasta el intercambio por tokens y la creación de sesión en el cliente


# Los ataques CSRF (Cross-Site Request Forgery), o falsificación de petición en sitios cruzados, son un tipo de ataque en el que un atacante engaña a un usuario autenticado para que ejecute acciones no deseadas en una aplicación web sin su consentimiento.


# (InteractiveConsole)
>>> from django.conf import settings
>>> print(settings.OIDC_RSA_PRIVATE_KEY)
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDGb9CMnlTWn1Cl
4Oe8gdLv06nTW21fxI9VKOUKcNqK5nPmQGHXRP22c/DBLKCKWPBuc1VO8fbMFLU/
LAn0JUKBH3idtuEca2mfUYvtp3tUu25g68jdT/MMD7/9CQgh7gwocuRZxstzYjUz
ab8m4LDmSOkJvna283mgqphbH4l2Yb4cxYXeP6/SL4KpwnEMyNvQ4W5t+Rm3tRtg
y8gDZGOFCgJMncTK/fqQJUGKCDjrykdh/89psA61HE3bf0cV+pBCpfuRkYJsYnB3
uetdF6QSSfqFatjU4PgIKEMcsAvqHD/NdoacqIdouP6CTa5W30Og8mWQMoHnXgj8
kHjXCwqLAgMBAAECggEAVGyc+z6flKI6UyCBJ0vKnRtd7NzAh1aerpoT/CGwcRkD
5Umt9sLU+IuSOfWNJd8aB7vM5yX9nK0QwZwwbe1uQnZLwDnew1MVoGE22bkAOTf3
CYg3MKVDn/WRdouhqKHZDVp4OZPg2inFvaZ3W4iL6qXJc8pTQpoKvKbn5BjiSHkk
IbJOOBaM8GSHsfrDKfdoKEWlY8R2NIyc+oAUIfzaCAAkQQDxDK9cqcS0bnlVuJTg
m5weE44kOY81aRRM/pskFoKo/jF968khaHD8SCq1dGUjTigx6HASa+HepKBOo1a5
3aH30g6HOJpU0ypXOZYIj+8BgNhJ5d5QX8L79/KkUQKBgQDvY6eXI3HOgk4Kf4iX
lTzRobIo+Hgalb8XwKzzzx+aqeO/j9aALN1EYC0J20wuoCAtB7bpP7Vb9LCPK5Ni
XkmZDzg66dQpQv25ZRTa3pG0xXy+sA1XQT42sb0dqNP0Ww73j2T93J63/03ZD5WL
lYsujDvhWkN3yH0LrKcpF/M7UQKBgQDUNLVIq+oEJ+oZXfamTAkpnqcwG8Ve4p7K
bdHWUeNS8gl9DTlRmCt8x5G7qKPmi0SCWIPpJXbyhz6RcXoW52Mn/BvMqnPv/a9Z
TXwToNa09xHUovWeQOg1iHRVAMWCCw1mUT/7tcZhKkOOivrFSz+1HguSyZmShuue
i7hgkBL5GwKBgH/1fcSM/q1K+5oi94lHDV5klw3NWq2jM6TnqcsdAKC0hPeFVDvp
P1DoM8rb/MnDb8+CGyRsmG2RyrqMqVhgW+jDuOPMz0pK88KgpFglti6xjW+EPW1R
g4bK1PLApqMr9UEg1fPYdMKXZi5LZT1aby4vaWaY0A18DlMqM6QEmFAxAoGAGFif
v+GxbJ6jthtYtAWfO34vUk6tW1CGxVTKMVudyCNqwUUmIV1jB+LhrnUPsOCjkIzV
PYeF2Rd5LzikuEH911WOXvHjcVJartU7+giG+aYrDolPwsNRoOqx5hq7jkr0U5vY
ymk1hGpT6+O4F7Clc4Mp8sJcczo1iDAhjDqbYqcCgYAFfSmae1RyHDqM1U0fKrHu
RSlMtKZg5LeEs/XhUYDmGD0exmpNTDXaqG5/FFDr9LDPFwwKppzeCGK8cRIN5wvk
swfX5JVk8wa9wijr0dattgDru2OClXmSWM7JBb7KeNAJxBld3dGEVmAzqmVinKvC
MmaqhBA+k6+5KvbUZU/Jqw==
-----END PRIVATE KEY-----
>>> from oidc_provider.models import RSAKey
>>> print(RSAKey.objects.all())
<QuerySet []>
>>> from oidc_provider.models import RSAKey
>>> from django.conf import settings
>>> RSAKey.objects.create(key=settings.OIDC_RSA_PRIVATE_KEY)
<RSAKey: a8080b6bbfb4996db4cba76fdb1d1d0c>
>>> print(RSAKey.objects.all())
<QuerySet [<RSAKey: a8080b6bbfb4996db4cba76fdb1d1d0c>]>
>>>