import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta

# ventana principal del programa
root = tk.Tk()
root.title("Gestión de activos")

# marco para organizar los widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# marco para mostrar los datos
data_frame = ttk.Frame(root, padding="10")
data_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Almacenar los datos de los procesos
procesos = []

#  Estilos
style = ttk.Style(root)
style.configure("Green.TLabel", background="#98fb98")
style.configure("Yellow.TLabel", background="#ffffe0")
style.configure("Blue.TLabel", background="#add8e6")
style.configure("Red.TLabel", background="#ffcccb")

# Guardar los datos en el archivo
def guardar_datos():
    with open("procesos.txt", "w") as file:
        json.dump(procesos, file)

# Cargar los datos desde el archivo
def cargar_datos():
    global procesos
    if os.path.exists("procesos.txt"):
        try:
            with open("procesos.txt", "r") as file:
                procesos = json.load(file)
        except json.decoder.JSONDecodeError:
            procesos = []
    # timestamp 
    for proceso in procesos:
        if "Timestamp" not in proceso:
            proceso["Timestamp"] = datetime.now().isoformat()
    guardar_datos()  # para guardar los datos
    mostrar_datos()

# Guardar la información 
def guardar():
    datos = {
        "Worker": worker_var.get(),
        "Correo": correo_var.get(),
        "Cargo": cargo_var.get(),
        "Área": area_var.get(),
        "Cambio de Equipo": cambio_equipo_var.get(),
        "Especificación Técnica Requerida": especificacion_var.get(),
        "APPS": apps_var.get(),
        "Status": status_var.get(),
        "Help Desk": helpdesk_var.get(),
        "Equipo Actual": equipo_actual_var.get(),
        "Timestamp": datetime.now().isoformat()
    }
    procesos.append(datos)
    guardar_datos()
    mostrar_datos()

# Función para eliminar un proceso
def eliminar(proceso):
    procesos.remove(proceso)
    guardar_datos()
    mostrar_datos()

# Función para mostrar los datos
def mostrar_datos():
    for widget in data_frame.winfo_children():
        widget.destroy()
    
    headers = ["Worker", "Correo", "Cargo", "Área", "Cambio de Equipo", "Especificación Técnica Requerida", "APPS", "Status", "Help Desk", "Equipo Actual", "Timestamp", "Eliminar"]
    
    for col, header in enumerate(headers):
        ttk.Label(data_frame, text=header).grid(row=0, column=col, padx=5, pady=5)
    
    for row, proceso in enumerate(procesos, start=1):
        for col, header in enumerate(headers[:-2]): 
            if header == "Status":
                status_var = tk.StringVar(value=proceso[header])
                status_menu = tk.OptionMenu(data_frame, status_var, "Pendiente Cambio", "Bodega", "Retirado", "En Preparacion",
                                            command=lambda new_status, r=row-1: actualizar_status(new_status, r))
                status_menu.grid(row=row, column=col, padx=5, pady=5)
                actualizar_color(status_menu, proceso, "optionmenu", status_var.get())
            else:
                ttk.Label(data_frame, text=proceso[header]).grid(row=row, column=col, padx=5, pady=5)
        
        # Mostrar el tiempo que ha transcurrido
        timestamp_label = ttk.Label(data_frame, text=calcular_tiempo(proceso["Timestamp"]))
        timestamp_label.grid(row=row, column=len(headers)-2, padx=5, pady=5)
        actualizar_color(timestamp_label, proceso, "label", None)  # Actualizar el color del timestamp
        
        # Botón de eliminar los procesos
        ttk.Button(data_frame, text="Eliminar", command=lambda p=proceso: eliminar(p)).grid(row=row, column=len(headers)-1, padx=5, pady=5)

    # Actualizar colores 
    root.after(60000, mostrar_datos)  # se debe actualizar cada minuto 

# calcular el tiempo transcurrido desde el timestamp 
def calcular_tiempo(timestamp):
    try:
        timestamp_dt = datetime.fromisoformat(timestamp)
    except ValueError:
        return "N/A"
    elapsed_time = datetime.now() - timestamp_dt
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m"

# Actualizar el estado en la lista de procesos
def actualizar_status(new_status, row):
    procesos[row]["Status"] = new_status
    guardar_datos()
    mostrar_datos()  # Llama a la función para mostrar datos,para actualizar el color

#  Actualizar el color basado en el estado y el tiempo transcurrido
def actualizar_color(widget, proceso, widget_type, status):
    try:
        timestamp = datetime.fromisoformat(proceso["Timestamp"])
    except KeyError:
        timestamp = datetime.now()
        proceso["Timestamp"] = timestamp.isoformat()
    elapsed_time = datetime.now() - timestamp
    hours = elapsed_time.total_seconds() // 3600

    if widget_type == "label":
        if hours < 5:
            widget.config(background="#98fb98")  
        elif hours < 10:
            widget.config(background="#ffffe0")  
        elif hours < 15:
            widget.config(background="#add8e6")  
        else:
            widget.config(background="#ffcccb")  

    elif widget_type == "optionmenu":
        colores = {
            "Pendiente Cambio": "#add8e6",  
            "Bodega": "#ffffe0",            
            "Retirado": "#98fb98",          
            "En Preparacion": "#ffcccb"     
        }
        bg_color = colores.get(status, "white")
        widget.config(background=bg_color)

# Variables para actulizar campos
worker_var = tk.StringVar()
correo_var = tk.StringVar()
cargo_var = tk.StringVar()
area_var = tk.StringVar()
cambio_equipo_var = tk.StringVar()
especificacion_var = tk.StringVar()
apps_var = tk.StringVar()
helpdesk_var = tk.StringVar()
equipo_actual_var = tk.StringVar()
status_var = tk.StringVar()

# Etiquetas y campos de entrada 
fields = [
    ("Worker", worker_var),
    ("Correo", correo_var),
    ("Cargo", cargo_var),
    ("Área", area_var),
    ("Cambio de Equipo", cambio_equipo_var),
    ("Especificación Técnica Requerida", especificacion_var),
    ("APPS", apps_var),
    ("Help Desk", helpdesk_var),
    ("Equipo Actual", equipo_actual_var),
]

for i, (label_text, var) in enumerate(fields):
    ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
    ttk.Entry(frame, textvariable=var).grid(row=i, column=1, pady=2)

# Menú desplegable con colores para el campo de estado 
def actualizar_color_entry(*args):
    estado = status_var.get()
    colores = {
        "Pendiente Cambio": "#add8e6",  
        "Bodega": "#ffffe0",            
        "Retirado": "#98fb98",          
        "En Preparacion": "#ffcccb"     
    }
    bg_color = colores.get(estado, "white")
    status_menu.config(background=bg_color)

status_var.trace("w", actualizar_color_entry)

status_menu = tk.OptionMenu(frame, status_var, "Pendiente Cambio", "Bodega", "Retirado", "En Preparacion")
status_menu.grid(row=len(fields), column=1, pady=2, sticky="ew")
ttk.Label(frame, text="Status").grid(row=len(fields), column=0, sticky=tk.W, pady=2)

# Botón para guardar la información
ttk.Button(frame, text="Guardar", command=guardar).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

# Cargar datos desde el archivo al iniciar la aplicación
cargar_datos()

# Bucle principal de la aplicación
root.mainloop()
