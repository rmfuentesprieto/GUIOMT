from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from omt.gui.empty import Empty


class BeamScanner(Empty):

    def __init__(self, **kwargs):
        super(BeamScanner, self).__init__(kwargs=kwargs)

        ## this is the controll to move the beam scanner
        self.set_center = Button(text='Set Center', size_hint=(1,None), size=(1,30))
        self.move_up = Button(text='/\\', size_hint=(0.33,None), size=(1,30))
        move_up_padding_l = Label( size_hint=(0.33,None), size=(1,30))
        move_up_padding_r = Label( size_hint=(0.33,None), size=(1,30))

        self.move_left = Button(text='<', size_hint=(0.33,None), size=(1,30))
        self.move_rigth = Button(text='>', size_hint=(0.33,None), size=(1,30))
        self.step_size = TextInput(size_hint=(0.33,None), size=(1,30))

        self.move_down = Button(text='\\/', size_hint=(0.33,None), size=(1,30))
        move_down_padding_l = Label( size_hint=(0.33,None), size=(1,30))
        move_down_padding_r = Label( size_hint=(0.33,None), size=(1,30))

        move_top = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1, 30))
        move_top.add_widget(move_up_padding_l)
        move_top.add_widget(self.move_up)
        move_top.add_widget(move_up_padding_r)

        move_middle = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1, 30))
        move_middle.add_widget(self.move_left)
        move_middle.add_widget(self.step_size)
        move_middle.add_widget(self.move_rigth)

        move_bottom = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1, 30))
        move_bottom.add_widget(move_down_padding_l)
        move_bottom.add_widget(self.move_down)
        move_bottom.add_widget(move_down_padding_r)

        move_xy_layes = BoxLayout(orientation='vertical', size_hint=(1,None), size=(1, 120))

        move_xy_layes.add_widget(self.set_center)
        move_xy_layes.add_widget(move_top)
        move_xy_layes.add_widget(move_middle)
        move_xy_layes.add_widget(move_bottom)

        ## this is the controll to rotate the beam scanner

        self.set_origin = Button(text='Set Zero', size_hint=(0.33,None), size=(1,30))
        self.do_rotation = Button(text='Rotate to:', size_hint=(0.33,None), size=(1,30))
        self.destination_angle = TextInput(size_hint=(0.33,None), size=(1,30))

        rotation_layou = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1, 30))
        rotation_layou.add_widget(self.set_origin)
        rotation_layou.add_widget(self.do_rotation)
        rotation_layou.add_widget(self.destination_angle)

        ##  check the plane movility

        size_of_plane_label = Label(text='Plane size [mm]', size=(1,30))
        self.size_of_plane_val = TextInput( size=(1,30))

        plane_size = BoxLayout(orientaion='horizontal',size_hint=(1,None),size=(1,30))
        plane_size.add_widget(size_of_plane_label)
        plane_size.add_widget(self.size_of_plane_val)

        ## configuration

        # frecuency

        frec_label = Label(text='Set Lambda [mm]: ', size_hint=(1,None), size=(1,30))
        self.frec_value = TextInput( size_hint=(1,None), size=(1,30))

        frec_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1, 30))
        frec_layout.add_widget(frec_label)
        frec_layout.add_widget(self.frec_value)

        # display step

        step_label = Label(text='Step size [mm]: ')
        self.step_val = Label(text='0.0')

        display_step = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1, 30))
        display_step.add_widget(step_label)
        display_step.add_widget(self.step_val)


        paddind = BoxLayout(size_hint=(1,1), size=(1,1000))

        self.big_one = BoxLayout(orientation='vertical')

        self.big_one.add_widget(move_xy_layes)
        self.big_one.add_widget(rotation_layou)
        self.big_one.add_widget(plane_size)
        self.big_one.add_widget(frec_layout)
        self.big_one.add_widget(display_step)
        self.big_one.add_widget(paddind)

        self.add_widget(self.big_one)

