# 📞 Registro de Llamadas (Desktop App)

Aplicación de escritorio desarrollada en Python para gestionar y registrar llamadas de forma sencilla, visual y eficiente.

---

## 🚀 Características

* 📋 Registro de llamadas con:

  * Fecha
  * Hora
  * Quién llama
  * Teléfono
  * Destino
  * Motivo
  * Solución

* 🔍 Buscador integrado (filtro en tiempo real)

* 🎨 Interfaz moderna y colorida

* 📅 Selector de fecha (formato dd/MM/yyyy)

* ✏️ Edición de registros (doble clic)

* ✅ Estados visuales:

  * Pendiente (rojo claro)
  * Resuelto (verde claro)

* 📤 Exportación a Excel

* 💾 Guardado automático en JSON

* 🖥️ Ejecutable (.exe) sin necesidad de instalar Python

---

## 📂 Estructura del proyecto

```
registro-llamadas/
│
├── app_llamadas.py
├── icono.ico
├── llamadas.json
├── instalador.iss
├── dist/
│   └── app_llamadas.exe
```

---

## 🛠️ Requisitos (para desarrollo)

* Python 3.11 recomendado
* Librerías:

```bash
pip install tkcalendar openpyxl pyinstaller
```

## 💾 Almacenamiento de datos

Los datos se guardan automáticamente en:

```
Documentos/RegistroLlamadas/llamadas.json

---

## 🎯 Tecnologías utilizadas

* Python
* Tkinter (interfaz gráfica)
* tkcalendar
* openpyxl
* PyInstaller
* Inno Setup

---

## 📌 Notas

* No requiere conexión a internet
* No necesita base de datos externa
* Ligera y fácil de usar

---

## 📄 Licencia

Uso libre para fines educativos y personales.
