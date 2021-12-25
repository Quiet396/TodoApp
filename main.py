# Kivy
from kivy.lang import Builder
from kivy.properties import StringProperty

# KivyMD
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import ThreeLineAvatarIconListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

# Standard
import datetime


class Tab(MDBoxLayout, MDTabsBase):
    text = StringProperty()


class Task(ThreeLineAvatarIconListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()


class DoneTask(ThreeLineAvatarIconListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
 

# not use
class Content(MDBoxLayout):
    taskname = StringProperty()
    description = StringProperty()
    
    def get_taskname(self):
        return taskname

    def get_description(self):
        return description


class Main(MDApp):
    dialog = None
    task_dialog = None

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

    def build(self):
        self.root.ids.taskname.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
    
    def set_error_message(self, instance_textfield):
        self.root.ids.taskname.error = True

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        pass
        
    def send(self):
        taskname = self.root.ids.taskname.text
        description = self.root.ids.description.text
        if(len(taskname) == 0):
            Snackbar(text="Please input taskname!").open()
            return
        now = datetime.datetime.now()
        nowtime = now.strftime("%Y/%m/%d %H:%M:%S")
        self.root.ids.todo.add_widget(
                                        Task(
                                                text=taskname, 
                                                secondary_text=description, 
                                                tertiary_text=nowtime
                                            )
                                        )
        Snackbar(text="Task Created!").open()
        self.root.ids.taskname.text = ""
        self.root.ids.description.text = ""
        
    def remove_widget(self, instance):
        if("todo" == instance.parent.text):
            self.root.ids.todo.remove_widget(instance)
        elif("doing" == instance.parent.text):
            self.root.ids.doing.remove_widget(instance)
        else:
            self.root.ids.done.remove_widget(instance)
            Snackbar(text="Task Removed!").open()
        
    def change_task_status(self, instance):
        if not self.task_dialog:
            self.task_dialog = MDDialog(
                title="Move to Status?",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="YES",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.move_to_next( x,
                                                                instance,
                                                                instance.text, 
                                                                instance.secondary_text,
                                                                instance.tertiary_text
                                                              )
                    )
                ],
            )
        self.task_dialog.open()
    
    def move_to_next(self, button_instance, task_instance, text, secondary_text, tertiary_text):
        if("todo" == task_instance.parent.text):
            self.root.ids.doing.add_widget(
                                            Task(
                                                    text=text, 
                                                    secondary_text=secondary_text, 
                                                    tertiary_text=tertiary_text
                                                )
                                          )
        else:
            self.root.ids.done.add_widget(
                                             DoneTask(
                                                        text=text, 
                                                        secondary_text=secondary_text, 
                                                        tertiary_text=tertiary_text
                                                     )
                                         )
        self.remove_widget(task_instance)
        self.task_dialog.dismiss()
        self.task_dialog = None
        Snackbar(text="Task Moved!").open()

Main().run()
