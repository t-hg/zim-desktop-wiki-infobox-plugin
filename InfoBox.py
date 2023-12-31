import logging

logger = logging.getLogger('zim.plugins.InfoBox')

from zim.plugins import PluginClass, InsertedObjectTypeExtension
from zim.gui.insertedobjects import TextViewWidget
from zim.config import ConfigManager

from gi.repository import Gdk, Gtk, Pango

class InfoBoxPlugin(PluginClass):
    plugin_info = {
        'name': _('Info box'),
        'description': _('Info box'),
        'author': 'Tobias Hort-Giess'
    }


class InfoBoxObjectType(InsertedObjectTypeExtension):
	name = 'info'
	label = _('Info Box')
	object_attr = {}

	def model_from_data(self, notebook, page, attrib, data):
		return InfoBoxBuffer(attrib, data)

	def data_from_model(self, buffer):
		return buffer.get_attrib_and_data()

	def create_widget(self, buffer):
		return InfoBoxWidget(buffer)


class InfoBoxBuffer(Gtk.TextBuffer):
	def __init__(self, attrib, data):
		Gtk.TextBuffer.__init__(self)
		self.attrib = attrib
		if data.endswith('\n'):
			data = data[:-1]
		self.set_text(data)

	def get_attrib_and_data(self):
		start, end = self.get_bounds()
		text = start.get_text(end)
		text += "\n"
		return self.attrib, text


def get_style(key, default, _type):
	try:
		style = ConfigManager.get_config_dict('style.conf')
		value = style['Tag info'][key]
		if _type == 'string':
			return value
		elif _type == 'color':
			color_ok, color = Gdk.Color.parse(value)
			if color_ok:
				return color
			else:
				return default
		else:
			return default
	except KeyError:
		return default


class InfoBoxWidget(TextViewWidget):
	def _init_view(self):
		TextViewWidget._init_view(self)
		font = get_style('family', 'monospace', 'string')
		background = get_style('background', 'blue', 'color')
		self.view.modify_font(Pango.FontDescription(font))
		self.view.modify_bg(Gtk.StateType.NORMAL, background)

