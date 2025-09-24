import requests
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import csv

# Your OpenWeatherMap API key
API_KEY = 'bad1db9373621064dd69e33230a6428f'

# List of German cities (can be expanded as needed)
german_cities = [
    "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart", "Düsseldorf", 
    "Dortmund", "Essen", "Bremen", "Dresden", "Leipzig", "Hannover", "Nuremberg"
]

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("1000x600")
        
        self.city_combobox = None
        self.save_button = None
        self.city_label = None
        self.temp_label = None
        self.humidity_label = None
        self.pressure_label = None
        self.description_label = None
        self.temp_min_label = None
        self.temp_max_label = None
        self.graph_frame = None
        self.favorites_listbox = None
        
        self.setup_gui()
    
    def setup_gui(self):
        # Setup the GUI components
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=10)

        self.city_label = tk.Label(self.top_frame, text="City: ", font=('Times New Roman', 14))
        self.city_label.grid(row=0, column=0, padx=5)

        self.temp_label = tk.Label(self.top_frame, text="Temperature: ", font=('Times New Roman', 14))
        self.temp_label.grid(row=0, column=1, padx=5)

        self.humidity_label = tk.Label(self.top_frame, text="Humidity: ", font=('Times New Roman', 14))
        self.humidity_label.grid(row=0, column=2, padx=5)

        self.pressure_label = tk.Label(self.top_frame, text="Pressure: ", font=('Times New Roman', 14))
        self.pressure_label.grid(row=0, column=3, padx=5)

        self.description_label = tk.Label(self.top_frame, text="Description: ", font=('Times New Roman', 14))
        self.description_label.grid(row=1, column=0, padx=5)

        self.temp_min_label = tk.Label(self.top_frame, text="Min Temp: ", font=('Times New Roman', 14))
        self.temp_min_label.grid(row=1, column=1, padx=5)

        self.temp_max_label = tk.Label(self.top_frame, text="Max Temp: ", font=('Times New Roman', 14))
        self.temp_max_label.grid(row=1, column=2, padx=5)

        # Dropdown (ComboBox) for selecting city
        self.city_combobox = ttk.Combobox(self.root, values=german_cities, font=('Times New Roman', 14))
        self.city_combobox.pack(pady=10)

        # Button to fetch weather data
        get_weather_button = tk.Button(self.root, text="Get Weather", font=('Times New Roman', 14), command=self.update_weather_display)
        get_weather_button.pack(pady=5)

        # Button to save city to favorites
        self.save_button = tk.Button(self.root, text="Save to Favorites", font=('Times New Roman', 14), command=self.save_favorite_city, state=tk.DISABLED)
        self.save_button.pack(pady=5)

        # Frame for weather graphs (scrollable part for the graph only)
        graph_frame_canvas = tk.Canvas(self.root)
        graph_frame_scrollbar = tk.Scrollbar(self.root, orient="vertical", command=graph_frame_canvas.yview)
        self.graph_frame = tk.Frame(graph_frame_canvas)

        graph_frame_canvas.create_window((0, 0), window=self.graph_frame, anchor="nw")
        graph_frame_canvas.configure(yscrollcommand=graph_frame_scrollbar.set)

        graph_frame_scrollbar.pack(side="right", fill="y")
        graph_frame_canvas.pack(side="left", fill="both", expand=True)

        # Favorites Tab
        favorites_frame = tk.Frame(self.root, width=300)
        favorites_frame.pack(side="right", fill="y", padx=10)

        self.favorites_listbox = tk.Listbox(favorites_frame, width=30, height=15, font=('Times New Roman', 14))
        self.favorites_listbox.pack(pady=5)
        self.favorites_listbox.bind("<Double-1>", self.load_favorite_city)

        show_favorites_button = tk.Button(favorites_frame, text="Show Favorites", font=('Times New Roman', 14), command=self.show_favorites)
        show_favorites_button.pack(pady=5)

        # Button to remove selected city from favorites
        remove_favorite_button = tk.Button(favorites_frame, text="Remove from Favorites", font=('Times New Roman', 14), command=self.remove_favorite_city)
        remove_favorite_button.pack(pady=5)

        download_button = tk.Button(self.root, text="Download Weather Data", font=('Times New Roman', 14), command=self.download_data)
        download_button.pack(pady=10)

    def get_weather(self, city_name):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name},de&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get('cod') == 200:
            weather_info = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max']
            }
            return weather_info
        else:
            error_message = data.get('message', 'Unknown error')
            messagebox.showerror("Error", f"City not found or API error: {error_message}")
            return None

    def plot_weather_graphs(self, weather_info):
        fig, axs = plt.subplots(2, 2, figsize=(8, 6))  # Adjusted figsize to make graphs smaller

        # Temperature Graph
        axs[0, 0].bar(['Min Temp', 'Current Temp', 'Max Temp'],
                      [weather_info['temp_min'], weather_info['temperature'], weather_info['temp_max']],
                      color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        axs[0, 0].set_title('Temperature')
        axs[0, 0].set_ylabel('Temperature (°C)')

        # Humidity Graph (Separate graph)
        axs[0, 1].bar(['Humidity'], [weather_info['humidity']], color='#1f77b4')
        axs[0, 1].set_title('Humidity')
        axs[0, 1].set_ylabel('%')

        # Pressure Graph (Separate graph)
        axs[1, 0].bar(['Pressure'], [weather_info['pressure']], color='#9467bd')
        axs[1, 0].set_title('Pressure')
        axs[1, 0].set_ylabel('Pressure (hPa)')

        # Description Graph (Optional: Placeholder graph for description or any other data)
        axs[1, 1].axis('off')  # Just turn off the last graph for now

        plt.tight_layout()

        # Clear previous canvas and plot new graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def update_weather_display(self):
        city_name = self.city_combobox.get()
        if city_name:
            weather_info = self.get_weather(city_name)
            if weather_info:
                self.city_label.config(text=f"City: {weather_info['city']}")
                self.temp_label.config(text=f"Temperature: {weather_info['temperature']}°C")
                self.humidity_label.config(text=f"Humidity: {weather_info['humidity']}%")
                self.pressure_label.config(text=f"Pressure: {weather_info['pressure']} hPa")
                self.description_label.config(text=f"Description: {weather_info['description']}")
                self.temp_min_label.config(text=f"Min Temp: {weather_info['temp_min']}°C")
                self.temp_max_label.config(text=f"Max Temp: {weather_info['temp_max']}°C")
                self.save_button.config(state=tk.NORMAL)

                # Plot graphs on the canvas
                self.plot_weather_graphs(weather_info)
        else:
            messagebox.showerror("Error", "Please select a city.")

    def save_favorite_city(self):
        city_name = self.city_combobox.get()
        if city_name:
            try:
                with open('favorite_cities.json', 'r') as file:
                    favorite_cities = json.load(file)
            except FileNotFoundError:
                favorite_cities = []

            favorite_cities.append(city_name)

            with open('favorite_cities.json', 'w') as file:
                json.dump(favorite_cities, file)

            self.show_favorites()
            messagebox.showinfo("Success", f"{city_name} has been added to your favorite cities.")
        else:
            messagebox.showerror("Error", "No city to save.")

    def show_favorites(self):
        try:
            with open('favorite_cities.json', 'r') as file:
                favorite_cities = json.load(file)
            self.favorites_listbox.delete(0, tk.END)
            for city in favorite_cities:
                self.favorites_listbox.insert(tk.END, city)
        except FileNotFoundError:
            messagebox.showerror("Error", "No favorite cities found.")

    def load_favorite_city(self, event):
        city_name = self.favorites_listbox.get(self.favorites_listbox.curselection())
        self.city_combobox.set(city_name)
        self.update_weather_display()

    def remove_favorite_city(self):
        city_name = self.favorites_listbox.get(self.favorites_listbox.curselection())
        if city_name:
            try:
                with open('favorite_cities.json', 'r') as file:
                    favorite_cities = json.load(file)

                if city_name in favorite_cities:
                    favorite_cities.remove(city_name)

                with open('favorite_cities.json', 'w') as file:
                    json.dump(favorite_cities, file)

                self.show_favorites()
                messagebox.showinfo("Success", f"{city_name} has been removed from your favorites.")
            except FileNotFoundError:
                messagebox.showerror("Error", "No favorite cities found.")
        else:
            messagebox.showerror("Error", "No city selected to remove.")

    def download_data(self):
        city_name = self.city_combobox.get()
        if city_name:
            weather_info = self.get_weather(city_name)
            if weather_info:
                filename = f"{city_name}_weather.csv"
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['City', 'Temperature', 'Humidity', 'Pressure', 'Description', 'Min Temp', 'Max Temp']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        'City': weather_info['city'],
                        'Temperature': weather_info['temperature'],
                        'Humidity': weather_info['humidity'],
                        'Pressure': weather_info['pressure'],
                        'Description': weather_info['description'],
                        'Min Temp': weather_info['temp_min'],
                        'Max Temp': weather_info['temp_max']
                    })
                messagebox.showinfo("Success", f"Weather data saved as {filename}")
        else:
            messagebox.showerror("Error", "No data to save.")

# GUI Setup using Tkinter
root = tk.Tk()
weather_dashboard = WeatherDashboard(root)
root.mainloop()
