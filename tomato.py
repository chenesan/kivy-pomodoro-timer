import datetime
import json

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.properties import NumericProperty, StringProperty
from kivy.properties import ListProperty
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
    tomato_count = NumericProperty(0)
    record = open('tomato_record.txt','a')

    def __init__(self, *args, **kwargs):
        start_time = datetime.datetime.now()
        self._state = {
            'date': start_time.date().strftime("%Y-%b-%d"),
            'finished_goals': []
        }
        try:
            last_state = json.load(open('pomodoro_state.json','r'))
            if self._state['date'] == last_state['date']:
                self._state = last_state
        except IOError:
            pass
        self.tomato_count = len(self._state["finished_goals"])
        super(TomatoPlayer, self).__init__(*args, **kwargs)
        
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
        for i in range(self.tomato_count):
            #Don't know why the height and width is 100*100...
            img = Image(source='tomato.png')
            img.center_x = 800 * (i + 1) / 10.0
            img.center_y = 600 * 1 / 6.0
            self.add_widget(img)
            

    def update(self, t):
        if self.start:
            self.s -= 1
            if self.s == -1:
                self.m -= 1
                if self.m != -1:
                    self.s = 59
                else: # restart clock
                    self.finish_loop_handler()
            self.time_strprop = self.get_time_str()
            
    def finish_loop_handler(self):
        self.start = False
        now_str = datetime.datetime.now().strftime("%Y-%b-%d, %H:%M")
        self._state['finished_goals'].append(tuple([now_str, self.goal]))
        self.tomato_count = len(self._state["finished_goals"])
        self.record.write("{now}: {goal}\n".format(
            now=now_str,
            goal=self.goal
        ))
        # TODO: Currently the it will not show the tomato icon.
        notification = Notify.Notification.new("Times up!\n", body=self.goal, icon="tomato.png")
        notification.show()
        self.goal = ""
        self.add_widget(self.goal_input)
        img = Image(source='tomato.png')
        img.center_y = self.height * 1 / 6.0
        img.center_x = self.width * len(self._state['finished_goals']) / 10.0
        print img.center_x, img.center_y
        self.add_widget(img)
        self.h = 0
        self.m = 25
        self.s = 0
        self.time_strprop = "00:25:00"

    def save_state(self, app):
        json.dump(self._state, open('pomodoro_state.json','w'))
        
class TomatoApp(App):
    def build(self):
        Notify.init('tomato')
        tomato = TomatoPlayer()
        tomato.init_task()
        Clock.schedule_interval(tomato.update, 1.0/1000)
        self.bind(on_stop=tomato.save_state)
        return tomato

if __name__ == "__main__":
    TomatoApp().run()