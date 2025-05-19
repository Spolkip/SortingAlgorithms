import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import random
import time
import colorsys
import math
from collections import deque
from constants import *
from record_sorting import SortingRecorder
from sorting_algorithms import *

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sorting Algorithm Visualizer")
        self.root.config(bg=BG_COLOR)
        self.root.geometry("1400x900")
        
        # Initialize all variables first
        self.selected_algo = tk.StringVar()
        self.speed_scale = tk.IntVar(value=100)
        self.data_size = tk.IntVar(value=30)
        self.show_positions = tk.BooleanVar(value=True)
        self.order_var = tk.StringVar(value="Ascending")
        self.viz_mode = tk.StringVar(value="Bars")
        self.step_mode = tk.BooleanVar(value=False)
        self.theme_mode = tk.StringVar(value="Dark")
        
        # Import and set algorithm info
        from algorithms_info import algorithm_info
        self.algorithm_info = algorithm_info
        
        # Initialize other state variables
        self.data = []
        self.original_data = []
        self.sorting = False
        self.paused = False
        self.stop_sorting = False
        self.continue_logging = True
        self.after_id = None
        self.recorder = SortingRecorder()
        self.current_generator = None
        self.comparison_algorithms = []
        self.comparison_mode = False
        self.step_history = deque(maxlen=100)
        self.pseudocode_highlights = {}
        
        # Now setup the UI
        from ui_setup import setup_ui
        setup_ui(self)
        
        # Final initialization
        self.generate_array("random")
        self.root.after(100, self.initial_redraw)
        self.update_theme()

    def update_theme(self):
        theme = self.theme_mode.get()
        if theme == "Dark":
            bg = "#2d3436"
            control_bg = "#636e72"
            text_color = "#ffffff"
            console_bg = "#1e1e1e"
            console_text = "#e0e0e0"
        else:  # Light
            bg = "#f5f5f5"
            control_bg = "#e0e0e0"
            text_color = "#000000"
            console_bg = "#ffffff"
            console_text = "#000000"
        
        # Update all UI elements
        self.root.config(bg=bg)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=control_bg if widget.cget('bg') == CONTROL_BG else bg)
            elif isinstance(widget, tk.Label):
                widget.config(bg=bg, fg=text_color)
        
        self.canvas.config(bg=bg)
        self.complexity_canvas.config(bg=bg)
        self.console.config(bg=console_bg, fg=console_text)
        self.pseudocode_text.config(bg=console_bg, fg=console_text)
        self.complexity_text.config(bg=console_bg, fg=console_text)

    def toggle_theme(self):
        self.theme_mode.set("Light" if self.theme_mode.get() == "Dark" else "Dark")
        self.update_theme()
        self.redraw()

    def handle_array_generation(self, pattern):
        if pattern == "Custom":
            self.generate_custom_array()
        else:
            self.generate_special_array(pattern.lower().replace(" ", "_"))

    def generate_custom_array(self):
        input_str = simpledialog.askstring("Custom Array", 
                                          "Enter comma-separated numbers:",
                                          parent=self.root)
        if input_str:
            try:
                self.data = [int(x.strip()) for x in input_str.split(",")]
                self.original_data = self.data.copy()
                self.data_size.set(len(self.data))
                self.draw_bars(self.data, [BAR_COLOR for _ in range(len(self.data))])
                self.log_to_console(f"Loaded custom array with {len(self.data)} elements")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers separated by commas")

    def generate_array(self, pattern):
        """Alias for generate_special_array for backward compatibility"""
        self.generate_special_array(pattern)

    def generate_special_array(self, pattern):
        """Main implementation remains the same"""
        if pattern == "Custom":
            self.generate_custom_array()
        else:
            # Rest of your existing generate_special_array implementation
            size = self.data_size.get()
            if pattern == "sorted":
                self.data = list(range(1, size+1))
            elif pattern == "reversed":
                self.data = list(range(size, 0, -1))
            elif pattern == "nearly_sorted":
                self.data = list(range(1, size+1))
                # Swap 10% of elements
                for _ in range(size//10):
                    i, j = random.sample(range(size), 2)
                    self.data[i], self.data[j] = self.data[j], self.data[i]
            elif pattern == "few_unique":
                unique_values = random.sample(range(1, 100), min(5, size//2))
                self.data = [random.choice(unique_values) for _ in range(size)]
            else:  # random
                self.data = [random.randint(1, 100) for _ in range(size)]
            
            self.original_data = self.data.copy()
            self.draw_bars(self.data, [BAR_COLOR for _ in range(len(self.data))])
            self.log_to_console(f"Generated {pattern.replace('_', ' ')} array with {size} elements")

    def show_algorithm_info(self):
        algo = self.selected_algo.get()
        info = self.algorithm_info.get(algo, {})
        
        # Prepare the message parts separately
        description = info.get('description', '')
        complexity = info.get('complexity', '').split('\n')
        time_complexity = complexity[0] if len(complexity) > 0 else ''
        space_complexity = complexity[1] if len(complexity) > 1 else ''
        best_case = info.get('best_case', '')
        worst_case = info.get('worst_case', '')
        stable = 'Yes' if info.get('stable', False) else 'No'
        
        # Build the message using concatenation
        message = (
            f"{algo}\n\n"
            f"Description:\n{description}\n\n"
            f"Time Complexity: {time_complexity}\n"
            f"Space Complexity: {space_complexity}\n\n"
            f"Best Case: {best_case}\n"
            f"Worst Case: {worst_case}\n"
            f"Stable: {stable}"
        )
        
        messagebox.showinfo(f"{algo} Information", message)

    def update_algorithm_info(self):
        algo = self.selected_algo.get()
        info = self.algorithm_info.get(algo, {})
        
        # Update pseudocode
        self.pseudocode_text.config(state='normal')
        self.pseudocode_text.delete(1.0, tk.END)
        self.pseudocode_text.insert(tk.END, info.get("pseudocode", "Select an algorithm"))
        self.pseudocode_text.config(state='disabled')
        
        # Update complexity
        self.complexity_text.config(state='normal')
        self.complexity_text.delete(1.0, tk.END)
        self.complexity_text.insert(tk.END, info.get("complexity", ""))
        self.complexity_text.config(state='disabled')
        
        # Update complexity label - fixed version
        complexity = info.get('complexity', '')
        first_line = complexity.split('\n')[0] if '\n' in complexity else complexity
        self.complexity_label.config(text=f"O(n): {first_line}")

    def add_resize_handle(self, parent):
        """Adds a resize handle to a container"""
        resize_handle = tk.Frame(parent, bg=CONSOLE_DRAG_HANDLE_COLOR, 
                               height=RESIZE_HANDLE_HEIGHT, cursor="sb_v_double_arrow")
        resize_handle.pack(side=tk.BOTTOM, fill=tk.X)
        
        def start_resize(event):
            resize_handle.start_height = parent.winfo_height()
            resize_handle.start_y = event.y_root
        
        def do_resize(event):
            if hasattr(resize_handle, 'start_height'):
                delta = event.y_root - resize_handle.start_y
                new_height = max(100, resize_handle.start_height + delta)
                parent.config(height=new_height)
        
        resize_handle.bind("<ButtonPress-1>", start_resize)
        resize_handle.bind("<B1-Motion>", do_resize)
        resize_handle.bind("<ButtonRelease-1>", lambda e: resize_handle.__dict__.pop('start_height', None))

    def on_window_resize(self, event):
        """Handle window resizing events"""
        if hasattr(self, 'canvas'):
            self.redraw()
                
    def draw_bars(self, array, color_array):
        self.canvas.delete("all")
        if not array:
            return
            
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        max_val = max(array) if array else 1
        normalized_data = [i/max_val for i in array]
        
        if self.viz_mode.get() == "Bars":
            bar_width = c_width / (len(array) + 1)
            spacing = 2
            for i, height in enumerate(normalized_data):
                # Draw the bar
                x0 = i * bar_width + spacing
                y0 = c_height - height * (c_height - 20)
                x1 = (i + 1) * bar_width
                y1 = c_height
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i], outline="")
                
                # Draw the number if enabled
                if self.show_positions.get() and len(array) <= 50 and bar_width > 20:
                    x_center = (x0 + x1) / 2
                    y_text = y0 - 15  # Position above the bar
                    font_size = max(8, min(12, int(bar_width/3)))
                    self.canvas.create_text(
                        x_center, y_text,
                        text=str(array[i]),
                        fill=TEXT_COLOR,
                        font=("Arial", font_size),
                        anchor=tk.S
                    )
        
        elif self.viz_mode.get() == "Lines":
            points = []
            for i, height in enumerate(normalized_data):
                x = (i + 0.5) * (c_width / len(array))
                y = c_height - height * (c_height - 20)
                points.extend([x, y])
            if len(points) > 3:
                self.canvas.create_line(points, fill=BAR_COLOR, width=2)
        
        elif self.viz_mode.get() == "Color Gradient":
            for i, height in enumerate(normalized_data):
                x0 = i * (c_width / len(array))
                y0 = 0
                x1 = (i + 1) * (c_width / len(array))
                y1 = c_height
                hue = height * 120
                color = self.hsv_to_hex(hue, 1.0, 1.0)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        
        # Draw complexity graph
        self.draw_complexity_graph()
        
        self.root.update_idletasks()

    def draw_complexity_graph(self):
        self.complexity_canvas.delete("all")
        width = self.complexity_canvas.winfo_width()
        height = self.complexity_canvas.winfo_height()
        
        # Draw axes
        self.complexity_canvas.create_line(30, height-30, width-30, height-30, fill="white")  # X-axis
        self.complexity_canvas.create_line(30, height-30, 30, 30, fill="white")  # Y-axis
        
        # Draw labels
        self.complexity_canvas.create_text(15, height//2, text="O(n)", fill="white", angle=90)
        self.complexity_canvas.create_text(width//2, height-15, text="Input Size (n)", fill="white")
        
        # Get current algorithm's complexity
        algo = self.selected_algo.get()
        complexity = self.algorithm_info.get(algo, {}).get("complexity", "O(n²)").split("\n")[0]
        
        # Draw complexity curves
        n = len(self.data)
        x_scale = (width - 60) / n
        y_scale = (height - 60) / 100
        
        # Draw O(n²) curve
        points = []
        for i in range(1, n+1):
            x = 30 + i * x_scale
            y = height - 30 - (i**2) * y_scale / (n**2) * 100
            points.append((x, y))
        self.complexity_canvas.create_line(points, fill="#e74c3c", width=2)
        
        # Draw O(n log n) curve
        points = []
        for i in range(1, n+1):
            x = 30 + i * x_scale
            y = height - 30 - (i * math.log2(i+1)) * y_scale / (n * math.log2(n+1)) * 100
            points.append((x, y))
        self.complexity_canvas.create_line(points, fill="#3498db", width=2)
        
        # Draw O(n) curve
        points = []
        for i in range(1, n+1):
            x = 30 + i * x_scale
            y = height - 30 - i * y_scale
            points.append((x, y))
        self.complexity_canvas.create_line(points, fill="#2ecc71", width=2)
        
        # Highlight current algorithm's complexity
        if "O(n²)" in complexity:
            color = "#e74c3c"
        elif "O(n log n)" in complexity:
            color = "#3498db"
        else:
            color = "#2ecc71"
        
        self.complexity_canvas.create_text(width-50, 20, 
                                         text=f"Current: {complexity}", 
                                         fill=color, anchor=tk.NE)

    def log_to_console(self, message):
        self.console.config(state='normal')
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')
        self.root.update_idletasks()

    def initial_redraw(self):
        if hasattr(self, 'data'):
            self.redraw()

    def redraw(self):
        if hasattr(self, 'data'):
            color_array = [BAR_COLOR for _ in range(len(self.data))]
            self.draw_bars(self.data, color_array)
            self.log_to_console(f"Redrew visualization (Show Positions: {self.show_positions.get()}")

    def start_sorting(self):
        print("Start sorting called")  # Debug line
        if self.sorting and not self.paused:
            self.log_to_console("Sorting already in progress")
            return
            
        if not self.data:
            self.log_to_console("No data to sort - generate an array first")
            return
            
        if self.paused:
            self.toggle_pause()
            return
            
        self.original_data = self.data.copy()
        self.sorting = True
        self.paused = False
        self.stop_sorting = False
        self.continue_logging = True
        self.recorder.start_recording()
        self.step_history.clear()
        
        algo = self.selected_algo.get()
        print(f"Selected algorithm: {algo}")  # Debug line
        speed = max(1, 1000 - self.speed_scale.get())
        
        self.log_to_console(f"Starting {algo} ({self.order_var.get()}) on {len(self.data)} elements")
        
        algorithm_map = {
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Selection Sort": selection_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort,
            "Shell Sort": shell_sort,
            "Radix Sort": radix_sort,
            "Counting Sort": counting_sort
        }
        
        print(f"Available algorithms: {algorithm_map.keys()}")  # Debug line
        
        if algo in algorithm_map:
            print(f"Algorithm found: {algo}")  # Debug line
            try:
                generator = algorithm_map[algo](
                    self.data, 
                    BAR_COLOR, 
                    BAR_HIGHLIGHT, 
                    self.order_var.get(), 
                    self.get_logger()
                )
                self.current_generator = generator
                print("Generator created successfully")  # Debug line
                
                if self.step_mode.get():
                    self.log_to_console("Step mode enabled - use Step button to advance")
                else:
                    print("Starting animation")  # Debug line
                    self.animate(generator, speed, algo)
            except Exception as e:
                print(f"Error creating generator: {e}")  # Debug line
                self.sorting = False
        else:
            print(f"Algorithm not found: {algo}")  # Debug line
            self.sorting = False
            self.log_to_console("Error: Unknown algorithm selected")
            
    def toggle_pause(self):
        if not self.sorting:
            return
            
        self.paused = not self.paused
        if self.paused:
            self.log_to_console("Sorting paused")
            if hasattr(self, 'after_id'):
                self.root.after_cancel(self.after_id)
        else:
            self.log_to_console("Resuming sorting")
            if self.step_mode.get():
                self.log_to_console("Still in step mode - use Step button to advance")
            else:
                self.animate(self.current_generator, max(1, 1000 - self.speed_scale.get()), 
                            self.selected_algo.get())

    def animate(self, generator, speed, algo):
        if self.stop_sorting or not self.sorting or self.paused:
            return
            
        try:
            arr, color_array, comparisons, swaps, accesses = next(generator)
            self.step_history.append((self.data.copy(), [BAR_COLOR for _ in range(len(self.data))]))
            self.data = arr.copy()
            self.draw_bars(arr, color_array)
            self.recorder.update_stats(comparisons, swaps, accesses)  # Now passing 3 arguments
            self.update_info_labels(
                self.recorder.get_elapsed_time(),
                self.recorder.comparisons,
                self.recorder.swaps,
                self.recorder.accesses
            )
            
            if not self.step_mode.get():
                self.after_id = self.root.after(speed, lambda: self.animate(generator, speed, algo))
        except StopIteration:
            self.sorting = False
            self.paused = False
            self.draw_bars(self.data, [BAR_COLOR for _ in range(len(self.data))])
            self.log_to_console(f"{algo} completed in {self.recorder.get_elapsed_time():.2f}s")
            self.log_to_console(f"Comparisons: {self.recorder.comparisons}, Swaps: {self.recorder.swaps}, Accesses: {self.recorder.accesses}")
        except Exception as e:
            print(f"Error in animation: {e}")
            self.sorting = False

    def step_forward(self):
        if self.step_mode.get() and self.sorting and not self.paused and self.current_generator:
            try:
                arr, color_array, comparisons, swaps, accesses = next(self.current_generator)
                self.step_history.append((self.data.copy(), [BAR_COLOR for _ in range(len(self.data))]))
                self.data = arr.copy()
                self.draw_bars(arr, color_array)
                self.recorder.update_stats(comparisons, swaps, accesses)
                self.update_info_labels(
                    self.recorder.get_elapsed_time(),
                    self.recorder.comparisons,
                    self.recorder.swaps,
                    self.recorder.accesses
                )
                self.highlight_pseudocode_step()
            except StopIteration:
                self.sorting = False
                self.paused = False
                self.draw_bars(self.data, [BAR_COLOR for _ in range(len(self.data))])
                self.log_to_console(f"{self.selected_algo.get()} completed!")

    def step_backward(self):
        if self.step_history:
            self.data, color_array = self.step_history.pop()
            self.draw_bars(self.data, color_array)
            self.log_to_console("Stepped backward one step")
            self.highlight_pseudocode_step(backward=True)

    def highlight_pseudocode_step(self, backward=False):
        pass

    def setup_comparison(self):
        algorithms = list(self.algorithm_info.keys())
        selected = simpledialog.askstring("Algorithm Comparison",
                                         "Enter two algorithms to compare, separated by comma:",
                                         parent=self.root)
        if selected:
            try:
                algo1, algo2 = [a.strip() for a in selected.split(",")]
                if algo1 in algorithms and algo2 in algorithms:
                    self.comparison_mode = True
                    self.comparison_algorithms = [algo1, algo2]
                    self.start_comparison()
                else:
                    messagebox.showerror("Error", "Please enter valid algorithm names")
            except ValueError:
                messagebox.showerror("Error", "Please enter exactly two algorithms separated by comma")

    def start_comparison(self):
        if len(self.comparison_algorithms) != 2:
            return
            
        self.log_to_console(f"Starting comparison between {self.comparison_algorithms[0]} and {self.comparison_algorithms[1]}")
        
        self.selected_algo.set(self.comparison_algorithms[0])
        self.start_sorting()
        
        self.root.after(5000, lambda: self.run_second_algorithm())

    def run_second_algorithm(self):
        if not self.comparison_mode:
            return
            
        self.selected_algo.set(self.comparison_algorithms[1])
        self.start_sorting()
        self.comparison_mode = False

    def stop_sorting_func(self):
        if self.sorting:
            self.stop_sorting = True
            self.sorting = False
            self.paused = False
            self.log_to_console("Stopping current sorting operation...")
            if hasattr(self, 'after_id'):
                self.root.after_cancel(self.after_id)
            if hasattr(self, 'original_data') and self.original_data:
                self.data = self.original_data.copy()
                self.draw_bars(self.data, [BAR_COLOR for _ in range(len(self.data))])

    def update_info_labels(self, time_val, comparisons, swaps, accesses):
        self.time_label.config(text=f"Time: {time_val:.2f}s")
        self.comparisons_label.config(text=f"Comparisons: {comparisons}")
        self.swaps_label.config(text=f"Swaps: {swaps}")
        self.accesses_label.config(text=f"Array Accesses: {accesses}")

    def reset(self):
        self.stop_sorting_func()
        self.generate_array("random")
        self.log_to_console("Application reset")

    def get_logger(self):
        def logger(message):
            if self.continue_logging:
                self.log_to_console(message)
        return logger

    def hsv_to_hex(self, h, s=1.0, v=1.0):
        """Convert HSV to hexadecimal color (h: 0-360, s: 0-1, v: 0-1)"""
        r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
        # Using string format() instead of f-string to avoid backslash issue
        return "#{:02x}{:02x}{:02x}".format(
            int(r*255),
            int(g*255),
            int(b*255)
        )