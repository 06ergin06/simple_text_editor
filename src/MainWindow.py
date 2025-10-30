import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

import FileOperations

import locale
from locale import gettext as _

APPNAME = "hakkitor"
TRANSLATIONS_PATH = "/usr/share/locale"
locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
locale.textdomain(APPNAME)

class MainWindow(Gtk.ApplicationWindow):
	def __init__(self, app):
		super().__init__(application=app)
		self.setup_variables()
		self.setup_actions()
		self.setup_window()
		self.setup_headerbar()
		self.setup_ui()

	# Setups
	def setup_variables(self):
		self.current_working_file = None

	def setup_actions(self):
		new_action = Gio.SimpleAction(name="new")
		new_action.connect("activate", self.on_action_win_new_activated)
		self.add_action(new_action)

		open_action = Gio.SimpleAction(name="open")
		open_action.connect("activate", self.on_action_win_open_activated)
		self.add_action(open_action)

		save_action = Gio.SimpleAction(name="save")
		save_action.connect("activate", self.on_action_win_save_activated)
		self.add_action(save_action)

		save_as_action = Gio.SimpleAction(name="save-as")
		save_as_action.connect("activate", self.on_action_win_save_as_activated)
		self.add_action(save_as_action)

	def setup_window(self):
		self.set_default_size(600, 400)
		self.set_title("Hakki Text Editor")

	def setup_headerbar(self):
		btn_open = Gtk.Button(
			icon_name="document-open-symbolic",
			action_name="win.open",
			tooltip_text=_("Open a file."),
		)
		btn_new = Gtk.Button(
			icon_name="document-new-symbolic",
			action_name="win.new",
			tooltip_text=_("Create a new empty document."),
		)
		btn_save = Gtk.Button(
			icon_name="document-save-symbolic",
			action_name="win.save",
			tooltip_text=_("Save the current file."),
		)
		btn_save_as = Gtk.Button(
			icon_name="document-save-as-symbolic",
			action_name="win.save-as",
			tooltip_text=_("Save the current file as a different file."),
		)

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		box.append(btn_open)
		box.append(btn_new)
		box.append(btn_save)
		box.append(btn_save_as)

		headerbar = Gtk.HeaderBar()
		headerbar.pack_start(box)
		self.set_titlebar(headerbar)

	def setup_ui(self):
		self.text_view = Gtk.TextView(
			monospace=True,
			left_margin=5,
			right_margin=5,
			top_margin=5,
			bottom_margin=5,
		)
		scrolled_window = Gtk.ScrolledWindow(child=self.text_view)
		self.set_child(scrolled_window)

	# Functions
	def get_textview_text(self):
		buffer = self.text_view.get_buffer()

		start = buffer.get_start_iter()
		end = buffer.get_end_iter()
		return buffer.get_text(start, end, False)

	def set_textview_text(self, text):
		buffer = self.text_view.get_buffer()
		buffer.set_text(text)
		start = buffer.get_start_iter()
		buffer.place_cursor(start)

	# Callbacks
	def on_action_win_new_activated(self, action, params):
		self.set_textview_text("")
		self.set_title("Hakki Text Editor")
		self.current_working_file = None

	def on_action_win_open_activated(self, action, params):
		self._open_file_chooser = Gtk.FileChooserNative(
			title=_("Open File"),
			transient_for=self,
			action=Gtk.FileChooserAction.OPEN,
			accept_label="_Open",
			cancel_label="_Cancel",
		)
		self._open_file_chooser.connect("response", self.on_open_dialog_response)
		self._open_file_chooser.show()

	def on_open_dialog_response(self, dialog, response):
		if response == Gtk.ResponseType.ACCEPT:
			FileOperations.read_file(dialog.get_file(), self.on_file_read)
		self._open_file_chooser = None

	def on_file_read(self, file, content, err):
		if err:
			print(f"Error : {err}")
			return
		self.set_textview_text(content)
		filename = FileOperations.get_name(file)
		self.set_title(filename)
		self.current_working_file = file

	def on_action_win_save_as_activated(self, action, params):
		self._save_file_chooser = Gtk.FileChooserNative(
			title=_("Save File"),
			transient_for=self,
			action=Gtk.FileChooserAction.SAVE,
			accept_label="_Save",
			cancel_label="_Cancel",
		)
		self._save_file_chooser.connect("response", self.on_save_dialog_response)
		self._save_file_chooser.show()

	def on_save_dialog_response(self, dialog, response):
		if response == Gtk.ResponseType.ACCEPT:
			text = self.get_textview_text()

			FileOperations.save_file(dialog.get_file(), text, self.on_file_saved)
		self._save_file_chooser = None

	def on_action_win_save_activated(self, action, params):
		if self.current_working_file:
			text = self.get_textview_text()

			FileOperations.save_file(
				self.current_working_file, text, self.on_file_saved
			)
		else:
			self.activate_action("win.save-as")

	def on_file_saved(self, file, success, new_etag):
		if success:
			filename = FileOperations.get_name(file)
			self.set_title(filename)
			self.current_working_file = file
