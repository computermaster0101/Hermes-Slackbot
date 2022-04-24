import dearpygui.dearpygui as dpg

from dearpygui.demo import show_demo

# application using..
# https://pypi.org/project/dearpygui/
# and
# https://medium.datadriveninvestor.com/create-quick-and-powerful-guis-using-dear-pygui-in-python-713cc138bf5a

dpg.create_context()

dpg.create_viewport()

dpg.setup_dearpygui()

show_demo()

dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context()
