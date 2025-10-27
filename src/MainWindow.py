import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class MainWindow(Gtk.ApplicationWindow):
	def __init__(self, app):
		super().__init__(application=app)
		print("window oluştu")
		self.setup_window()
		self.setup_headerbar()
		self.setup_ui()


	def setup_window(self):
		self.set_default_size(600, 400)
		self.set_title("Hakki Text Editor")

	def setup_headerbar(self):
		btn_open = Gtk.Button(
			label="Open",
			icon_name="document-open-symbolic",
			tooltip_text="Create a new empty document.",
		)
		btn_new = Gtk.Button(
			label="New", icon_name="document-new-symbolic", tooltip_text="Open a file."
		)
		btn_save = Gtk.Button(
			label="Save",
			icon_name="document-save-symbolic",
			tooltip_text="Save the current file.",
		)
		btn_save_as = Gtk.Button(
			label="Save As",
			icon_name="document-save-as-symbolic",
			tooltip_text="Save the current file as a different file.",
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

	def on_btn_clicked(self, btn):
		print("clicked a btn")
