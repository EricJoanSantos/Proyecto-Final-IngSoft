import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import numpy as np
import os

# Diccionario para almacenar los usuarios y sus datos
usuarios = {}

# Función para cargar los usuarios desde los archivos individuales
def cargar_usuarios():
    usuarios = {}
    usuarios_dir = "usuarios"
    if not os.path.exists(usuarios_dir):
        os.makedirs(usuarios_dir)

    for filename in os.listdir(usuarios_dir):
        if filename.endswith(".txt"):
            usuario = filename[:-4]
            with open(os.path.join(usuarios_dir, filename), "r") as file:
                contraseña = file.readline().strip()
                dinero_disponible = float(file.readline().strip())  # Leer dinero disponible
                balance_actual = float(file.readline().strip())  # Leer balance actual
                balance_proyectado = float(file.readline().strip())  # Leer balance proyectado
                gasto_proyectado = float(file.readline().strip())  # Leer gasto proyectado
                usuarios[usuario] = {"contraseña": contraseña, "cuentas": {"dinero_disponible": dinero_disponible, "balance_actual": balance_actual, "balance_proyectado": balance_proyectado, "gasto_proyectado": gasto_proyectado}}
    return usuarios

# Función para guardar el usuario en un archivo individual
def guardar_usuario(usuario, contraseña, cuentas):
    usuarios_dir = "usuarios"
    if not os.path.exists(usuarios_dir):
        os.makedirs(usuarios_dir)

    filename = os.path.join(usuarios_dir, f"{usuario}.txt")
    with open(filename, "w") as file:
        file.write(contraseña + "\n")
        file.write(str(cuentas["dinero_disponible"]) + "\n")
        file.write(str(cuentas["balance_actual"]) + "\n")
        file.write(str(cuentas["balance_proyectado"]) + "\n")
        file.write(str(cuentas["gasto_proyectado"]) + "\n")

# Función para guardar los usuarios y cerrar la ventana
def guardar_usuarios():
    for usuario, datos in usuarios.items():
        guardar_usuario(usuario, datos["contraseña"], datos["cuentas"])
    root.destroy()

# Función para inicializar el programa
def inicializar_programa():
    global usuarios
    # Cargar los usuarios existentes
    usuarios = cargar_usuarios()

# Función para mostrar la barra de navegación después del inicio de sesión exitoso
def mostrar_barra_navegacion():
    login_frame.pack_forget()
    nav_frame.pack(side=tk.LEFT, fill=tk.Y)

# Función para iniciar sesión
def login():
    usuario = username_entry.get()
    contraseña = password_entry.get()

    if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
        messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {usuario}!")
        mostrar_cuentas(usuario)
        mostrar_barra_navegacion()
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")

# Función para cerrar sesión
def cerrar_sesion():
    nav_frame.pack_forget()
    login_frame.pack()

# Función para registrar un nuevo usuario
def registrar():
    usuario = username_entry.get()
    contraseña = password_entry.get()

    if usuario in usuarios:
        messagebox.showerror("Error de registro", "El usuario ya existe, por favor elija otro.")
    else:
        usuarios[usuario] = {"contraseña": contraseña, "cuentas": {"dinero_disponible": 0, "balance_actual": 0, "balance_proyectado": 0, "gasto_proyectado": 0}}
        guardar_usuarios()
        messagebox.showinfo("Registro exitoso", f"Usuario '{usuario}' registrado correctamente.")

# Función para mostrar las cuentas del usuario
def mostrar_cuentas(usuario):
    global usuario_actual
    usuario_actual = usuario  # Almacenar el usuario actual
    # Obtener datos de las cuentas del usuario
    cuentas_usuario = usuarios[usuario]["cuentas"]
    dinero_disponible = cuentas_usuario["dinero_disponible"]
    gasto_proyectado = cuentas_usuario["gasto_proyectado"]

    # Calcular el balance actual
    balance_actual = dinero_disponible - gasto_proyectado

    # Actualizar etiquetas de las cuentas
    dinero_disponible_label.config(text=f"Dinero disponible: ${dinero_disponible}")
    balance_actual_label.config(text=f"Balance actual: ${balance_actual}")
    gasto_proyectado_label.config(text=f"Gasto: ${gasto_proyectado}")



# Función para agregar dinero a la cuenta del usuario

def agregar_dinero():
    usuario = username_entry.get()
    cantidad = float(cantidad_entry.get())  # Obtener la cantidad ingresada por el usuario
    if usuario in usuarios:
        # Actualizar el dinero disponible del usuario
        usuarios[usuario]["cuentas"]["dinero_disponible"] += cantidad
        # Actualizar el balance actual del usuario
        usuarios[usuario]["cuentas"]["balance_actual"] += cantidad
        # Actualizar las cuentas en el archivo
        guardar_usuario(usuario, usuarios[usuario]["contraseña"], usuarios[usuario]["cuentas"])
        # Mostrar un mensaje de confirmación
        messagebox.showinfo("Dinero agregado", f"Se agregaron ${cantidad} a tu cuenta")
        # Actualizar las etiquetas de las cuentas
        mostrar_cuentas(usuario)
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

# Función para resetear el dinero disponible a cero
def resetear_dinero():
    usuario = username_entry.get()
    if usuario in usuarios:
        # Establecer el dinero disponible del usuario a cero
        usuarios[usuario]["cuentas"]["dinero_disponible"] = 0
        # Establecer el balance actual y el balance proyectado del usuario a cero
        usuarios[usuario]["cuentas"]["balance_actual"] = 0
        usuarios[usuario]["cuentas"]["balance_proyectado"] = 0
        # Establecer el gasto proyectado del usuario a cero
        usuarios[usuario]["cuentas"]["gasto_proyectado"] = 0
        # Actualizar las cuentas en el archivo
        guardar_usuario(usuario, usuarios[usuario]["contraseña"], usuarios[usuario]["cuentas"])
        # Mostrar un mensaje de confirmación
        messagebox.showinfo("Dinero reseteado", "El dinero disponible se ha reseteado a cero")
        # Actualizar las etiquetas de las cuentas
        mostrar_cuentas(usuario)
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

# Función para registrar un ingreso
def registrar_ingreso():
    usuario = username_entry.get()
    monto = float(ingreso_monto_entry.get())
    descripcion = ingreso_descripcion_entry.get()
    fecha = ingreso_fecha_entry.get()
    if usuario in usuarios:
        # Actualizar las cuentas del usuario
        usuarios[usuario]["cuentas"]["dinero_disponible"] += monto
        # Guardar el registro del ingreso
        with open("historial_transacciones.txt", "a") as file:
            file.write(f"Ingreso: ${monto} - Descripción: {descripcion} - Fecha: {fecha}\n")
        # Mostrar un mensaje de confirmación
        messagebox.showinfo("Ingreso registrado", "Se ha registrado el ingreso correctamente")
        # Actualizar las etiquetas de las cuentas
        mostrar_cuentas(usuario)
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

# Función para registrar un gasto
def registrar_gasto():
    usuario = username_entry.get()
    monto = float(gasto_monto_entry.get())
    descripcion = gasto_descripcion_entry.get()
    fecha = gasto_fecha_entry.get()
    if usuario in usuarios:
        # Verificar si el usuario tiene suficiente dinero disponible para realizar el gasto
        if usuarios[usuario]["cuentas"]["dinero_disponible"] >= monto:
            # Actualizar las cuentas del usuario
            usuarios[usuario]["cuentas"]["dinero_disponible"] -= monto
            usuarios[usuario]["cuentas"]["balance_actual"] -= monto  # Actualizar el balance actual
            usuarios[usuario]["cuentas"]["gasto_proyectado"] += monto
            # Guardar el registro del gasto
            with open("historial_transacciones.txt", "a") as file:
                file.write(f"Gasto: ${monto} - Descripción: {descripcion} - Fecha: {fecha}\n")
            # Mostrar un mensaje de confirmación
            messagebox.showinfo("Gasto registrado", "Se ha registrado el gasto correctamente")
            # Actualizar las etiquetas de las cuentas
            mostrar_cuentas(usuario)
        else:
            messagebox.showerror("Error", "Fondos insuficientes para realizar el gasto")
    else:
        messagebox.showerror("Error", "Usuario no encontrado")
# Configuración de la ventana
root = tk.Tk()
root.title("Bienvenido a tu Gestor de Finanzas")

# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Configurar el tamaño y la posición de la ventana
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Etiqueta de bienvenida
welcome_label = tk.Label(root, text="Bienvenido a tu Gestor de Finanzas", font=("Arial", 20))
welcome_label.pack(pady=20)

# Marco para el inicio de sesión
login_frame = tk.Frame(root)
login_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Etiquetas y campos de entrada para el inicio de sesión
username_label = tk.Label(login_frame, text="Usuario:", font=("Arial", 16))
username_label.grid(row=0, column=0, padx=10, pady=5)

username_entry = tk.Entry(login_frame, font=("Arial", 16))
username_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = tk.Label(login_frame, text="Contraseña:", font=("Arial", 16))
password_label.grid(row=1, column=0, padx=10, pady=5)

password_entry = tk.Entry(login_frame, show="*", font=("Arial", 16))
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Botón de inicio de sesión
login_button = tk.Button(login_frame, text="Iniciar sesión", font=("Arial", 16), command=login)
login_button.grid(row=2, columnspan=2, padx=10, pady=5, sticky="ew")

# Botón de registro
register_button = tk.Button(login_frame, text="Registrar", font=("Arial", 16), command=registrar)
register_button.grid(row=3, columnspan=2, padx=10, pady=5, sticky="ew")

# Marco para la barra de navegación
nav_frame = tk.Frame(root)

# Barra de navegación (pestañas)
tabs = ttk.Notebook(nav_frame)

# Pestaña de cuentas
cuentas_frame = tk.Frame(tabs)
tabs.add(cuentas_frame, text="Cuentas")

# Etiqueta de la cantidad a agregar
cantidad_label = tk.Label(cuentas_frame, text="Cantidad a agregar:", font=("Arial", 16))
cantidad_label.pack(pady=10)

# Campo de entrada para la cantidad
cantidad_entry = tk.Entry(cuentas_frame, font=("Arial", 16))
cantidad_entry.pack(pady=5)

# Botón para agregar dinero
agregar_dinero_button = tk.Button(cuentas_frame, text="Agregar dinero", font=("Arial", 16), command=agregar_dinero)
agregar_dinero_button.pack(pady=10)

# Botón para resetear el dinero disponible
resetear_dinero_button = tk.Button(cuentas_frame, text="Resetear dinero", font=("Arial", 16), command=resetear_dinero)
resetear_dinero_button.pack(pady=10)

# Etiquetas de cuentas
dinero_disponible_label = tk.Label(cuentas_frame, text="Dinero disponible: $0", font=("Arial", 16))
dinero_disponible_label.pack(pady=10)

balance_actual_label = tk.Label(cuentas_frame, text="Balance actual: $0", font=("Arial", 16))
balance_actual_label.pack(pady=10)

gasto_proyectado_label = tk.Label(cuentas_frame, text="Gasto: $0", font=("Arial", 16))
gasto_proyectado_label.pack(pady=10)

# Pestaña de acciones
acciones_frame = tk.Frame(tabs)
tabs.add(acciones_frame, text="Acciones")

# Etiquetas y campos de entrada para ingresos
ingreso_monto_label = tk.Label(acciones_frame, text="Monto (ingreso):", font=("Arial", 16))
ingreso_monto_label.grid(row=0, column=0, padx=10, pady=5)
ingreso_monto_entry = tk.Entry(acciones_frame, font=("Arial", 16))
ingreso_monto_entry.grid(row=0, column=1, padx=10, pady=5)

ingreso_descripcion_label = tk.Label(acciones_frame, text="Descripción (ingreso):", font=("Arial", 16))
ingreso_descripcion_label.grid(row=1, column=0, padx=10, pady=5)
ingreso_descripcion_entry = tk.Entry(acciones_frame, font=("Arial", 16))
ingreso_descripcion_entry.grid(row=1, column=1, padx=10, pady=5)

ingreso_fecha_label = tk.Label(acciones_frame, text="Fecha (ingreso):", font=("Arial", 16))
ingreso_fecha_label.grid(row=2, column=0, padx=10, pady=5)
ingreso_fecha_entry = tk.Entry(acciones_frame, font=("Arial", 16))
ingreso_fecha_entry.grid(row=2, column=1, padx=10, pady=5)

# Botón para registrar ingreso
registrar_ingreso_button = tk.Button(acciones_frame, text="Registrar Ingreso", font=("Arial", 16), command=registrar_ingreso)
registrar_ingreso_button.grid(row=3, columnspan=2, padx=10, pady=5, sticky="ew")

# Etiquetas y campos de entrada para gastos
gasto_monto_label = tk.Label(acciones_frame, text="Monto (gasto):", font=("Arial", 16))
gasto_monto_label.grid(row=4, column=0, padx=10, pady=5)
gasto_monto_entry = tk.Entry(acciones_frame, font=("Arial", 16))
gasto_monto_entry.grid(row=4, column=1, padx=10, pady=5)

gasto_descripcion_label = tk.Label(acciones_frame, text="Descripción (gasto):", font=("Arial", 16))
gasto_descripcion_label.grid(row=5, column=0, padx=10, pady=5)
gasto_descripcion_entry = tk.Entry(acciones_frame, font=("Arial", 16))
gasto_descripcion_entry.grid(row=5, column=1, padx=10, pady=5)

gasto_fecha_label = tk.Label(acciones_frame, text="Fecha (gasto):", font=("Arial", 16))
gasto_fecha_label.grid(row=6, column=0, padx=10, pady=5)
gasto_fecha_entry = tk.Entry(acciones_frame, font=("Arial", 16))
gasto_fecha_entry.grid(row=6, column=1, padx=10, pady=5)

# Pestaña de historial
historial_frame = tk.Frame(tabs)
tabs.add(historial_frame, text="Historial")

# Etiqueta de historial
historial_label = tk.Label(historial_frame, text="Historial de transacciones", font=("Arial", 16))
historial_label.pack(pady=10)

# Lista para almacenar los registros de ingresos y gastos
historial_transacciones = []

# Función para mostrar el historial de transacciones
def mostrar_historial():
    # Limpiar el contenido actual del widget Text
    historial_text.delete(1.0, tk.END)
    
    # leer el archivo historial_transacciones.txt
    try:
        with open("historial_transacciones.txt", "r") as file:
            # Leer el contenido del archivo y mostrarlo en el widget Text
            historial_text.insert(tk.END, file.read())
    except FileNotFoundError:
        # Manejar el caso en que el archivo no existe
        historial_text.insert(tk.END, "No hay historial de transacciones.")


# Función para registrar una transacción en el historial
def registrar_transaccion(tipo, monto, descripcion, fecha):
    transaccion = f"{tipo}: ${monto} - Descripción: {descripcion} - Fecha: {fecha}"
    historial_transacciones.append(transaccion)
    mostrar_historial()

# Función para actualizar el historial de transacciones
def actualizar_historial():
    mostrar_historial()

# Función para eliminar los registros del historial
def eliminar_registros():
    with open("historial_transacciones.txt", "w") as file:
        file.write("")  # Escribir un string vacío para vaciar el archivo


# Crear el botón de actualizar
actualizar_button = tk.Button(historial_frame, text="Actualizar", font=("Arial", 16), command=actualizar_historial)
actualizar_button.pack(pady=10)

# Área de texto para mostrar el historial
historial_text = tk.Text(historial_frame, font=("Arial", 12), height=10, width=50)
historial_text.pack(pady=10)

# Crear el botón de eliminar registros
eliminar_registros_button = tk.Button(historial_frame, text="Eliminar registros", font=("Arial", 16), command=eliminar_registros)
eliminar_registros_button.pack(pady=10)

# Mostrar el historial inicialmente
mostrar_historial()

# Variable global para almacenar el usuario actual
usuario_actual = ""

# Función para actualizar la gráfica
def actualizar_grafica():
    if usuario_actual:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        # Obtener los datos para la gráfica
        nombres = ["Dinero Disponible", "Balance Actual", "Gastos"]
        valores = [usuarios[usuario_actual]["cuentas"]["dinero_disponible"],
                   usuarios[usuario_actual]["cuentas"]["balance_actual"],
                   usuarios[usuario_actual]["cuentas"]["gasto_proyectado"]]
        
        # Crear un arreglo de índices para las barras
        x = np.arange(len(nombres))
        
        # Dibujar la gráfica de líneas
        ax.plot(nombres, valores, marker='o', linestyle='-')
        
        # Etiquetas y título
        ax.set_ylabel('Valores')
        ax.set_title('Estado Financiero')
        
        # Mostrar la gráfica
        plt.show()

# Pestaña de gráfica
grafica_frame = tk.Frame(tabs)
tabs.add(grafica_frame, text="Gráfica")

# Botón para actualizar la gráfica
actualizar_grafica_button = tk.Button(grafica_frame, text="Actualizar Gráfica", font=("Arial", 16), command=actualizar_grafica)
actualizar_grafica_button.pack(padx=10, pady=10)
# Botón para cerrar sesión
cerrar_sesion_button = tk.Button(root, text="Cerrar sesión", font=("Arial", 16), command=cerrar_sesion)
cerrar_sesion_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Botón para registrar gasto
registrar_gasto_button = tk.Button(acciones_frame, text="Registrar Gasto", font=("Arial", 16), command=registrar_gasto)
registrar_gasto_button.grid(row=7, columnspan=2, padx=10, pady=5, sticky="ew")

# Empaquetar pestañas
tabs.pack(fill=tk.BOTH, expand=True)

# Botón para cerrar sesión
cerrar_sesion_button = tk.Button(root, text="Cerrar sesión", font=("Arial", 16), command=cerrar_sesion)
cerrar_sesion_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Cerrar la ventana al cerrar la aplicación
root.protocol("WM_DELETE_WINDOW", guardar_usuarios)

# Inicializar el programa
inicializar_programa()

# Ejecutar la aplicación
root.mainloop()




