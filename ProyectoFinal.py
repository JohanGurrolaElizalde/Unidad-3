import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesita instalar pillow: pip install pillow
import os

# -------------------------
# FUNCIONES (pantallas vacías por ahora)
# -------------------------
def abrir_registro_productos():
    reg = tk.Toplevel()
    reg.title("Registro de Productos")
    reg.geometry("400x400")
    reg.resizable(False, False)

   # --- Etiquetas y Campos de Texto ---
    lbl_id = tk.Label(reg, text="ID del Producto:", font=("impact", 12))
    lbl_id.pack(pady=5)
    txt_id = tk.Entry(reg, font=("Arial", 12),justify="center")
    txt_id.pack(pady=5)
    lbl_desc = tk.Label(reg, text="Descripción:", font=("impact", 12))
    lbl_desc.pack(pady=5)
    txt_desc = tk.Entry(reg, font=("Arial", 12),justify="center")
    txt_desc.pack(pady=5)
    lbl_precio = tk.Label(reg, text="Precio:", font=("impact", 12))
    lbl_precio.pack(pady=5)
    txt_precio = tk.Entry(reg, font=("Arial", 12), justify="center")
    txt_precio.pack(pady=5)
    lbl_categoria = tk.Label(reg, text="Categoría:", font=("impact", 12))
    lbl_categoria.pack(pady=5)
    txt_categoria = tk.Entry(reg, font=("Arial", 12),justify="center")
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
      archivo = os.path.join(BASE_DIR,"productos.txt")
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
    messagebox.showinfo("Registro de Ventas", "Aquí irá el módulo de registro de ventas.")

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
