# conftest.py – Projektstamm
#
# Diese Datei wird von pytest automatisch erkannt und erfüllt zwei Aufgaben:
#
# 1. Markiert den Projektstamm für pytest (rootdir)
#    → pytest weiss wo das Projekt beginnt und sucht Tests ab hier
#
# 2. Zusammen mit pytest.ini (pythonpath = .) wird der Projektstamm
#    automatisch zum Python-Suchpfad hinzugefügt
#    → alle Imports wie "from app.src.todo import Todo" funktionieren
#    → keine manuellen sys.path Anpassungen nötig
#
# Resultat: Jeder der das Repo klont kann direkt "pytest" ausführen
#           ohne irgendwelche Pfade manuell konfigurieren zu müssen.
