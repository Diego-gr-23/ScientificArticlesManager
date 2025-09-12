# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from hashFNV1 import TablaHash
import uuid

# Instancia de la tabla hash
tabla = TablaHash()


# ==============================
# Funciones de la interfaz
# ==============================
def agregar_articulo():
    title = entry_title.get()
    authors = entry_authors.get()
    year = entry_year.get()
    filename = entry_filename.get()

    if not title or not authors or not year or not filename:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Usamos un hash único simulado (puedes cambiarlo por tu función hash real de archivo)
    hash_id = str(uuid.uuid4())[:8]

    tabla.insertar(hash_id, title, authors, year, filename)
    messagebox.showinfo("Éxito", f"Artículo '{title}' agregado correctamente.")
    limpiar_campos()
    mostrar_tabla()


def mostrar_tabla():
    # Limpiar tabla
    for row in tree.get_children():
        tree.delete(row)

    # Llenar con datos de la tabla hash
    for i in range(tabla.size):
        actual = tabla.tabla[i]
        while actual:
            tree.insert("", "end", values=(actual.hash_id, actual.title, actual.authors, actual.year, actual.filename))
            actual = actual.next


def buscar_articulo():
    hash_id = entry_buscar.get()
    if not hash_id:
        messagebox.showwarning("Campo vacío", "Ingresa un hash para buscar.")
        return

    articulo = tabla.buscar(hash_id)
    if articulo:
        messagebox.showinfo("Encontrado",
                            f"Título: {articulo.title}\nAutor(es): {articulo.authors}\nAño: {articulo.year}\nArchivo: {articulo.filename}")
    else:
        messagebox.showerror("No encontrado", "No existe un artículo con ese hash.")


def limpiar_campos():
    entry_title.delete(0, tk.END)
    entry_authors.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_filename.delete(0, tk.END)


# ==============================
# Ventana principal
# ==============================
root = tk.Tk()
root.title("Gestor de Artículos Científicos")
root.geometry("800x500")

# Frame para formulario
frame_form = tk.Frame(root, padx=10, pady=10)
frame_form.pack(side="top", fill="x")

tk.Label(frame_form, text="Título:").grid(row=0, column=0, sticky="e")
entry_title = tk.Entry(frame_form, width=40)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Autor(es):").grid(row=1, column=0, sticky="e")
entry_authors = tk.Entry(frame_form, width=40)
entry_authors.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Año:").grid(row=2, column=0, sticky="e")
entry_year = tk.Entry(frame_form, width=40)
entry_year.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Archivo (.txt):").grid(row=3, column=0, sticky="e")
entry_filename = tk.Entry(frame_form, width=40)
entry_filename.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_form, text="Agregar Artículo", command=agregar_articulo)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# Frame búsqueda
frame_search = tk.Frame(root, padx=10, pady=10)
frame_search.pack(side="top", fill="x")

tk.Label(frame_search, text="Buscar por Hash:").grid(row=0, column=0, sticky="e")
entry_buscar = tk.Entry(frame_search, width=30)
entry_buscar.grid(row=0, column=1, padx=5, pady=5)

btn_buscar = tk.Button(frame_search, text="Buscar", command=buscar_articulo)
btn_buscar.grid(row=0, column=2, padx=5)

# Tabla de artículos
columns = ("hash", "title", "authors", "year", "filename")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.pack(fill="both", expand=True, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=120)

# Inicializar tabla vacía
mostrar_tabla()

# Iniciar loop de la app
root.mainloop()
