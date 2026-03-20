# To-Do Web Applikation (OOP Projekt)

## 👥 Team

* Matthias Heiniger
* Lukas Fehr
* Wathanak Deng

---

## 📌 Projektbeschreibung

Dieses Projekt wird im Rahmen des Moduls **Objektorientierte Programmierung (OOP)** entwickelt.

Die neue Anwendung basiert auf einer **3-Schichten-Architektur**:

* Präsentationsschicht Frontend GUI (Browser mit NiceGUI)
* Anwendungslogik Backend (Python, objektorientiert, ORM)
* Persistenzschicht (SQLite mit ORM)

---

## 🏗️ Architektur

### 1. Präsentationsschicht (Frontend)

* Umsetzung mit **NiceGUI**
* UI wird serverseitig in Python definiert
* Darstellung im Browser (Thin Client)

### 2. Anwendungslogik (Backend)

* Implementierung in **Python**
* Strukturierung mit objektorientierter Programmierung (OOP)
* Trennung von Logik und Darstellung

### 3. Persistenzschicht (Datenbank)

* Verwendung von **SQLite**
* Zugriff über **SQLAlchemy (ORM)**
* Keine direkten SQL-Statements

---

## 🛠️ Technologien

* Python
* NiceGUI
* SQLAlchemy
* SQLite
* pytest
* GitHub
* VS Code

---

## ⚙️ Projekt Setup (lokale Umgebung)

### 1. Repository klonen

```bash
git clone <https://github.com/wathi22/oop_projektarbeit_to-do_applikation.git>
cd <REPOSITORY-NAME>
```

### 2. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
```

### 3. Virtuelle Umgebung aktivieren

**Windows (PowerShell):**

```bash
.venv\Scripts\Activate.ps1
```

**Falls Fehler (Execution Policy):**

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Alternative (immer möglich):**

```bash
.venv\Scripts\activate.bat
```

---

### 4. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

---

## ▶️ Anwendung starten

```bash
python app/main.py
```

👉 Danach öffnet sich die Anwendung im Browser.

---

## 🧪 Test der Umgebung

Die Umgebung ist korrekt eingerichtet, wenn:

* die Anwendung im Browser startet
* die UI angezeigt wird
* Buttons reagieren

---

## 🗄️ Datenbank

* Es wird **SQLite** verwendet
* Die Datenbank ist eine lokale Datei (`todo.db`)
* Sie wird automatisch erstellt, sobald sie verwendet wird

---

## 📁 Projektstruktur

```text
app/
  main.py
  ui/
  services/
  models/
  database/

docs/
tests/

README.md
requirements.txt
.gitignore
```

---

## 📄 Dokumentation

Die Projektdokumentation befindet sich im Ordner `docs/`:

---

## 💡 Hinweis

Dieses Projekt wird iterativ entwickelt. Die README und Dokumentation werden laufend erweitert.

---
