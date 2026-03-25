import json
import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry
from openpyxl import Workbook
import os

CARPETA = os.path.join(os.environ["USERPROFILE"], "Documents", "RegistroLlamadas")
os.makedirs(CARPETA, exist_ok=True)

ARCHIVO = os.path.join(CARPETA, "llamadas.json")

# ---------------------- DATOS ----------------------
def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return []

def guardar_datos(datos):
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

# ---------------------- APP ----------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("📞 Registro de Llamadas PRO")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ecf0f1")

        style = ttk.Style()
        style.theme_use("clam")

        self.datos = cargar_datos()

        # 🔵 CABECERA
        top = Frame(root, bg="#34495e")
        top.pack(fill=X)
        Label(top, text="📞 Registro de Llamadas", fg="white", bg="#34495e",
              font=("Segoe UI", 18, "bold")).pack(pady=10)

        # 🔍 BUSCADOR
        frame_busqueda = Frame(root, bg="#ecf0f1")
        frame_busqueda.pack(fill=X, padx=10, pady=5)

        Label(frame_busqueda, text="Buscar:", bg="#ecf0f1", font=("Segoe UI", 11)).pack(side=LEFT)
        self.buscar_var = StringVar()
        Entry(frame_busqueda, textvariable=self.buscar_var, font=("Segoe UI", 11), width=30).pack(side=LEFT, padx=5)

        Button(frame_busqueda, text="🔍 Filtrar", bg="#3498db", fg="white",
               font=("Segoe UI", 10, "bold"), command=self.filtrar).pack(side=LEFT)

        # 📋 TABLA
        self.tree = ttk.Treeview(root, columns=("Dia","Hora","Quien","Telefono","Destino","Motivo","Estado","Solucion"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # 🎨 COLORES
        self.tree.tag_configure("pendiente", background="#f8d7da")
        self.tree.tag_configure("resuelto", background="#d4edda")

        self.tree.bind("<Double-1>", self.doble_click)

        # 🔘 BOTONES
        frame_botones = Frame(root, bg="#ecf0f1")
        frame_botones.pack(fill=X, padx=10, pady=10)

        Button(frame_botones, text="➕ Nueva", bg="#2ecc71", fg="white", width=12,
               font=("Segoe UI", 10, "bold"), command=self.nueva_llamada).pack(side=LEFT, padx=5)

        Button(frame_botones, text="✏️ Editar", bg="#f39c12", fg="white", width=12,
               font=("Segoe UI", 10, "bold"), command=self.editar).pack(side=LEFT, padx=5)

        Button(frame_botones, text="✅ Resuelto", bg="#27ae60", fg="white", width=12,
               font=("Segoe UI", 10, "bold"), command=self.marcar_resuelto).pack(side=LEFT, padx=5)

        Button(frame_botones, text="🗑 Eliminar", bg="#e74c3c", fg="white", width=12,
               font=("Segoe UI", 10, "bold"), command=self.eliminar).pack(side=LEFT, padx=5)

        Button(frame_botones, text="📤 Excel", bg="#8e44ad", fg="white", width=12,
               font=("Segoe UI", 10, "bold"), command=self.exportar_excel).pack(side=RIGHT, padx=5)

        self.cargar_tabla()

    def ordenar(self, datos):
        return sorted(datos, key=lambda d: datetime.strptime(d["dia"], "%d/%m/%Y"), reverse=True)

    def cargar_tabla(self, datos=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        datos = datos if datos else self.datos
        datos = self.ordenar(datos)

        for i, d in enumerate(datos):
            tag = "resuelto" if d["estado"] == "Resuelto" else "pendiente"
            self.tree.insert("", "end", iid=i, values=(
                d["dia"], d["hora"], d["quien_llama"], d["telefono"],
                d["destinatario"], d["motivo"], d["estado"], d["solucion"]
            ), tags=(tag,))

    def filtrar(self):
        texto = self.buscar_var.get().lower()
        filtrados = [d for d in self.datos if texto in str(d).lower()]
        self.cargar_tabla(filtrados)

    def doble_click(self, event):
        if self.tree.selection():
            self.editar()

    def nueva_llamada(self):
        self.formulario()

    def editar(self):
        if not self.tree.selection():
            return
        idx = int(self.tree.selection()[0])
        self.formulario(idx)

    def formulario(self, idx=None):
        v = Toplevel(self.root)
        v.title("Formulario")
        v.geometry("600x600")
        v.resizable(False, False)
        v.configure(bg="#ecf0f1")

        font = ("Segoe UI", 12)

        def campo(texto):
            Label(v, text=texto, font=font, bg="#ecf0f1").pack(anchor="w", padx=20)
            e = Entry(v, font=font)
            e.pack(fill=X, padx=20, pady=5)
            return e

        Label(v, text="Fecha", font=font, bg="#ecf0f1").pack(anchor="w", padx=20)
        fecha = DateEntry(v, date_pattern='dd/MM/yyyy', font=font)
        fecha.pack(fill=X, padx=20, pady=5)

        quien = campo("Quién llama")
        tel = campo("Teléfono")
        destino = campo("Destino")

        Label(v, text="Motivo", font=font, bg="#ecf0f1").pack(anchor="w", padx=20)
        motivo = Text(v, height=3, font=font)
        motivo.pack(fill=X, padx=20, pady=5)

        Label(v, text="Solución", font=font, bg="#ecf0f1").pack(anchor="w", padx=20)
        solucion = Text(v, height=3, font=font)
        solucion.pack(fill=X, padx=20, pady=5)

        if idx is not None:
            d = self.datos[idx]
            fecha.set_date(d["dia"])
            quien.insert(0, d["quien_llama"])
            tel.insert(0, d["telefono"])
            destino.insert(0, d["destinatario"])
            motivo.insert("1.0", d["motivo"])
            solucion.insert("1.0", d["solucion"])

        def guardar():
            nuevo = {
                "dia": fecha.get(),
                "hora": datetime.now().strftime("%H:%M"),
                "quien_llama": quien.get(),
                "telefono": tel.get(),
                "destinatario": destino.get(),
                "motivo": motivo.get("1.0", END).strip(),
                "estado": "Pendiente",
                "solucion": solucion.get("1.0", END).strip()
            }

            if idx is None:
                self.datos.append(nuevo)
            else:
                self.datos[idx] = nuevo

            guardar_datos(self.datos)
            self.cargar_tabla()
            v.destroy()

        botones = Frame(v, bg="#ecf0f1")
        botones.pack(pady=20)

        Button(botones, text="💾 Guardar", bg="#2ecc71", fg="white",
               font=("Segoe UI", 12, "bold"), width=15, height=2,
               command=guardar).pack(side=LEFT, padx=10)

        Button(botones, text="❌ Cancelar", bg="#bdc3c7",
               font=("Segoe UI", 12), width=15, height=2,
               command=v.destroy).pack(side=LEFT, padx=10)

    def marcar_resuelto(self):
        if not self.tree.selection():
            return
        idx = int(self.tree.selection()[0])
        self.datos[idx]["estado"] = "Resuelto"
        guardar_datos(self.datos)
        self.cargar_tabla()

    def eliminar(self):
        if not self.tree.selection():
            return
        idx = int(self.tree.selection()[0])
        del self.datos[idx]
        guardar_datos(self.datos)
        self.cargar_tabla()

    def exportar_excel(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if not ruta:
            return

        wb = Workbook()
        ws = wb.active

        ws.append(["Dia","Hora","Quien","Telefono","Destino","Motivo","Estado","Solucion"])

        for d in self.datos:
            ws.append([
                d["dia"], d["hora"], d["quien_llama"], d["telefono"],
                d["destinatario"], d["motivo"], d["estado"], d["solucion"]
            ])

        wb.save(ruta)
        messagebox.showinfo("OK", "Exportado correctamente")

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
