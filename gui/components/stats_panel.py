import tkinter as tk
from tkinter import ttk

class StatsPanelComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f172a")
        self.pack(fill=tk.X, pady=5)

        # Counter Widgets
        self.lbl_persons = self._create_card("PERSONS DETECTED")
        self.lbl_vehicles = self._create_card("VEHICLES DETECTED")
        self.lbl_tripwire = self._create_card("TRIPWIRE HITS")
        self.lbl_alerts = self._create_card("PROXIMITY ALERTS")

    def _create_card(self, title):
        card = tk.Frame(self, bg="#1e293b", padx=10, pady=8, relief="flat")
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

        tk.Label(card, text=title, font=("Helvetica", 8, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor="w")
        val_lbl = tk.Label(card, text="0", font=("Helvetica", 18, "bold"), fg="#38bdf8", bg="#1e293b")
        val_lbl.pack(anchor="w", pady=2)
        return val_lbl

    def update_counters(self, persons, vehicles, tripwires, alerts):
        self.lbl_persons.config(text=str(persons))
        self.lbl_vehicles.config(text=str(vehicles))
        self.lbl_tripwire.config(text=str(tripwires))
        self.lbl_alerts.config(text=str(alerts))