# Importation des modules nécéssaires
import os
import json
import jinja2
import jinja2tool
import jinja2plugin
import cherrypy
from cherrypy.lib.static import serve_file

ROOT = os.path.abspath(os.getcwd()) # retourne le dossier où se trouve ce fichier

# Classe principale pour cherrypy
class flightFinder():

    # Déclaration des variables générales où se trouvent les dictionnaires
    def __init__(self):
        self.arrivals = self.openArrivals()
        self.departures = self.openDepartures()

    # Définit la route vers l'index du site (/) 
    @cherrypy.expose
    def index(self):
        return 

    # Défini la route vers les pages inconnues (404) et renvoie la page statique
    @cherrypy.expose
    def default(self, attr=''):
        return serve_file(os.path.join(ROOT, 'static/404.html'))

    # Défini la route vers la page des résultats
    @cherrypy.expose
    def results(self, q=False): # q contient ce qui a été renvoyé par le formulaire de la page d'acceuil

        # Déclaration de 2 listes qui vont servir à stocker les résultats trouvés
        results_arrivals = []
        results_departures = []

        if q: # si le formulaire n'est pas vide on continue, si il l'est, ce sera géré par jinja2 dans le fichier html
            for i in range(len(self.arrivals)):
                for j in self.arrivals[i]: # on itère sur toutes les entrées de la liste qui contient les dictionnaires 
                    if q.lower() in self.arrivals[i][j].lower() and self.arrivals[i] not in results_arrivals: # et on compare la valeure du formulaire avec toutes les valeures dans tous les dictionnaires et on fait attention aussi à ne pas avoir de doublons
                        results_arrivals.append(self.arrivals[i]) # on ajoute à la liste le dictionnaire dans lequel se trouve la valeur qui correspond à la recherche

            for i in range(len(self.departures)): # parreil pour les départs
                for j in self.departures[i]:
                    if q.lower() in self.departures[i][j].lower() and self.departures[i] not in results_departures:
                        results_departures.append(self.departures[i])


        return {'form': q, 'arrivals': results_arrivals, 'departures': results_departures} # on renvoie le contenu du formulaire et les résultats des eux dictionnaires à jinja2

    # Fonctions qui ouvrent les dictionnaires
    def openDepartures(self):
        try:
            with open('static/departures.json', 'r') as departuresFile:
                departures = json.load(departuresFile)
                return departures
        except:
            cherrypy.log('[ERROR] Failed loading database.')
            return []

    def openArrivals(self):
        try:
            with open('static/arrivals.json', 'r') as arrivalsFile:
                arrivals = json.load(arrivalsFile)
                return arrivals
        except:
            cherrypy.log('[ERROR] Failed loading database.')
            return []


# Enregistrer le plugin et tool jinja2
ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe ()
cherrypy.tools.template=jinja2tool.Jinja2Tool()

cherrypy.quickstart(flightFinder(), '', 'server.conf') # lancement du serveur cherrypy avec le fichier de configuration
