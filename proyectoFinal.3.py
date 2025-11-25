import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk  # Necesita instalar pillow: pip install pillow
import os
from datetime import datetime  # Para manejar la fecha y hora

# -------------------------
# FUNCIONES (pantallas vacías por ahora)
# -------------------------

def mostrar_ticket(producto, precio, cantidad, total):
    # Crear una nueva ventana emergente (Toplevel)
    ticket = tk.Toplevel()
    ticket.title("Ticket de Venta")
    ticket.geometry("300x400")  # Tamaño ajustado para incluir el logo
    ticket.resizable(False, False)

    # Fecha y hora actual
    fecha_hora = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

    # Cargar el logo para el ticket
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        imagen = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))  # Usa el mismo archivo del logo
        imagen = imagen.resize((80, 80))  # Ajusta el tamaño del logo en el ticket
        img_logo_ticket = ImageTk.PhotoImage(imagen)

        lbl_logo_ticket = tk.Label(ticket, image=img_logo_ticket)
        lbl_logo_ticket.image = img_logo_ticket  # Guardar la referencia de la imagen
        lbl_logo_ticket.pack(pady=10)
    except:
        print("No se pudo cargar el logo para el ticket.")

    # Texto del ticket
    texto = (
        " *** PUNTO DE VENTA ***\n"
        "--------------------------------------\n"
        f"Fecha: {fecha_hora}\n"
        "--------------------------------------\n"
        f"Producto: {producto}\n"
        f"Precio: ${precio}\n"
        f"Cantidad: {cantidad}\n"
        "--------------------------------------\n"
        f"TOTAL: ${total}\n"
        "--------------------------------------\n"
        " ¡GRACIAS POR SU COMPRA!\n"
    )

    # Etiqueta con el texto del ticket
    lbl_ticket = tk.Label(ticket, text=texto, justify="left", font=("Consolas", 11))
    lbl_ticket.pack(pady=15)

    # Botón para cerrar la ventana emergente
    btn_cerrar = ttk.Button(ticket, text="Cerrar", command=ticket.destroy)
    btn_cerrar.pack(pady=10)

def abrir_registro_productos():
    reg = tk.Toplevel()
    reg.title("Registro de Productos")
    reg.geometry("400x400")
    reg.resizable(False, False)

    # --- Etiquetas y Campos de Texto ---
    lbl_id = tk.Label(reg, text="ID del Producto:", font=("impact", 12))
    lbl_id.pack(pady=5)
    txt_id = tk.Entry(reg, font=("Arial", 12), justify="center")
    txt_id.pack(pady=5)
    lbl_desc = tk.Label(reg, text="Descripción:", font=("impact", 12))
    lbl_desc.pack(pady=5)
    txt_desc = tk.Entry(reg, font=("Arial", 12), justify="center")
    txt_desc.pack(pady=5)
    lbl_precio = tk.Label(reg, text="Precio:", font=("impact", 12))
    lbl_precio.pack(pady=5)
    txt_precio = tk.Entry(reg, font=("Arial", 12), justify="center")
    txt_precio.pack(pady=5)
    lbl_categoria = tk.Label(reg, text="Categoría:", font=("impact", 12))
    lbl_categoria.pack(pady=5)
    txt_categoria = tk.Entry(reg, font=("Arial", 12), justify="center")
    txt_categoria.pack(pady=5)

    # --- Función para guardar ---
    def guardar_producto():
        id_prod = txt_id.get().strip()
        descripcion = txt_desc.get().strip()
        precio = txt_precio.get().strip()
        categoria = txt_categoria.get().strip()
        # Validaciones
        if id_prod == "" or descripcion == "" or precio == "" or categoria == "":
            messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
            return
        # Validar precio como número
        try:
            float(precio)
        except:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        # Guardar en archivo de texto
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR, "productos.txt")
        with open(archivo, "a", encoding="utf-8") as archivo:
            archivo.write(f"{id_prod}|{descripcion}|{precio}|{categoria}\n")
            messagebox.showinfo("Guardado", "Producto registrado correctamente.")
            # Limpiar campos
            txt_id.delete(0, tk.END)
            txt_desc.delete(0, tk.END)
            txt_precio.delete(0, tk.END)
            txt_categoria.delete(0, tk.END)

    # --- Botón Guardar ---
    btn_guardar = tk.Button(reg, text="Guardar Producto", command=guardar_producto)
    btn_guardar.pack(pady=20)

def abrir_registro_ventas():
    ven = tk.Toplevel()
    ven.title("Registro de Ventas")
    ven.geometry("420x430")
    ven.resizable(False, False)
    # ------------------------------------
    # Cargar productos desde productos.txt
    # ------------------------------------
    productos = {}
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivof = os.path.join(BASE_DIR, "productos.txt")
        with open(archivof, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    idp, desc, precio, cat = partes
                    productos[desc] = float(precio)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo productos.txt")
        ven.destroy()
        return

    # Lista de nombres de productos
    lista_productos = list(productos.keys())
    # ------------------------------------
    # CONTROLES VISUALES
    # ------------------------------------
    lbl_prod = tk.Label(ven, text="Producto:", font=("Arial", 12))
    lbl_prod.pack(pady=5)
    cb_producto = ttk.Combobox(ven, values=lista_productos, font=("Arial", 12), state="readonly")
    cb_producto.pack(pady=5)
    lbl_precio = tk.Label(ven, text="Precio:", font=("Arial", 12))
    lbl_precio.pack(pady=5)
    txt_precio = tk.Entry(ven, font=("Arial", 12), state="readonly")
    txt_precio.pack(pady=5)
    lbl_cantidad = tk.Label(ven, text="Cantidad:", font=("Arial", 12))
    lbl_cantidad.pack(pady=5)
    cantidad_var = tk.StringVar(ven)
    ven.cantidad_var = cantidad_var   # importante: mantiene la referencia
    txt_cantidad = tk.Entry(ven, font=("Arial", 12), textvariable=cantidad_var)
    txt_cantidad.pack(pady=5)  
    cantidad_var.trace_add("write", lambda *args: calcular_total())
    lbl_total = tk.Label(ven, text="Total:", font=("Arial", 12))
    lbl_total.pack(pady=5)
    txt_total = tk.Entry(ven, font=("Arial", 12), state="readonly")
    txt_total.pack(pady=5)
    # ------------------------------------
    # FUNCIONES
    # ------------------------------------
    def actualizar_precio(event):      
        prod = cb_producto.get()
        if prod in productos:
            txt_precio.config(state="normal")
            txt_precio.delete(0, tk.END)
            txt_precio.insert(0, productos[prod])
            txt_precio.config(state="readonly")
            calcular_total()
    
    def calcular_total(*args):      
        try:
            cant = int(txt_cantidad.get())
            precio = float(txt_precio.get())
            total = cant * precio
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.insert(0, total)
            txt_total.config(state="readonly")
        except:
            # Si no hay número válido, limpiar el total
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.config(state="readonly")

    def registrar_venta():
        prod = cb_producto.get()
        precio = txt_precio.get()
        cant = txt_cantidad.get()
        total = txt_total.get()
        if prod == "" or precio == "" or cant == "" or total == "":
            messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
            return
        # Guardar venta
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivov = os.path.join(BASE_DIR, "ventas.txt")
        with open(archivov, "a", encoding="utf-8") as archivo:
            archivo.write(f"{prod}|{precio}|{cant}|{total}\n")
            messagebox.showinfo("Venta Registrada", "La venta se registró correctamente.")
            
            # Mostrar el ticket de la venta
            mostrar_ticket(prod, precio, cant, total)

        # Limpiar campos
        cb_producto.set("")
        txt_precio.config(state="normal"); txt_precio.delete(0, tk.END); txt_precio.config(state="readonly")
        txt_cantidad.delete(0, tk.END)
        txt_total.config(state="normal"); txt_total.delete(0, tk.END); txt_total.config(state="readonly")
    
    # ------------------------------------
    # EVENTOS Y BOTÓN
    # ------------------------------------
    cb_producto.bind("<<ComboboxSelected>>", actualizar_precio)
    btn_guardar = ttk.Button(ven, text="Registrar Venta", command=registrar_venta)
    btn_guardar.pack(pady=25)

def abrir_reportes():
    messagebox.showinfo("Reportes", "Aquí irá el módulo de reportes.")

def abrir_acerca_de():
    messagebox.showinfo("Acerca de", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")

# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Punto de Venta - Ropa")
ventana.geometry("500x600")
ventana.resizable(False, False)

# -------------------------
# LOGO
# -------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagen = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))  # Cambia por el archivo del alumno
    imagen = imagen.resize((250, 250))  # Tamaño recomendado
    img_logo = ImageTk.PhotoImage(imagen)

    lbl_logo = tk.Label(ventana, image=img_logo)
    lbl_logo.image = img_logo  # Guardar la referencia de la imagen
    lbl_logo.pack(pady=20)
except:
    lbl_sin_logo = tk.Label(ventana, text="(Aquí va el logo del sistema)", font=("Arial", 14))
    lbl_sin_logo.pack(pady=40)

# -------------------------
# BOTONES PRINCIPALES
# -------------------------
btn_reg_prod = tk.Button(ventana, text="Registro de Productos", font=("Impact", 12), fg="white", bg="#09A9E9", relief="flat", command=abrir_registro_productos)
btn_reg_prod.pack(pady=10)

btn_reg_ventas = tk.Button(ventana, text="Registro de Ventas", font=("Impact", 12), fg="white", bg="#09A9E9", relief="flat", command=abrir_registro_ventas)
btn_reg_ventas.pack(pady=10)

btn_reportes = tk.Button(ventana, text="Reportes", font=("Impact", 12), fg="white", bg="#09A9E9", relief="flat", command=abrir_reportes)
btn_reportes.pack(pady=10)

btn_acerca = tk.Button(ventana, text="Acerca de", font=("Impact", 12), fg="white", bg="#09A9E9", relief="flat", command=abrir_acerca_de)
btn_acerca.pack(pady=10)

# -------------------------
# INICIO DE LA APP
# -------------------------
ventana.mainloop()
