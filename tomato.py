from kivy.app import App
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from gi.repository import Notify

def on_enter(instance, value):
    print ('User pressed enter in', instance)

def on_text(instance, value):
    print ('User enter text:', value, 'in', instance)    

    
class TomatoPlayer(Widget):
    h = NumericProperty(0)
    m = NumericProperty(25)
    s = NumericProperty(0)
    time_strprop = StringProperty()
    goal_input = ObjectProperty(None)
    goal = StringProperty()
    start = BooleanProperty()
    finished_tomato = NumericProperty(0)
    record = open('tomato_record.txt','a')

    def get_time_str(self):
        h_str = "00"
        m_str = str(self.m) if self.m >= 10 else "0"+str(self.m)
        s_str = str(self.s) if self.s >= 10 else "0"+str(self.s)
        return ":".join([h_str, m_str, s_str])

    def get_goal(self, textinput):
        self.goal = textinput.text
        textinput.text = ""
        self.remove_widget(self.goal_input)
        self.start = True
        
    def init_task(self):
        self.time_strprop = "00:25:00"
        self.start = False
        self.goal_input.bind(on_text_validate=self.get_goal)

    def update(self, t):
        if self.start:
            self.s -= 1
            if self.s == -1:
                self.m -= 1
                if self.m != -1:
                    self.s = 59
                else: # restart clock
                    self.finished_tomato += 1
                    self.finish_loop_handler()
            self.time_strprop = self.get_time_str()
            
    def finish_loop_handler(self):
        self.start = False
        self.record.write("Finish today's {c} tomato: {goal}".format(
            c=self.finished_tomato,
            goal=self.goal
        ))
        # TODO: Currently the it will not show the tomato icon.
        notification = Notify.Notification.new("Times up!\n You", body=self.goal, icon="tomato.png")
        notification.show()
        self.goal = ""
        self.add_widget(self.goal_input)
        img = Image(source='tomato.png')
        img.center_y = self.height * 1 / 6.0
        img.center_x = self.width * self.finished_tomato / 10.0 
        self.add_widget(img)
        self.h = 0
        self.m = 25
        self.s = 0
        self.time_strprop = "00:25:00"
        

class TomatoApp(App):
    def build(self):
        Notify.init('tomato')
        tomato = TomatoPlayer()
        tomato.init_task()
        Clock.schedule_interval(tomato.update, 1.0)
        return tomato

if __name__ == "__main__":
    TomatoApp().run()