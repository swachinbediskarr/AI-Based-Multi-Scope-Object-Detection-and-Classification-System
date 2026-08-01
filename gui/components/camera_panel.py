import tkinter as tk

class CameraPanelComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f172a")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.video_label = tk.Label(self, bg="#000000", text="[LIVE CAMERA FEED]", fg="#64748b", font=("Helvetica", 14))
        self.video_label.pack(fill=tk.BOTH, expand=True, pady=5)

    def update_frame(self, imgtk):
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)