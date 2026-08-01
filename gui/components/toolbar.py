import tkinter as tk

class ToolbarComponent(tk.Frame):
    def __init__(self, parent, on_snapshot, on_export, on_shutdown):
        super().__init__(parent, bg="#1e293b", height=50)
        self.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(self, text="⚡ AI DETECTION DASHBOARD", font=("Helvetica", 12, "bold"), fg="#38bdf8", bg="#1e293b").pack(side=tk.LEFT, padx=15)

        tk.Button(self, text="📸 Snapshot", bg="#0284c7", fg="white", font=("Helvetica", 9, "bold"), relief="flat", command=on_snapshot).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Button(self, text="📄 Export PDF", bg="#8b5cf6", fg="white", font=("Helvetica", 9, "bold"), relief="flat", command=lambda: on_export("pdf")).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Button(self, text="📊 Export Excel", bg="#10b981", fg="white", font=("Helvetica", 9, "bold"), relief="flat", command=lambda: on_export("excel")).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Button(self, text="🚨 Shutdown", bg="#ef4444", fg="white", font=("Helvetica", 9, "bold"), relief="flat", command=on_shutdown).pack(side=tk.RIGHT, padx=15, pady=8)