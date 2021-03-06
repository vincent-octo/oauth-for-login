# Tour d'horizon des plateformes utilisant OAuth pour l'authentification

## Les plateformes testées

Les plateformes testées sont les suivantes :

- [Github] [gh-doc-oauth]
- [Google] [google-doc-oauth]
- [Facebook] [fb-doc-oauth]

Github et Google sont celles qui ont la meilleure documentation.

**Note :** A partir du 1er septembre 2014, Google considère l'authentification via OAuth2 comme obsolète, au profit de OpenID Connect.


## Le processus d'authentification général

Il y a 3 acteurs dans l'authentification :

- l'utilisateur qui veut accéder à une ressource dont l'accès lui est restreint.
- le serveur qui a cette ressource, que nous gérons.
- la plateforme qui authentifie l'utilisateur, que nous ne gérons pas.

Le processus d'authentification suit globalement le schéma suivant :

1. l'utilisateur tente d'accéder à une page dont l'accès lui est restreint.
2. le serveur capte cette requête et redirige l'utilisateur vers la plateforme d'authentification, le serveur doit fournir son `client_id` et (optionnellement) sa `redirect_uri` afin que la plateforme l'identifie.
3. l'utilisateur s'identifie sur la plateforme d'authentification.
4. la plateforme envoie un `code` à usage unique au serveur (un paramètre `state` peut aussi être renvoyé pour éviter des attaques MITM).
5. le serveur renvoie le `code`, ainsi que son `client_id` et `client_secret` (pour prouver son identité) à la plateforme.
6. la plateforme renvoie un `access_token` au serveur.
7. le serveur renvoie cet `access_token` à la plateforme pour obtenir des informations sur l'utilisateur.
8. la plateforme renvoie les informations sur l'utilisateur au serveur.
9. le serveur indique à l'utilisateur qu'il est bien identifié.


## Exemple: Github

A titre d'exemple, j'ai fais un script qui utilise l'authentification sur Github. Vous le trouverez dans le répertoire *flask-oauth*.

Voici les commandes pour créer l'environnement virtuel python et installer les dépendances :
- `virtualenv . -p python3` (ce prototype n'est compatible qu'avec la version 3 de python).
- `source bin/activate` pour activer l'environnement virtuel.
- `pip install Flask`.

Avant de lancer, vous devez [enregistrer une application sur Github] [gh-application-reg]. Dans le champs *Authorization callback URL*, mettre `http://localhost:9090/`.
Après, vous devez renseigner les variables `CLIENT_ID` et `CLIENT_SECRET` dans le fichier *flask-oauth/config.py* (voir leurs valeurs sur Github). Ensuite, deux façons de lancer le script (bien vérifier de les lancer dans l'environnement virtuel) :

- `python flask-oauth/__init__.py`
- `uwsgi --http :9090 -w flask-oauth --callable app --python-path flask-oauth` (si vous avez *uwsgi* installé dans l'environnement virtuel, sinon `pip install uwsgi` pour l'installer).

**Note** : Ceci est un script de démonstration : l'identification n'est pas faite au niveau d'une session, mais est *globale au serveur*... *Ne pas utiliser en production*.


## Les différences entre les plateformes


|                    | Github                                                           | Google (OAuth2 early version)                           | Facebook |
| ------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------- | --- |
| paramètres étape 2 | `client_id`, `redirect_uri` (opt), `scope` (opt), `state` (opt). | `client_id`, `redirect_uri`, `scope`, `response_type`, `state` (opt) | `client_id`, `redirect_uri`, `scope` (opt), `state` (opt), `response_type` (opt) |
| paramètres étape 5 | `code`, `client_id`, `client_secret`, `redirect_uri` (opt)       | `code`, `client_id`, `client_secret`, `redirect_uri`, `grant_type` | `code`, `client_id`, `client_secret`, `redirect_uri` |


[gh-doc-oauth]: https://developer.github.com/v3/oauth/
[google-doc-oauth]: https://developers.google.com/accounts/docs/OAuth2LoginV1
[fb-doc-oauth]: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/v2.0

[gh-application-reg]: https://github.com/settings/applications/new
[oidc-dynamic-reg]: http://openid.net/specs/openid-connect-registration-1_0.html

## Conclusion

Les différentes plateformes testées utilisent le même protocole (OAuth 2) pour faire la même chose : de l'authentification. Cependant, celles-ci ont des différences mineures dans la façon d'utiliser OAuth, ce qui rend impossible l'utilisation d'un système unique pour s'authentifier sur ces plateformes.

Je pense que OpenID Connect est la réponse à ce manque d'uniformité. On notera que les solutions utilisées par ces plateformes ne sont pas très éloignées du standard définit par OpenID Connect.
Un autre avantage d'OpenID Connect est l'extension [Dynamic Registration] [oidc-dynamic-reg], qui définit un processus d'inscription dynamique d'un serveur sur une plateforme qui fournie une authentification.
