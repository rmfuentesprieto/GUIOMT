
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class ScrollViewApp(App):
    def build(self):

        grid = GridLayout(rows=2, size_hint=(None,None))
        grid.bind(minimum_width=grid.setter('width'))

        for i in range(60):
            grid.add_widget(Button(text='#00' + str(i), size=(100,100), size_hint=(None,None)))

        scroll = ScrollView( size_hint=(1,1), do_scroll_x=True, do_scroll_y=False )
        scroll.add_widget(grid)

        return scroll


if __name__ == '__main__':
    ScrollViewApp().run()