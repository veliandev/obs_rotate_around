import obspython as S
import threading
from time import sleep

alignment_modes = {
	"center": 0,
	"left": 1 << 0,
	"right": 1 << 1,
	"top": 1 << 2,
	"bottom": 1 << 3
}

class Example:
	def __init__(self, source_name=None):
		self.source_name = source_name
		self.rotation = 0
		self.rotation_speed = 0
		self.rotation_mode = None
		self.current_thread = None
		self.thread_running = False

	def rotate_source_around_center(self):
		current_scene = S.obs_frontend_get_current_scene()
		source = S.obs_get_source_by_name(self.source_name)
		scene = S.obs_scene_from_source(current_scene)
		scene_item = S.obs_scene_find_source(scene, self.source_name)

		if scene_item:
			S.obs_sceneitem_set_alignment(scene_item, self.rotation_mode)
			while self.thread_running:
				if not scene_item:
					self.thread_running = False
					break
				old_rot = S.obs_sceneitem_get_rot(
					scene_item
				)
				self.rotation = old_rot + 1 * (self.rotation_speed * 0.005)
				S.obs_sceneitem_set_rot(scene_item, self.rotation)
				sleep(0.01)

		S.obs_scene_release(scene)
		S.obs_source_release(source)


eg = Example()  # class created ,obs part starts

def move_pressed(props, prop):
    
	eg.thread_running = not eg.thread_running
	print(eg.thread_running)
 
	if eg.thread_running == True:
		eg.current_thread = threading.Thread(target=eg.rotate_source_around_center)    
		eg.current_thread.start()
	# eg.rotate_source_around_center()

def script_description():
	return "Rotate a selected source around it's centerpoint"

def script_update(settings):
    eg.source_name = S.obs_data_get_string(settings, "source")
    eg.rotation_speed = S.obs_data_get_double(settings, "rotation_speed")
    eg.rotation_mode = S.obs_data_get_int(settings, "rotation_modes")

def script_properties():  # ui
	props = S.obs_properties_create()
	p = S.obs_properties_add_list(
		props,
		"source",
		"Image Source",
		S.OBS_COMBO_TYPE_EDITABLE,
		S.OBS_COMBO_FORMAT_STRING,
	)
	sources = S.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = S.obs_source_get_unversioned_id(source)
			name = S.obs_source_get_name(source)
			S.obs_property_list_add_string(p, name, name)

		S.source_list_release(sources)
  
	q = S.obs_properties_add_list(
		props,
		"rotation_modes",
		"Rotate Around",
		S.OBS_COMBO_TYPE_LIST,
		S.OBS_COMBO_FORMAT_INT,
	)
	S.obs_property_list_add_int(q, "Top Left", alignment_modes["top"] + alignment_modes["left"])
	S.obs_property_list_add_int(q, "Top", alignment_modes["top"])
	S.obs_property_list_add_int(q, "Top Right", alignment_modes["top"] + alignment_modes["top"])
	S.obs_property_list_add_int(q, "Center Left", alignment_modes["center"] + alignment_modes["left"])
	S.obs_property_list_add_int(q, "Center", alignment_modes["center"])
	S.obs_property_list_add_int(q, "Center Right", alignment_modes["center"] + alignment_modes["right"])
	S.obs_property_list_add_int(q, "Bottom Left", alignment_modes["bottom"] + alignment_modes["left"])
	S.obs_property_list_add_int(q, "Bottom", alignment_modes["bottom"])
	S.obs_property_list_add_int(q, "Bottom Right", alignment_modes["bottom"] + alignment_modes["right"])

	S.obs_properties_add_button(
	    props, "button2", "Rotate this mf", move_pressed
	)
 
	S.obs_properties_add_float_slider(props,"rotation_speed", "Anti-Clockwise / Clockwise Speed",-500,500,0.01) # Change the -500 and 500 if you wanna increase your maximum speed
	return props
