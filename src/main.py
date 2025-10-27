#!/usr/bin/python3
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from MainWindow import MainWindow
def on_activate(app):
    win = MainWindow(app)
    win.present()

app = Gtk.Application(application_id='me.ihakkiergin.notepad')
app.connect('activate', on_activate)

app.run(None)
