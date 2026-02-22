import tkinter as tk
from tkinter import ttk
import random

# --- Environment and Agent Classes ---

class GridEnvironment:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.grid = {(r, c): random.choice(["Dirty", "Clean"]) for r in range(rows) for c in range(cols)}
        self.agent_pos = (0, 0)
        self.visited = set()

    def percept(self):
        return self.agent_pos, self.grid[self.agent_pos]

    def execute_action(self, action):
        r, c = self.agent_pos
        if action == "Suck":
            self.grid[(r, c)] = "Clean"
        elif action == "Up" and r > 0:
            self.agent_pos = (r - 1, c)
        elif action == "Down" and r < self.rows - 1:
            self.agent_pos = (r + 1, c)
        elif action == "Left" and c > 0:
            self.agent_pos = (r, c - 1)
        elif action == "Right" and c < self.cols - 1:
            self.agent_pos = (r, c + 1)
        self.visited.add(self.agent_pos)

    def is_done(self):
        return all(status == "Clean" for status in self.grid.values())

    def progress(self):
        total = self.rows * self.cols
        cleaned = sum(1 for s in self.grid.values() if s == "Clean")
        return int((cleaned / total) * 100)


class SimpleReflexAgent:
    def program(self, percept):
        (r, c), status = percept
        if status == "Dirty":
            return "Suck"
        return random.choice(["Up", "Down", "Left", "Right"])


class ModelBasedAgent:
    def __init__(self, rows=3, cols=3):
        self.model = {(r, c): "Unknown" for r in range(rows) for c in range(cols)}
        self.rows = rows
        self.cols = cols

    def program(self, percept):
        (r, c), status = percept
        self.model[(r, c)] = status
        if status == "Dirty":
            return "Suck"
        if all(s == "Clean" for s in self.model.values()):
            return "NoOp"
        return random.choice(["Up", "Down", "Left", "Right"])


# --- Premium UI Dashboard ---

class AIVacuumPremiumUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 AI Vacuum Cleaner Dashboard — Premium Edition")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0b132b")

        self.step = 0
        self.running = False

        self.build_ui()
        self.root.mainloop()

    # --- Build UI Layout ---
    def build_ui(self):
        title = tk.Label(self.root, text="AI Vacuum Cleaner Simulator",
                         font=("Poppins", 20, "bold"), fg="#f8f9fa", bg="#0b132b")
        title.pack(pady=10)

        subtitle = tk.Label(self.root, text="Simple Reflex vs Model-Based Agent",
                            font=("Poppins", 13), fg="#e0e0e0", bg="#0b132b")
        subtitle.pack()

        # --- Control Frame ---
        self.control_frame = tk.Frame(self.root, bg="#1c2541", bd=0, highlightthickness=0)
        self.control_frame.pack(pady=15)

        tk.Label(self.control_frame, text="Grid Size:", bg="#1c2541", fg="white", font=("Poppins", 10)).grid(row=0, column=0, padx=8)
        self.grid_entry = ttk.Entry(self.control_frame, width=5)
        self.grid_entry.insert(0, "3")
        self.grid_entry.grid(row=0, column=1, padx=5)

        style = ttk.Style()
        style.configure("TButton", font=("Poppins", 10), padding=6)
        style.map("TButton",
                  background=[("active", "#5bc0be")],
                  foreground=[("active", "#0b132b")])

        self.start_btn = ttk.Button(self.control_frame, text="▶ Start", command=self.start)
        self.pause_btn = ttk.Button(self.control_frame, text="⏸ Pause", command=self.pause, state="disabled")
        self.reset_btn = ttk.Button(self.control_frame, text="🔁 Reset", command=self.reset, state="disabled")

        self.start_btn.grid(row=0, column=2, padx=10)
        self.pause_btn.grid(row=0, column=3, padx=5)
        self.reset_btn.grid(row=0, column=4, padx=5)

        tk.Label(self.control_frame, text="Speed:", bg="#1c2541", fg="white", font=("Poppins", 10)).grid(row=0, column=5, padx=8)
        self.speed_slider = ttk.Scale(self.control_frame, from_=200, to=1500, value=800, orient="horizontal")
        self.speed_slider.grid(row=0, column=6, padx=5)

        # --- Canvas ---
        self.canvas = tk.Canvas(self.root, width=900, height=450, bg="#1b263b", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", font=("Poppins", 11), fg="#ffffff", bg="#0b132b")
        self.status_label.pack(pady=5)

    # --- Setup Grids ---
    def setup_env(self):
        self.rows = self.cols = int(self.grid_entry.get())
        self.env1 = GridEnvironment(self.rows, self.cols)
        self.env2 = GridEnvironment(self.rows, self.cols)
        self.agent1 = SimpleReflexAgent()
        self.agent2 = ModelBasedAgent(self.rows, self.cols)

        self.cell_size = int(300 / self.rows)
        self.cells1, self.cells2 = {}, {}

        self.canvas.delete("all")
        self.canvas.create_text(250, 40, text="Simple Reflex Agent", font=("Poppins", 13, "bold"), fill="#98c1d9")
        self.canvas.create_text(650, 40, text="Model-Based Agent", font=("Poppins", 13, "bold"), fill="#f4d35e")

        # Draw grid panels
        for env_cells, x_offset in [(self.cells1, 100), (self.cells2, 500)]:
            for r in range(self.rows):
                for c in range(self.cols):
                    x1, y1 = c*self.cell_size + x_offset, r*self.cell_size + 100
                    x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                    rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#3a506b", outline="#0b132b", width=2)
                    env_cells[(r, c)] = rect

        self.agent_icon1 = self.canvas.create_oval(0, 0, 0, 0, fill="#00aaff", outline="")
        self.agent_icon2 = self.canvas.create_oval(0, 0, 0, 0, fill="#ffd166", outline="")

        self.update_canvas()

    # --- Canvas Updates ---
    def update_canvas(self):
        for env, cells in [(self.env1, self.cells1), (self.env2, self.cells2)]:
            for (r, c), status in env.grid.items():
                color = "#ef233c" if status == "Dirty" else "#80ed99"
                self.canvas.itemconfig(cells[(r, c)], fill=color)

        self.move_agent(self.agent_icon1, self.env1.agent_pos, 100)
        self.move_agent(self.agent_icon2, self.env2.agent_pos, 500)

        progress1, progress2 = self.env1.progress(), self.env2.progress()
        self.status_label.config(text=f"Step {self.step} | Reflex: {progress1}% | Model-Based: {progress2}%")

    def move_agent(self, icon, pos, offset):
        r, c = pos
        x1, y1 = c*self.cell_size + offset + 10, r*self.cell_size + 110
        x2, y2 = x1 + 40, y1 + 40
        self.canvas.coords(icon, x1, y1, x2, y2)
        # Add glowing effect
        self.canvas.itemconfig(icon, outline="white", width=2)

    # --- Simulation Loop ---
    def simulate_step(self):
        if not self.running:
            return

        if self.env1.is_done() and self.env2.is_done():
            self.status_label.config(text=f"✅ Cleaning Complete in {self.step} steps!")
            self.pause_btn.config(state="disabled")
            self.reset_btn.config(state="normal")
            self.running = False
            return

        for env, agent in [(self.env1, self.agent1), (self.env2, self.agent2)]:
            if not env.is_done():
                percept = env.percept()
                action = agent.program(percept)
                if action != "NoOp":
                    env.execute_action(action)

        self.step += 1
        self.update_canvas()
        delay = int(self.speed_slider.get())
        self.root.after(delay, self.simulate_step)

    # --- Controls ---
    def start(self):
        if not hasattr(self, "env1"):
            self.setup_env()
        self.running = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.reset_btn.config(state="disabled")
        self.simulate_step()

    def pause(self):
        self.running = not self.running
        if self.running:
            self.pause_btn.config(text="⏸ Pause")
            self.simulate_step()
        else:
            self.pause_btn.config(text="▶ Resume")

    def reset(self):
        self.step = 0
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="⏸ Pause")
        self.reset_btn.config(state="disabled")
        self.canvas.delete("all")
        self.status_label.config(text="")
        if hasattr(self, "env1"):
            del self.env1, self.env2


# --- Run App ---
if __name__ == "__main__":
    AIVacuumPremiumUI()
