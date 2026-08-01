import tkinter as tk
from tkinter import ttk

class DetectionTableComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e293b")
        self.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.all_logs = []

        tk.Label(
            self, text="REAL-TIME TELEMETRY LOGS", 
            font=("Helvetica", 10, "bold"), fg="#38bdf8", bg="#1e293b"
        ).pack(anchor="w", padx=10, pady=6)

        search_frame = tk.Frame(self, bg="#1e293b")
        search_frame.pack(fill=tk.X, padx=10, pady=2)

        tk.Label(search_frame, text="Filter Class:", fg="#94a3b8", bg="#1e293b", font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        self.filter_entry = tk.Entry(
            search_frame, textvariable=self.filter_var, 
            bg="#334155", fg="white", insertbackground="white", relief="flat"
        )
        self.filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.filter_entry.bind("<KeyRelease>", self._apply_filter)

        scroll = ttk.Scrollbar(self)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        self.tree = ttk.Treeview(
            self, columns=("Time", "ID", "Class", "Distance"), 
            show="headings", yscrollcommand=scroll.set, height=20
        )
        scroll.config(command=self.tree.yview)

        self.tree.heading("Time", text="Time")
        self.tree.heading("ID", text="Track ID")
        self.tree.heading("Class", text="Object Class")
        self.tree.heading("Distance", text="Distance")

        self.tree.column("Time", width=75, anchor="center")
        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Class", width=120, anchor="w")
        self.tree.column("Distance", width=75, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def update_table(self, logs):
        self.all_logs = logs
        self._apply_filter()

    def _apply_filter(self, event=None):
        filter_text = self.filter_var.get().lower()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for log in self.all_logs[:30]:  
            cls_name = str(log.get("class_name", ""))
            if filter_text == "" or filter_text in cls_name.lower():
                time_str = str(log.get("timestamp", "")).split()[-1] if log.get("timestamp") else ""
                self.tree.insert("", tk.END, values=(
                    time_str,
                    log.get("track_id", ""),
                    cls_name,
                    f"{log.get('distance_m', 0.0):.2f}m"
                ))