#!/usr/bin/python3
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from MainWindow import MainWindow

win = None
def on_activate(app):
	global win
	if not win:
		win = MainWindow(app)
	win.present()

app = Gtk.Application(application_id='me.ihakkiergin.notepad')
app.connect('activate', on_activate)

app.set_accels_for_action('win.new', ['<Ctrl>t'])
app.set_accels_for_action('win.open', ['<Ctrl>o'])
app.set_accels_for_action('win.save', ['<Ctrl>s'])
app.set_accels_for_action('win.save-as', ['<Ctrl><Shift>s'])

app.run(None)
