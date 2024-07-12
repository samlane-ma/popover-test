#! /usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Libxfce4windowing', '0.0')
from gi.repository import Libxfce4windowing
if Libxfce4windowing.windowing_get() == Libxfce4windowing.Windowing.WAYLAND:
    gi.require_version('Budgie', '2.0')
else:
    gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk

class TestApplet(GObject.GObject, Budgie.Plugin):

    __gtype_name__ = "BudgieTestApplet"

    def __init__(self):
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        return TestAppletApplet(uuid)

class TestAppletApplet(Budgie.Applet):

    def __init__(self, uuid):
        Budgie.Applet.__init__(self)
        self.uuid = uuid
        self.icon = Gtk.Image.new_from_icon_name("mail-unread-symbolic", 32)
        self.add(self.icon)
        self.popover = Budgie.Popover.new(self)
        self.popover_label = Gtk.Label(label="Popover")
        self.popover.add(self.popover_label)
        self.popover.get_child().show_all()
        self.show_all()
        self.connect("button-press-event", self.on_press)

    def do_supports_settings(self):
        """Return True if support setting through Budgie Setting,
        False otherwise.
        """
        return False

    def on_press(self, box, arg):
        self.manager.show_popover(self)

    def do_update_popovers(self, manager):
        self.manager = manager
        self.manager.register_popover(self, self.popover)
