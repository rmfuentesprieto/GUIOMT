from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.screenmanager import Screen


class AbstractSource(Screen):

     def __init__(self,**kwargs):

         super(AbstractSource, self).__init__(kwargs=kwargs)

         line1 = BoxLayout(orientation='horizontal')
         line2 = BoxLayout(orientation='horizontal')
         line3 = BoxLayout(orientation='horizontal')

         button_increase_frec = Button(text='->')
         button_reduce_frec = Button(text='<-')
         label_current_frec = Label(text=str(self.getVal()))

         line1.add_widget(button_reduce_frec)
         line1.add_widget(label_current_frec)
         line1.add_widget(button_increase_frec)

         self.add_widget(line1)


     def getVal(self):
         return 8
