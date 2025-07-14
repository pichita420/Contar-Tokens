import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import tiktoken
import json
import os

MODELS = {
    "GPT-4o": "gpt-4o",
    "GPT-4": "gpt-4",
    "GPT-3.5 Turbo": "gpt-3.5-turbo"
}
TOKEN_LIMITS = {
    "gpt-4o": 128000,
    "gpt-4": 128000,
    "gpt-3.5-turbo": 16385
}

def contar_tokens(mensajes, modelo):
    enc = tiktoken.encoding_for_model(modelo)
    total = 0
    por_mensaje = []
    for m in mensajes:
        tk_count = 4
        for k in ["role", "content", "name"]:
            if k in m:
                tk_count += len(enc.encode(m[k]))
        por_mensaje.append(tk_count)
        total += tk_count
    total += 2
    return total, por_mensaje

def parse_lines(text):
    mensajes = []
    lines = text.strip().split('\n')
    for l in lines:
        l = l.strip()
        if not l: continue
        if l.startswith("Usuario:"):
            mensajes.append({"role": "user", "content": l[8:].strip()})
        elif l.startswith("Asistente:"):
            mensajes.append({"role": "assistant", "content": l[10:].strip()})
        elif l.startswith("Wolfram:"):
            mensajes.append({"role": "function", "name": "wolfram_alpha", "content": l[8:].strip()})
        elif l.startswith("{") and l.endswith("}"):
            try:
                msg = json.loads(l)
                mensajes.append(msg)
            except:
                continue
    return mensajes

def cargar_archivo():
    fname = filedialog.askopenfilename(filetypes=[("All files", "*.txt *.json")])
    if fname:
        ext = os.path.splitext(fname)[1].lower()
        with open(fname, "r", encoding="utf-8") as f:
            contenido = f.read()
            historial.delete("1.0", tk.END)
            if ext == ".json":
                try:
                    data = json.loads(contenido)
                    pretty = ""
                    if isinstance(data, list):
                        for msg in data:
                            pretty += json.dumps(msg, ensure_ascii=False) + "\n"
                    elif isinstance(data, dict):
                        pretty += json.dumps(data, ensure_ascii=False) + "\n"
                    historial.insert(tk.END, pretty)
                except:
                    historial.insert(tk.END, contenido)
            else:
                historial.insert(tk.END, contenido)

def guardar_resultados():
    datos = resultado.get("1.0", tk.END)
    fname = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if fname:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(datos)
        messagebox.showinfo("Guardado", f"Resultados guardados en:\n{fname}")

def calcular():
    modelo = MODELS[modelo_var.get()]
    mensajes = parse_lines(historial.get("1.0", tk.END))
    total, por_mensaje = contar_tokens(mensajes, modelo)
    limite = TOKEN_LIMITS[modelo]
    porc = (total / limite) * 100
    rest = 100 - porc
    res = f"Modelo: {modelo}\nTokens usados: {total}\nTokens restantes: {limite-total}\nPorcentaje usado: {porc:.2f}%\n"
    res += "\nTokens por mensaje:\n"
    for i, tkc in enumerate(por_mensaje, 1):
        res += f"  Mensaje {i}: {tkc}\n"
    if rest < 10:
        res += "\n🔴 ¡Advertencia! Menos del 10% de tokens restantes."
    elif rest < 20:
        res += "\n🟡 Atención: menos del 20% de tokens."
    else:
        res += "\n🟢 Puedes continuar."
    resultado.config(state="normal")
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, res)
    resultado.config(state="disabled")

def limpiar():
    historial.delete("1.0", tk.END)
    resultado.config(state="normal")
    resultado.delete("1.0", tk.END)
    resultado.config(state="disabled")

root = tk.Tk()
root.title("Contador de Tokens ChatGPT/Wolfram (Avanzado)")

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Abrir archivo...", command=cargar_archivo)
filemenu.add_command(label="Guardar resultados...", command=guardar_resultados)
filemenu.add_separator()
filemenu.add_command(label="Limpiar", command=limpiar)
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)
root.config(menu=menubar)

tk.Label(root, text="Historial (Usuario:, Asistente:, Wolfram: por línea o formato JSON):").pack(anchor="w")
historial = scrolledtext.ScrolledText(root, width=70, height=12)
historial.pack()

modelo_var = tk.StringVar(root)
modelo_var.set("GPT-4o")
tk.Label(root, text="Modelo:").pack(anchor="w")
tk.OptionMenu(root, modelo_var, *MODELS.keys()).pack(anchor="w")

tk.Button(root, text="Calcular tokens", command=calcular).pack(pady=7)

resultado = scrolledtext.ScrolledText(root, width=70, height=10, state="disabled", fg="blue")
resultado.pack()

root.mainloop()