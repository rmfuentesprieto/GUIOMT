
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class GUIStart(App):
    def build(self, **kwargs):
        layout = GridLayout(cols=1, spacing=0, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        root = ScrollView(size_hint=(None, None), size=(400, 400))
        root.add_widget(layout)

        for i in range(30):
            btn = Button(text=str(i), size_hint=(0.5,None), height=20)
            btn1 = Button(text=str(i), size_hint=(0.5,None), height=20)
            lol = BoxLayout(orientation='horizontal',size_hint=(1, None), size=(1,20))
            lol.add_widget(btn)
            lol.add_widget(btn1)
            layout.add_widget(lol)

        return root

GUIStart().run()