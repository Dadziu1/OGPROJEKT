

import os
import folium
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from geopy.geocoders import Nominatim
import webbrowser

class GeoportalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geoportal API")
        self.root.geometry("800x600")

        # Ustawienia mapy bazowej
        self.map = folium.Map(location=[52.2297, 21.0122], zoom_start=12)  # Warszawa

        # Interfejs użytkownika
        self.create_widgets()

        # Ścieżka do zapisu mapy
        self.map_file = "map.html"

    def create_widgets(self):
        # Główna ramka
        frame = Frame(self.root)
        frame.pack(side=TOP, fill=X, padx=10, pady=10)

        # Pole do wyszukiwania lokalizacji
        Label(frame, text="Wyszukaj lokalizację:").pack(side=LEFT, padx=5)
        self.search_entry = Entry(frame, width=40)
        self.search_entry.pack(side=LEFT, padx=5)
        Button(frame, text="Szukaj", command=self.search_location).pack(side=LEFT, padx=5)

        # Przycisk do wczytywania danych GeoJSON
        Button(frame, text="Wczytaj GeoJSON", command=self.load_geojson).pack(side=LEFT, padx=5)

        # Przycisk do wyświetlania mapy
        Button(frame, text="Pokaż mapę", command=self.show_map).pack(side=LEFT, padx=5)

    def search_location(self):
        """Wyszukaj lokalizację i ustaw mapę na tej lokalizacji."""
        location = self.search_entry.get()
        if location:
            geolocator = Nominatim(user_agent="geoportal")
            loc = geolocator.geocode(location)
            if loc:
                # Aktualizacja środka mapy na współrzędne lokalizacji
                self.map = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=12)

                # Dodanie znacznika na nową lokalizację
                folium.Marker(
                    location=[loc.latitude, loc.longitude],
                    popup=location,
                    tooltip="Kliknij, aby zobaczyć",
                ).add_to(self.map)

                self.save_map()
                self.show_map()
            else:
                self.show_message("Nie znaleziono lokalizacji!")

    def load_geojson(self):
        """Wczytaj dane GeoJSON i dodaj je do mapy."""
        file_path = filedialog.askopenfilename(
            title="Wybierz plik GeoJSON",
            filetypes=[("Pliki GeoJSON", "*.geojson")],
        )
        if file_path:
            folium.GeoJson(file_path, name="geojson").add_to(self.map)
            self.save_map()
            self.show_map()

    def save_map(self):
        """Zapisz mapę do pliku HTML."""
        self.map.save(self.map_file)

    def show_map(self):
        """Wyświetl zapisany plik mapy w przeglądarce."""
        webbrowser.open(self.map_file)

    def show_message(self, message):
        """Wyświetl wiadomość dla użytkownika."""
        popup = Toplevel(self.root)
        popup.title("Informacja")
        Label(popup, text=message, padx=20, pady=10).pack()
        Button(popup, text="OK", command=popup.destroy).pack(pady=10)

# Uruchomienie aplikacji
if __name__ == "__main__":
    root = Tk()
    app = GeoportalApp(root)
    root.mainloop()