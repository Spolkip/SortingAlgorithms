import tkinter as tk
from tkinter import ttk, scrolledtext
from constants import *

def setup_ui(visualizer):
    # Main container with paned window for resizable split
    visualizer.main_paned = tk.PanedWindow(visualizer.root, orient=tk.HORIZONTAL, 
                                        bg=BG_COLOR, sashrelief=tk.RAISED, 
                                        sashwidth=8, opaqueresize=True)
    visualizer.main_paned.pack(fill=tk.BOTH, expand=True)
    
    # Left panel - Visualization and controls
    visualizer.left_frame = tk.Frame(visualizer.main_paned, bg=BG_COLOR)
    visualizer.main_paned.add(visualizer.left_frame, minsize=800, stretch='always')
    
    # Right panel - Console and educational info (draggable)
    visualizer.right_frame = tk.Frame(visualizer.main_paned, bg=CONSOLE_BG, width=450)
    visualizer.main_paned.add(visualizer.right_frame, minsize=400)
    
    # Make right panel draggable
    visualizer.drag_handle = tk.Frame(visualizer.right_frame, bg=CONSOLE_DRAG_HANDLE_COLOR, 
                                    height=20, cursor="fleur")
    visualizer.drag_handle.pack(fill=tk.X)
    
    # Drag functionality
    def start_drag(event):
        visualizer.drag_handle.drag_data = {"x": event.x_root, "y": event.y_root}
    
    def stop_drag(event):
        visualizer.drag_handle.drag_data = None
    
    def do_drag(event):
        if hasattr(visualizer.drag_handle, 'drag_data'):
            dx = event.x_root - visualizer.drag_handle.drag_data["x"]
            dy = event.y_root - visualizer.drag_handle.drag_data["y"]
            x = visualizer.right_frame.winfo_x() + dx
            y = visualizer.right_frame.winfo_y() + dy
            visualizer.right_frame.place(x=x, y=y)
            visualizer.drag_handle.drag_data = {"x": event.x_root, "y": event.y_root}
    
    visualizer.drag_handle.bind("<ButtonPress-1>", start_drag)
    visualizer.drag_handle.bind("<ButtonRelease-1>", stop_drag)
    visualizer.drag_handle.bind("<B1-Motion>", do_drag)
    
    # Control frame
    control_frame = tk.Frame(visualizer.left_frame, bg=CONTROL_BG, padx=10, pady=5)
    control_frame.pack(fill=tk.X)
    
    # Algorithm selection
    algo_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    algo_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(algo_frame, text="Algorithm:", bg=CONTROL_BG, fg="white").pack(side=tk.LEFT)
    algo_menu = ttk.Combobox(algo_frame, textvariable=visualizer.selected_algo,
                           values=list(visualizer.algorithm_info.keys()), width=15)
    algo_menu.current(0)
    algo_menu.pack(side=tk.LEFT)
    algo_menu.bind("<<ComboboxSelected>>", lambda e: visualizer.update_algorithm_info())
    tk.Button(algo_frame, text="ℹ️", command=visualizer.show_algorithm_info,
             bg=CONTROL_BG, fg="white", relief=tk.FLAT, bd=0).pack(side=tk.LEFT, padx=5)
    
    # Speed control (slider)
    speed_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    speed_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(speed_frame, text="Speed:", bg=CONTROL_BG, fg="white").pack(side=tk.LEFT)
    tk.Scale(speed_frame, from_=1, to=1000, orient=tk.HORIZONTAL,
            variable=visualizer.speed_scale, bg=CONTROL_BG, fg="white",
            highlightthickness=0, length=150).pack(side=tk.LEFT)
    
    # Data controls
    data_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    data_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(data_frame, text="Size:", bg=CONTROL_BG, fg="white").pack(side=tk.LEFT)
    tk.Scale(data_frame, from_=2, to=200, orient=tk.HORIZONTAL,
            variable=visualizer.data_size, bg=CONTROL_BG, fg="white",
            highlightthickness=0, length=100).pack(side=tk.LEFT)
    
    # Order and visualization
    order_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    order_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(order_frame, text="Order:", bg=CONTROL_BG, fg="white").pack(side=tk.LEFT)
    ttk.Combobox(order_frame, textvariable=visualizer.order_var,
                values=["Ascending", "Descending"], width=10).pack(side=tk.LEFT)
    
    viz_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    viz_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(viz_frame, text="Display:", bg=CONTROL_BG, fg="white").pack(side=tk.LEFT)
    ttk.Combobox(viz_frame, textvariable=visualizer.viz_mode,
                values=["Bars", "Dots", "Lines", "Color Gradient"], width=12).pack(side=tk.LEFT)
    
    # Array generation options
    array_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    array_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(array_frame, text="Array:", bg=CONTROL_BG, fg="white").pack(side=tk.LEFT)
    array_menu = ttk.Combobox(array_frame, 
                             values=["Random", "Sorted", "Reversed", "Nearly Sorted", "Few Unique", "Custom"],
                             width=10)
    array_menu.current(0)
    array_menu.pack(side=tk.LEFT)
    array_menu.bind("<<ComboboxSelected>>", lambda e: visualizer.handle_array_generation(array_menu.get()))
    
    # Buttons
    button_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    button_frame.pack(side=tk.LEFT, padx=5)
    
    buttons = [
        ("▶ Start", visualizer.start_sorting, BUTTON_COLOR),
        ("⏸ Pause", visualizer.toggle_pause, BUTTON_COLOR),
        ("⏹ Stop", visualizer.stop_sorting_func, BUTTON_COLOR),
        ("⟳ Reset", visualizer.reset, BUTTON_COLOR),
        ("⏩ Step", visualizer.step_forward, BUTTON_COLOR),
        ("⏪ Back", visualizer.step_backward, BUTTON_COLOR),
        ("⚖ Compare", visualizer.setup_comparison, BUTTON_COLOR),
        ("🎨 Theme", visualizer.toggle_theme, BUTTON_COLOR)
    ]
    
    for text, cmd, color in buttons:
        btn = tk.Button(button_frame, text=text, command=cmd,
                      bg=color, fg="white", relief=tk.FLAT)
        btn.pack(side=tk.LEFT, padx=2)
    
    # Checkboxes
    check_frame = tk.Frame(control_frame, bg=CONTROL_BG)
    check_frame.pack(side=tk.LEFT, padx=5)
    tk.Checkbutton(check_frame, text="Show Positions", variable=visualizer.show_positions,
                  bg=CONTROL_BG, fg="white", command=visualizer.redraw).pack(side=tk.LEFT)
    tk.Checkbutton(check_frame, text="Step Mode", variable=visualizer.step_mode,
                  bg=CONTROL_BG, fg="white").pack(side=tk.LEFT)
    
    # Info frame
    info_frame = tk.Frame(visualizer.left_frame, bg=BG_COLOR, padx=10, pady=5)
    info_frame.pack(fill=tk.X)
    
    visualizer.time_label = tk.Label(info_frame, text="Time: 0.00s", bg=BG_COLOR, fg="white")
    visualizer.time_label.pack(side=tk.LEFT, padx=10)
    
    visualizer.comparisons_label = tk.Label(info_frame, text="Comparisons: 0", bg=BG_COLOR, fg="white")
    visualizer.comparisons_label.pack(side=tk.LEFT, padx=10)
    
    visualizer.swaps_label = tk.Label(info_frame, text="Swaps: 0", bg=BG_COLOR, fg="white")
    visualizer.swaps_label.pack(side=tk.LEFT, padx=10)
    
    visualizer.accesses_label = tk.Label(info_frame, text="Array Accesses: 0", bg=BG_COLOR, fg="white")
    visualizer.accesses_label.pack(side=tk.LEFT, padx=10)
    
    visualizer.complexity_label = tk.Label(info_frame, text="O(n): ", bg=BG_COLOR, fg="white")
    visualizer.complexity_label.pack(side=tk.LEFT, padx=10)
    
    # Canvas for visualization
    visualizer.canvas = tk.Canvas(visualizer.left_frame, bg=BG_COLOR, height=500, highlightthickness=0)
    visualizer.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Complexity graph
    visualizer.complexity_canvas = tk.Canvas(visualizer.left_frame, bg=BG_COLOR, height=100, highlightthickness=0)
    visualizer.complexity_canvas.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    # Right panel contents
    visualizer.notebook = ttk.Notebook(visualizer.right_frame)
    visualizer.notebook.pack(fill=tk.BOTH, expand=True)
    
    # Pseudocode tab with resize handle
    pseudocode_frame = tk.Frame(visualizer.notebook, bg=CONSOLE_BG)
    visualizer.notebook.add(pseudocode_frame, text="Pseudocode")
    visualizer.pseudocode_text = scrolledtext.ScrolledText(
        pseudocode_frame, bg=CONSOLE_BG, fg=CONSOLE_TEXT,
        wrap=tk.WORD, state='disabled', font=('Consolas', 10))
    visualizer.pseudocode_text.pack(fill=tk.BOTH, expand=True)
    add_resize_handle(pseudocode_frame)
    
    # Console tab with resize handle
    console_frame = tk.Frame(visualizer.notebook, bg=CONSOLE_BG)
    visualizer.notebook.add(console_frame, text="Console")
    visualizer.console = scrolledtext.ScrolledText(
        console_frame, bg=CONSOLE_BG, fg=CONSOLE_TEXT,
        wrap=tk.WORD, state='disabled', font=('Consolas', 10))
    visualizer.console.pack(fill=tk.BOTH, expand=True)
    add_resize_handle(console_frame)
    
    # Complexity tab with resize handle
    complexity_frame = tk.Frame(visualizer.notebook, bg=CONSOLE_BG)
    visualizer.notebook.add(complexity_frame, text="Complexity")
    visualizer.complexity_text = tk.Text(
        complexity_frame, bg=CONSOLE_BG, fg=CONSOLE_TEXT,
        wrap=tk.WORD, state='disabled', font=('Consolas', 10))
    visualizer.complexity_text.pack(fill=tk.BOTH, expand=True)
    add_resize_handle(complexity_frame)
    
    # Update algorithm info display
    visualizer.update_algorithm_info()

def add_resize_handle(parent):
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