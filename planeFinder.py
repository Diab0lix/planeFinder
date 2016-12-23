import json
from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button

class planeFinder(App):
    def build(self):
        self.title = 'Plane Finder' # Titre de la fenêtre
        grid = GridLayout(cols=2) # On veut un layout style grille avec 2 colonnes

        # Déclaration des boutons, labels et champs de texte
        self.arrival = ToggleButton(text='Arrival', group='type', state='down')
        self.departure = ToggleButton(text='Departure', group='type')
        self.flight = TextInput(multiline=False)
        self.carrier = TextInput(id='carrier', multiline=False)
        self.destination = TextInput(id='dest', multiline=False)
        self.time = TextInput(id='time', multiline=False)
        self.codeshare = TextInput(id='codeshare', multiline=False)
        self.button = Button(text='Enter')
        self.button.bind(on_press=self.addFlight)
        self.confirm = Label(text='[color=90EE90]Enter a flight to be added to the database[/color]', markup=True)

        # Ajout des boutons, labels etc dans la grille d'interface graphique
        grid.add_widget(self.arrival)
        grid.add_widget(self.departure)
        grid.add_widget(Label(text='Flight'))
        grid.add_widget(self.flight)
        grid.add_widget(Label(text='Carrier'))
        grid.add_widget(self.carrier)
        grid.add_widget(Label(text='Destination'))
        grid.add_widget(self.destination)
        grid.add_widget(Label(text='Departure/arrival time'))
        grid.add_widget(self.time)
        grid.add_widget(Label(text='Codeshare'))
        grid.add_widget(self.codeshare)
        grid.add_widget(self.confirm)
        grid.add_widget(self.button)
        return grid

    # Fonction qui va modifier la BDD
    def addFlight(self, *kwargs):
        # On ouvre la BDD
        self.departures = self.openDepartures()
        self.arrivals = self.openArrivals()

        # Ajout des champs de texte dans un nouveau dictionnare qui va ensuite être ajouté à la liste des vols dans la BDD
        newFlight = {}
        newFlight['Flight'] = self.flight.text
        newFlight['Carrier'] = self.carrier.text
        newFlight['Destination'] = self.destination.text
        newFlight['Codeshare'] = self.codeshare.text

        # On décide dans quelle base de donnée sauvegarder en fonction de quel bouton à été enfoncé
        if self.arrival.state == 'down':
            newFlight['Arrival Time'] = self.time.text
            self.arrivals.append(newFlight)

            with open('static/arrivals.json', 'w') as arrivals_file:
                json.dump(self.arrivals, arrivals_file, indent=4)
            
            # Changement du texte pour confirmer la sauvegarde
            self.confirm.text = '[color=90EE90]Flight added to the database[/color]'
            self.eraseAll() # On efface les champs de texte
        else:
            newFlight['Departure Time'] = self.time.text
            self.departures.append(newFlight)

            with open('static/departures.json', 'w') as departures_file:
                json.dump(self.arrivals, departures_file, indent=4)

            self.confirm.text = '[color=90EE90]Flight added to the database[/color]'
            self.eraseAll()

    # Fonction qui efface les champs de textes, utilisé après une sauvegarde
    def eraseAll(self):
        self.flight.text = ''
        self.carrier.text = ''
        self.destination.text = ''
        self.time.text = ''
        self.codeshare.text = ''

    # Fonctions qui servent à ouvrir les BDD
    def openDepartures(self):
        try:
            with open('static/departures.json', 'r') as departuresFile:
                departures = json.load(departuresFile)
                return departures
        except:
            print('[ERROR] Failed loading database.')
            return []

    def openArrivals(self):
        try:
            with open('static/arrivals.json', 'r') as arrivalsFile:
                arrivals = json.load(arrivalsFile)
                return arrivals
        except:
            print('[ERROR] Failed loading database.')
            return []

Config.set('graphics', 'width', 550)
Config.set('graphics', 'height', 300)

planeFinder().run() # Lancement du programme
