# Tour d'horizon des plateformes utilisant OAuth pour l'authentification

Les différentes plateformes testées utilisent le même protocole (OAuth 2) pour faire la même chose : de l'authentification. Cependant, celles-ci ont des différences mineures dans la façon d'utiliser OAuth, ce qui rend impossible l'utilisation d'un système unique pour s'authentifier sur ces plateformes.

Je pense que OpenID Connect est la réponse à ce manque d'uniformité. On notera que les solutions utilisées par ces plateformes ne sont pas très éloignées du standard définit par OpenID Connect.
Un autre avantage d'OpenID Connect est l'extension [Dynamic Registration] [oidc-dynamic-reg], qui définit un processus d'inscription dynamique d'un serveur sur une plateforme qui fournie une authentification.


## Les plateformes testées

Les plateformes testées sont les suivantes :

- [Github] [gh-doc-oauth]
- [Google] [google-doc-oauth]
- [Facebook] [fb-doc-oauth]
- Twitter

Parmi celles-ci, Github et Google sont celles qui ont la meilleure documentation.

**Note :** Google met fin à l'authentification via OAuth2 au 1er septembre 2014, au profit de OpenID Connect.


## Le processus d'authentification général

Il y a 3 acteurs dans l'authentification :

- l'utilisateur qui veut accéder à une ressource dont l'accès est restreint.
- le serveur qui a cette ressource (que nous gérons).
- la plateforme qui authentifie l'utilisateur (que nous ne gérons pas).

Le processus d'authentification suit globalement le schéma suivant, pour les plateformes d'authentification :

1. l'utilisateur tente d'accéder à une page dont l'accès est restreint.
2. le serveur capte cette requête et redirige l'utilisateur vers la plateforme d'authentification, le serveur doit fournir son *client id* et (optionnellement) sa *redirect URI* afin que la plateforme l'identifie.
3. l'utilisateur s'identifie sur la plateforme d'authentification.
4. la plateforme envoie un *code* à usage unique au serveur.
5. le serveur renvoie le *code*, ainsi que son *client id* et *client secret* (pour prouver son identité) à la plateforme.
6. la plateforme renvoie un *access token* au serveur.
7. le serveur renvoie cet *access token* à la plateforme pour obtenir des informations sur l'utilisateur.
8. la plateforme renvoie les informations sur l'utilisateur au serveur.
9. le serveur indique à l'utilisateur qu'il est bien identifié.


## Exemple: Github

A titre d'exemple, j'ai fais un script qui utilise l'authentification sur Github. Vous le trouverez dans le répertoire *flask-oauth*.

Voici les commandes pour créer l'environnement virtuel python et installer les dépendances :
- `virtualenv . -p python3` (ou, si vous ne voulez pas utiliser python 3 : `virtualenv .`).
- `source bin/activate`.
- `pip install Flask`.

Avant de lancer, vous devez [enregistrer une application sur Github] [gh-application-reg]. Dans le champs *Authorization callback URL*, mettre `http://localhost:9090/`.
Après, vous devez renseigner les variables `CLIENT_ID` et `CLIENT_SECRET` dans le fichier *flask-oauth/config.py* (voir leurs valeurs sur Github). Ensuite, deux façons de lancer le script :

- `python flask-oauth/__init__.py`.
- `uwsgi --http :9090 -w flask-oauth --callable app --python-path flask-oauth` (si vous avez *uwsgi* installé, sinon `pip install uwsgi`).

**Note** : Ceci est un script de démonstration : l'identification n'est pas contrainte à une session, mais est *globale au serveur*.


## Les différences entre les plateformes



[gh-doc-oauth]: https://developer.github.com/v3/oauth/
[google-doc-oauth]: https://developers.google.com/accounts/docs/OAuth2LoginV1
[fb-doc-oauth]: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/v2.0

[gh-application-reg]: https://github.com/settings/applications/new
[oidc-dynamic-reg]: http://openid.net/specs/openid-connect-registration-1_0.html
