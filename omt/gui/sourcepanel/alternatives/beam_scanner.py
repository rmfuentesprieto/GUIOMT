import socket
import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from math import sqrt

from omt.controller.source.beam_scanner.move_xy import MoveXY
from omt.controller.source.beam_scanner.rotate import Rotate
from omt.controller.source.beam_scanner_controller import BeamScannerController, BeamScannerControllerTone
from omt.gui.sourcepanel.alternatives.abstractsource import AbstractSource


class BeamScanner(AbstractSource):
    def __init__(self, **kwargs):
        super(BeamScanner, self).__init__(kwargs=kwargs)

        # activate the beam scanner

        self.active_state = False
        self.sweep_state = False
        sweep_label = Label(text='Do Sweep')
        self.sweep_switch = Switch(active=False)
        self.sweep_switch.bind(active=self.sweepe_or_not)



        sweep_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), size=(1,40))
        sweep_layout.add_widget(sweep_label)
        sweep_layout.add_widget(self.sweep_switch)

        # this is the controll to move the beam scanner
        self.set_center = Button(text='Set Center', size_hint=(1, None), size=(1, 30))
        self.set_center.bind(on_press=self.set_zero_xy)
        self.move_up = Button(text='/\\', size_hint=(0.33, None), size=(1, 30))
        self.move_up.bind(on_press=self.move_up_beam)
        move_up_padding_l = Label(size_hint=(0.33, None), size=(1, 30))
        move_up_padding_r = Label(size_hint=(0.33, None), size=(1, 30))

        self.move_left = Button(text='<', size_hint=(0.33, None), size=(1, 30))
        self.move_left.bind(on_press=self.move_left_beam)
        self.move_rigth = Button(text='>', size_hint=(0.33, None), size=(1, 30))
        self.move_rigth.bind(on_press=self.move_rigth_beam)
        self.step_size = TextInput(size_hint=(0.33, None), size=(1, 30), multiline=False)
        self.step_size.text = '0.0'

        self.move_down = Button(text='\\/', size_hint=(0.33, None), size=(1, 30))
        self.move_down.bind(on_press=self.move_down_beam)
        move_down_padding_l = Label(size_hint=(0.33, None), size=(1, 30))
        move_down_padding_r = Label(size_hint=(0.33, None), size=(1, 30))

        move_top = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        move_top.add_widget(move_up_padding_l)
        move_top.add_widget(self.move_up)
        move_top.add_widget(move_up_padding_r)

        move_middle = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        move_middle.add_widget(self.move_left)
        move_middle.add_widget(self.step_size)
        move_middle.add_widget(self.move_rigth)

        move_bottom = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        move_bottom.add_widget(move_down_padding_l)
        move_bottom.add_widget(self.move_down)
        move_bottom.add_widget(move_down_padding_r)

        move_xy_layes = BoxLayout(orientation='vertical', size_hint=(1, None), size=(1, 120))

        move_xy_layes.add_widget(self.set_center)
        move_xy_layes.add_widget(move_top)
        move_xy_layes.add_widget(move_middle)
        move_xy_layes.add_widget(move_bottom)

        # this is the controll to rotate the beam scanner

        self.set_origin = Button(text='Set Zero', size_hint=(0.33, None), size=(1, 30))
        self.set_origin.bind(on_press=self.set_zero_ang)
        self.do_rotation = Button(text='Rotate to:', size_hint=(0.33, None), size=(1, 30))
        self.do_rotation.bind(on_press=self.rotate)
        self.destination_angle = TextInput(size_hint=(0.33, None), size=(1, 30), multiline=False)
        self.destination_angle.text = '0.0'

        rotation_layou = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        rotation_layou.add_widget(self.set_origin)
        rotation_layou.add_widget(self.do_rotation)
        rotation_layou.add_widget(self.destination_angle)

        # rotation speed

        speed_rotation = Label(text='Angular Speed', size_hint=(1, None), size=(1, 30))
        self.speed_rotation_value = TextInput(size_hint=(1, None), size=(1, 30))
        self.speed_rotation_value.text = '10.0'

        rotation_speed = BoxLayout(orientaion='horizontal', size_hint=(1, None), size=(1, 30))
        rotation_speed.add_widget(speed_rotation)
        rotation_speed.add_widget(self.speed_rotation_value)

        #  check the plane movility

        size_of_plane_label = Label(text='Plane size [mm]', size=(1, 30))
        self.size_of_plane_val = TextInput(size=(1, 30), multiline=False)
        self.size_of_plane_val.text = '0.0'
        self.size_of_plane_val.bind(focus=self.set_number_of_points)

        plane_size = BoxLayout(orientaion='horizontal', size_hint=(1, None), size=(1, 30))
        plane_size.add_widget(size_of_plane_label)
        plane_size.add_widget(self.size_of_plane_val)

        # configuration

        # frecuency

        frec_label = Label(text='Set Lambda [mm]: ', size_hint=(1, None), size=(1, 30))
        self.frec_value = TextInput(size_hint=(1, None), size=(1, 30), multiline=False)
        self.frec_value.text = '0.0'
        self.frec_value.bind(focus=self.set_number_of_points)

        frec_step = Label(text='Step factor: ', size_hint=(1, None), size=(1, 30))
        self.frec_step_value = TextInput(size_hint=(1, None), size=(1, 30), multiline=False)
        self.frec_step_value.text = '0.45'
        self.frec_step_value.bind(focus=self.set_number_of_points)

        frec_layout_val = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        frec_layout_val.add_widget(frec_label)
        frec_layout_val.add_widget(self.frec_value)

        frec_layout_step = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        frec_layout_step.add_widget(frec_step)
        frec_layout_step.add_widget(self.frec_step_value)

        frec_layout = BoxLayout(orientation='vertical', size_hint=(1, None), size=(1, 60))
        frec_layout.add_widget(frec_layout_val)
        frec_layout.add_widget(frec_layout_step)

        # display step

        step_label = Label(text='Number of Points: ')
        self.step_val = Label(text='0')

        display_step = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        display_step.add_widget(step_label)
        display_step.add_widget(self.step_val)

        # fast sweep enable

        self.fast_sweepp = ToggleButton(text='fast sweep', size_hint=(1,None), size=(1,30))

        # goto configuration

        goto_label = Label(text='Go to Position')
        self.goto_switch = Switch(active=False)
        self.goto_switch.bind(active=self.goto_or_not)

        x_dest = Label(text = 'x position [mm]')
        y_dest = Label(text = 'y position [mm]')
        theta_dest = Label(text = 'angle [Degree]')

        self.x_dest_val = TextInput(size_hint=(0.33, None), size=(1, 30), multiline=False)
        self.x_dest_val.text = '0.0'
        self.y_dest_val = TextInput(size_hint=(0.33, None), size=(1, 30), multiline=False)
        self.y_dest_val.text = '0.0'
        self.theta_dest_val = TextInput(size_hint=(0.33, None), size=(1, 30), multiline=False)
        self.theta_dest_val.text = '0.0'


        goto_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        goto_layout.add_widget(goto_label)
        goto_layout.add_widget(self.goto_switch)

        goto_layout_x = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        goto_layout_x.add_widget(x_dest)
        goto_layout_x.add_widget(self.x_dest_val)

        goto_layout_y = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        goto_layout_y.add_widget(y_dest)
        goto_layout_y.add_widget(self.y_dest_val)

        goto_layout_theta = BoxLayout(orientation='horizontal', size_hint=(1, None), size=(1, 30))
        goto_layout_theta.add_widget(theta_dest)
        goto_layout_theta.add_widget(self.theta_dest_val)

        goto_switch = BoxLayout(orientation='vertical', size_hint=(1, None), size=(1, 120))
        goto_switch.add_widget(goto_layout)
        goto_switch.add_widget(goto_layout_x)
        goto_switch.add_widget(goto_layout_y)
        goto_switch.add_widget(goto_layout_theta)



        # big container configuration

        paddind = BoxLayout(size_hint=(1, 1), size=(1, 1000))

        self.big_one = BoxLayout(orientation='vertical')

        self.big_one.add_widget(sweep_layout)
        self.big_one.add_widget(move_xy_layes)
        self.big_one.add_widget(rotation_layou)
        self.big_one.add_widget(rotation_speed)
        self.big_one.add_widget(plane_size)
        self.big_one.add_widget(frec_layout)
        self.big_one.add_widget(display_step)
        self.big_one.add_widget(self.fast_sweepp)
        self.big_one.add_widget(goto_switch)
        self.big_one.add_widget(paddind)

        self.add_widget(self.big_one)



        # attributes that lets you connect to beam scanner

        self.ip_beam = '192.168.1.62'
        self.ip_port = 9988
        self.move_xy = MoveXY(self.ip_beam, self.ip_port)
        self.move_ang = Rotate(self.ip_beam, self.ip_port)

        # disconnect thread configuration

        self.monitor = threading.Event()
        self.disconnect = True
        self.launch_thread = False

    def sweepe_or_not(self, instance, value):
        if value:
            self.sweep_state = value
            self.goto_switch.active = False
        self.active_state = value

    def goto_or_not(self, instance, value):
        if value:
            self.sweep_state = False
            self.sweep_switch.active = False
        self.active_state = value

    def is_active(self):
        return self.active_state

    def do_sweep(self):
        return self.sweep_state

    # connecto to configure and move around
    def start_connection(self):
        self.disconnect = False
        if not self.launch_thread:
            try:
                self.move_xy.start_connection()
                self.move_ang.start_connection()
                threading.Thread(target=self.close_connection_timer).start()
                self.launch_thread = True
                try:
                    self.move_ang.set_hspd(float(self.speed_rotation_value.text))
                except:
                    pass
                return True
            except socket.error as e:
                Popup(title='Error BeamScanner', content=Label(text=e.message),
                      size_hint=(None, None), size=(200, 200)).open()
                return False
        return True

    def stop_connection(self):
        self.move_xy.close_connection()
        self.move_ang.close_connection()

    # movement of the beam scanner


    def move_left_beam(self, instance):
        if self.start_connection():
            try:
                if not self.move_xy.move_relative(float(self.step_size.text), 0):
                    self.stop_connection()
                    self.disconnect = True
            except Exception as e:
                self.stop_connection()

    def move_rigth_beam(self, instance):
        if self.start_connection():
            try:
                if not self.move_xy.move_relative(-float(self.step_size.text), 0):
                    self.stop_connection()
                    self.disconnect = True
            except Exception:
                self.stop_connection()

    def move_up_beam(self, instance):
        if self.start_connection():
            try:
                if not self.move_xy.move_relative(0, -float(self.step_size.text)):
                    self.stop_connection()
                    self.disconnect = True
            except Exception as e:
                self.stop_connection()

    def move_down_beam(self, instance):
        if self.start_connection():
            try:
                if not self.move_xy.move_relative(0, float(self.step_size.text)):
                    self.stop_connection()
                    self.disconnect = True
            except Exception as e:
                self.stop_connection()

    def rotate(self, instance):
        if self.start_connection():
            try:
                if not self.move_ang.move_absolute(float(self.destination_angle.text)):
                    self.stop_connection()
                    self.disconnect = True
            except Exception:
                self.stop_connection()

    def set_zero_xy(self, instance):
        if self.start_connection():
            try:
                if not self.move_xy.set_origin():
                    self.stop_connection()
                    self.disconnect = True
            except Exception:
                self.stop_connection()

    def set_zero_ang(self, instance):
        if self.start_connection():
            try:
                if not self.move_ang.set_origin():
                    self.stop_connection()
                    self.disconnect = True
            except Exception:
                self.stop_connection()

    def set_number_of_points(self, instance, value):
        try:
            lambda_ = float(self.frec_value.text)
            factor = float(self.frec_step_value.text)

            if lambda_*factor > 0:
                size = float(self.size_of_plane_val.text)
                points = int(0.5 + size/(lambda_*factor)) + 1
                self.step_val.text = str(points*points)
        except:
            pass

    # thead de apagado
    def close_connection_timer(self):
        print 'close function initiated'
        while 1:
            if self.disconnect:
                print 'closing function'
                self.stop_connection()
                break

            self.disconnect = True

            self.monitor.wait(15)

        self.launch_thread = False

    def get_source_config(self):
        return_dic = {}

        try :
            if self.sweep_state:
                return_dic['size'] = float(self.size_of_plane_val.text)
                return_dic['total_points'] = int(self.step_val.text)
                return_dic['angle_to_measure'] = float(self.destination_angle.text)

                return_dic['instance'] = BeamScannerController
                return_dic['angle_speed'] = float(self.speed_rotation_value.text)
                return_dic['name'] = self.get_my_name()
                return_dic['fast'] = self.fast_sweepp.state != 'normal'

                if return_dic['fast']:
                    return_dic['frec_number_point'] = (int(self.step_val.text))
                else:
                    return_dic['frec_number_point'] = sqrt(int(self.step_val.text))*2
            else:
                return_dic['angle_speed'] = float(self.speed_rotation_value.text)
                return_dic['name'] = self.get_my_name()
                return_dic['instance'] = BeamScannerControllerTone
                return_dic['x'] = float(self.x_dest_val.text)
                return_dic['y'] = float(self.y_dest_val.text)
                return_dic['theta'] = float(self.theta_dest_val.text)
        except:
            raise Exception('Please Enter Numbers only')


        return return_dic

    def get_my_name(self):
        return 'BeamScanner'

    def save_config_dictionary(self):
        dic_return = {}

        dic_return['on_off'] = self.active_state
        dic_return['sweep'] = self.sweep_state
        dic_return['size'] = self.size_of_plane_val.text
        dic_return['total_points'] = self.step_val.text
        dic_return['angle_to_measure'] = self.destination_angle.text
        dic_return['angle_speed'] = self.speed_rotation_value.text
        dic_return['x'] = float(self.x_dest_val.text)
        dic_return['y'] = float(self.y_dest_val.text)
        dic_return['theta'] = float(self.theta_dest_val.text)
        dic_return['lambda'] = self.frec_value.text
        dic_return['step_factor'] = self.step_size.text

        return {self.get_my_name():dic_return}

    def set_configuration(self, config_dictionary):
        if self.get_my_name() in config_dictionary:
            config_dictionary_ = config_dictionary[self.get_my_name()]
            self.active_state = config_dictionary_['on_off']
            self.sweep_state = config_dictionary_['sweep']
            self.size_of_plane_val.text = config_dictionary_['size']
            self.step_val.text = config_dictionary_['total_points']
            self.destination_angle.text = config_dictionary_['angle_to_measure']
            self.speed_rotation_value.text = config_dictionary_['angle_speed']
            self.x_dest_val.text = str(config_dictionary_['x'])
            self.y_dest_val.text = str(config_dictionary_['y'])
            self.theta_dest_val.text = str(config_dictionary_['theta'])
            self.frec_value.text = config_dictionary_['lambda']
            self.step_size.text = config_dictionary_['step_factor']

            if self.active_state:
                if self.sweep_state:
                    self.sweep_switch.active = True
                else:
                    self.goto_switch.active = True
            else:
                self.sweep_switch.active = False
                self.goto_switch.active = False
        else:
            self.sweep_switch.active = False
            self.goto_switch.active = False



