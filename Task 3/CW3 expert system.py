# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:25:35 2024

@author: dan
"""

import loading_json
from experta.watchers import RULES, AGENDA
from datetime import datetime, timedelta
from experta import *
import numpy as np
import pandas as pd
from tkinter import *
import process_schedule_all

BG_GRAY = "gainsboro"
BG_COLOUR = "lavender"
TEXT_COLOUR = "black"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

train_schedules = loading_json.import_json()
#process_schedule_all.get_all_schedule_advice("LIVST",1500, train_schedules)



#%%

class ChatBot:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.initial_message()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.geometry("500x600")

    #head label

        head_label = Label(self.window, bg=BG_COLOUR,fg=TEXT_COLOUR,
                       text = "Welcome!", font=FONT, pady=10)
        head_label.pack(fill=X)
#divider
        line = Label(self.window, width=500, bg=BG_GRAY)
        line.pack(fill=X)
#text widget
        self.text_widget = Text(self.window,width=20, height=2, bg=BG_COLOUR, fg=TEXT_COLOUR,
                                font=FONT,padx=5,pady=5)
        self.text_widget.pack(fill=BOTH, expand=True)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
#scrollbar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.see(CURRENT)
        scrollbar.configure(command=self.text_widget.yview)
        print("scrollbar")

#Bottom label

        bottom_label = Label(self.window,bg=BG_COLOUR, height=80)
        bottom_label.pack(fill=X)
        print("bottom label")

#messaage frame
        message_frame = Frame(bottom_label, bg=BG_COLOUR, pady=5)
        message_frame.pack(fill=X)
        print("message frame")
#message label
        message_label = Label(message_frame, text="Type your message here: ", font=FONT, fg="white")
        message_label.pack(side=LEFT)
        print("message label")
#messages
        self.message_entry = Entry(bottom_label, bg="lavender", fg=TEXT_COLOUR, font=FONT)
        self.message_entry.pack(side=LEFT, fill=X, expand=True)
        self.message_entry.focus_set()
        self.message_entry.bind("<Return>", self.on_enter_pressed)

        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=25, bg=BG_GRAY,
                             command=lambda: self.on_enter_pressed(None))
        print("send button")
        send_button.pack(side=RIGHT)

    def parse_message(self,msg):
        if msg=="blocked line":
            expert.declare(Fact(service = "line_blockage"))
        if msg=="700":
            expert.dictionary['time']=700
            expert.declare(Fact(time = 700))
            expert.declare(Fact(isQuestion = False))
            expert.declare(Fact(time_provided=True))
        if msg == 'LIVST':
            expert.dictionary['location']="LIVST"
            expert.declare(Fact(location = 'LIVST'))
            expert.declare(Fact(isQuestion = False))
            expert.declare(Fact(location_provided=True))
        if msg == 'partial':
            expert.dictionary['full_or_part']="partial"
            expert.declare(Fact(full_or_part = 'partial'))
            expert.declare(Fact(isQuestion = False))
            expert.declare(Fact(full_or_part_provided=True))
        if msg == 'train staff':
            expert.dictionary['customer']="train_staff"
            expert.declare(Fact(customer = 'train_staff'))
            expert.declare(Fact(isQuestion = False))
            expert.declare(Fact(customer_provided=True))

    def on_enter_pressed(self, event):
        msg = self.message_entry.get()
        self.insert_messages(msg, "You ")
        self.parse_message(msg)
        expert.declare(Fact("get_input", user_input=msg))
        expert.run()

    def initial_message(self):
        message = "Welcome to the train service chatbot!\nWhat can I help you with today? \n" 
        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert(END, message)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    def insert_messages(self, msg, sender):
        if not msg:
            return

        self.message_entry.delete(0,END)
        msg1 = f"{sender}: {msg} \n"
        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.see(CURRENT)
        self.text_widget.configure(state=DISABLED)


#%%

    
def find_intention(user_input, dictionary, knowledge):
    if user_input == "blocked":
        knowledge['question'] = 'ask_location'
        return 'line_block'
    

#get the advice
# df = pd.read_csv('contingency_advice.csv')
# df = df.replace(r'\\n', '\n', regex=True)
# print(df['alt_transport'][2])

class line_blockage(Fact):
    "Contains all info about the event"
    pass

class location(Fact):
    "contains 2 station names that has a line blockage"
    pass
class isQuestion(Fact):
    "contains 2 station names that has a line blockage"
    pass

class line_block_loc(Fact):
    "contains 2 station names that has a line blockage"
    pass

class full_or_part(Fact):
    "Full or partial line blockage?"
    pass
    
class time(Fact):
    "Time for the required advice"
    pass

class customer(Fact):
    "Who is the bot talking to?"
    pass

class contingency_expert(KnowledgeEngine):


    # @DefFacts()
    # def _initial_action(self):
    #     if 'reset' in self.dictionary:
    #         if self.dictionary.get('reset') == 'true':
    #             self.knowledge = {}
    #             self.dictionary['service'] = 'chat'
    #         service = self.dictionary.get('service')
            
            
    #     yield Fact(service = self.knowledge.get('service'))

    #     # Set knowledge
    #     if not 'question' in self.knowledge:
    #         self.knowledge['question'] = str()

    #     if 'full_or_part' in self.knowledge:
    #         yield Fact(full_or_part = self.knowledge.get('full_or_part'))
    #     if 'time' in self.knowledge:
    #         yield Fact(time = self.knowledge.get('time'))
    #     if 'location' in self.knowledge:
    #         yield Fact(location = self.knowledge.get('location'))
    #     if 'customer' in self.knowledge:
    #         yield Fact(customer = self.knowledge.get('customer'))
            
    @Rule(
        AS.user_input_fact << Fact("get_input", user_input=MATCH.user_input),
        NOT(Fact(service="chat"))
        ) 
    def greeting(self, user_input_fact, user_input):
        self.retract(user_input_fact)
        self.dictionary.clear()
        self.knowledge.clear()
        if user_input.lower() == "hi":
            output = "hi! Is there currently a problem?"
            self.declare(Fact(service="chat"))
            self.knowledge['question'] ="asking_for_problem"
        else:
            output ="bye..."
        app.insert_messages(output, "ChatBot")
        
    @Rule(
        AS.user_input_fact << Fact("get_input", user_input=MATCH.user_input),
        Fact(service="chat"),
        NOT(Fact(location_provided=True))
        ) 
    def ask_if_blockage(self, user_input_fact, user_input):
        self.retract(user_input_fact)
        
        if self.knowledge["question"] == 'ask_if_blockage':
            output = "Sorry I don't get what you mean"
        else:
            self.knowledge['question'] = 'ask_if_blockage'
            output ="Is there currently a line blockage?"

        app.insert_messages(output, "ChatBot")

    #Ask location
    @Rule(
        AS.user_input_fact << Fact("get_input", user_input=MATCH.user_input),
        Fact(service= "line_blockage"),
        NOT(Fact(location_provided=True))
        ) 
    def get_location(self, user_input_fact, user_input):
        self.retract(user_input_fact)
        if 'location' in self.dictionary:
            location = self.dictionary.get('location')
            self.declare(Fact(location = location))
            self.knowledge['location'] = location
            self.declare(Fact(location_provided=True))
        else:
            #if it's already asked the question and can't comprehend it
            if self.knowledge['question'] == 'ask_location':
                output = "Sorry I dont geddit" 
            else:
                self.knowledge['question'] = 'ask_location'
                output = "Pls give location"
            self.knowledge['question'] = 'ask_location'
            app.insert_messages(output, "ChatBot")
            #self.declare(Fact(isQuestion = True))
            
   #ask time      
    @Rule(
        AS.user_input_fact << Fact("get_input", user_input=MATCH.user_input),
        Fact(service= "line_blockage"),
        NOT(Fact(time_provided=True)),
        NOT(Fact(isQuestion))
        ) 
    def get_time(self, user_input_fact, user_input):
        self.retract(user_input_fact)
        if 'time' in self.dictionary:
            time = self.dictionary.get('time')
            self.declare(Fact(time = time))
            self.knowledge['time'] = time
            self.declare(Fact(time_provided=True))
        else:
            #if it's already asked the question and can't comprehend it
            if self.knowledge['question'] == 'ask_time':
                output = "Sorry I dont geddit" 
            else:
                self.knowledge['question'] = 'ask_time'
                output= "What's the time?"
            #self.declare(Fact(isQuestion = True))
            self.knowledge['question'] = 'ask_time'
            app.insert_messages(output, "ChatBot: ")
       #ask full or part      
    @Rule(
        AS.user_input_fact << Fact("get_input", user_input=MATCH.user_input),
        Fact(service= "line_blockage"),
        NOT(Fact(full_or_part_provided=True)),
        NOT(Fact(isQuestion))
        ) 
    def get_full_or_part(self, user_input_fact, user_input):
        self.retract(user_input_fact)
        if 'full_or_part' in self.dictionary:
            full_or_part = self.dictionary.get('full_or_part')
            self.declare(Fact(full_or_part = full_or_part))
            self.knowledge['full_or_part'] = full_or_part
            self.declare(Fact(time_provided=True))
        else:
            #if it's already asked the question and can't comprehend it
            if self.knowledge['question'] == 'ask_full_or_part':
                output = "Sorry I dont geddit" 
            else:
                self.knowledge['question'] = 'ask_full_or_part'
                output= "Is it a full or partial blockage?"
            #self.declare(Fact(isQuestion = True))
            self.knowledge['question'] = 'ask_full_or_part'
            app.insert_messages(output, "ChatBot")
    #FULL OR PARTIAL?
    @Rule(
        AS.user_input_fact << Fact("get_input", user_input=MATCH.user_input),
        Fact(service= "line_blockage"),
        NOT(Fact(customer_provided=True)),
        NOT(Fact(isQuestion))
        ) 
    def get_customer(self, user_input_fact, user_input):
        self.retract(user_input_fact)
        if 'customer' in self.dictionary:
            customer = self.dictionary.get('customer')
            self.declare(Fact(customer = customer))
            self.knowledge['customer'] = customer
            self.declare(Fact(customer_provided=True))
        else:
            #if it's already asked the question and can't comprehend it
            if self.knowledge['question'] == 'ask_customer':
                output = "Sorry I dont geddit" 
            else:
                self.knowledge['question'] = 'ask_customer'
                output= "What is your profession?"
            #self.declare(Fact(isQuestion = True))

            self.knowledge['question'] = 'ask_customer'
            app.insert_messages(output, "ChatBot")
    #Once all the info is there, calculate the schedule amendments
    @Rule(Fact(service = 'line_blockage'),
        Fact(full_or_part = 'partial'),
        Fact(location = MATCH.location),
        Fact(time = MATCH.time),
        Fact(customer = "train_staff")
        )
    def advise_train_staff_part(self,  location,time):
        app.insert_messages(process_schedule_all.get_all_schedule_advice(location,time, train_schedules), "ChatBot")

        
#Init the expert
expert = contingency_expert()
expert.dictionary = {}
expert.knowledge = {}
expert.reset()

# Run the knowledge base to diagnose the illness
expert.run()


app = ChatBot()
app.run()
