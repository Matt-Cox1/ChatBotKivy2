import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

import warnings

warnings.filterwarnings('ignore')
import requests
# Design elements

def on_start_up():
    global model,numResults, maxTokens,stopSequences,topKReturn,temperature,full_prompt,total_cost,convo_cost, initial_prompt

    # Change the position of these
    model = "j1-large"  # Options are j1-large or j1-jumbo
    numResults = 1  # A value greater than 1 is meaningful only in case of non-greedy decoding, i.e. temperature > 0.
    maxTokens = 100  # The maximum number of tokens to generate per result
    stopSequences = ["\n"]
    topKReturn = 0  # Between 0 and 64
    temperature = 0.6  # Can go from 0 to 5.
    convo_cost = 0
    total_cost = find_total_cost(model)
    initial_prompt = prompt_creation("physics")
    full_prompt = prompt_creation("physics")



def run_chatbot(prompt):
    global settings, res, completion, data, number_of_tokens
    settings = model, prompt, numResults, maxTokens, stopSequences, topKReturn, temperature
    res = get_completion(settings)  # Model Running
    completion = res.json()['completions'][0]['data']['text']
    data = list(res.json()['completions'])[0]
    number_of_tokens = len(res.json()['prompt']['tokens']) + len(list(data['data']['tokens']))
    return [completion, number_of_tokens]

def get_completion(settings):
    (model, prompt, numResults, maxTokens, stopSequences, topKReturn, temperature) = settings
    API_KEY = "rrK3FjjiTW6R2zI8rAhYKP8cwWPrYEBW"
    result = requests.post(
        f"https://api.ai21.com/studio/v1/{model}/complete",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "prompt": prompt,
            "numResults": numResults,
            "maxTokens": maxTokens,
            "stopSequences": stopSequences,
            "topKReturn": topKReturn,
            "temperature": temperature  # Up to 5
        })
    return result

def find_total_cost(model):
    if model == "j1-jumbo":
        file_jumbo = open("JumboCost.txt", "r")
        previous_cost = file_jumbo.read()
        return previous_cost
    if model == "j1-large":
        file_large = open("LargeCost.txt", "r")
        previous_cost = file_large.read()
        return previous_cost

def update_cost_files(model, cost):
    previous_cost = find_total_cost(model)
    if model == "j1-large":
        file_large = open("LargeCost.txt", "w")
        file_large.write(str(int(cost) + int(previous_cost)))
        print(f"Just wrote {int(cost) + int(previous_cost)} onto the file LargeCost.txt")
    elif model == "j1-jumbo":
        file_jumbo = open("JumboCost.txt", "w")
        file_jumbo.write(str(int(cost) + int(previous_cost)))
        print(f"Just wrote {int(cost) + int(previous_cost)} onto the file JumboCost.txt")
    else:
        print("Shite model name is wrong")

def set_files_to_0():
    file_large = open("LargeCost.txt", "w")
    file_large.write("0")
    file_jumbo = open("JumboCost.txt", "w")
    file_jumbo.write("0")

def prompt_creation(program_type):
    global temperature, model,chatbot,ID,AI
    if program_type.lower() =="physics":
        ID = "Question"
        AI = "Physics guru answer"
        temperature = 0.3
        model = "j1-jumbo"
        chatbot = False
        prompt = "A specialist in theoretical physics concisely answers meaningful questions about the nature of the universe and mathematical laws.\n\n"
        prompt += f"{ID}: What is spin in quantum mechanics?\n"
        prompt += f"{AI}: Spin is intrinsic angular momentum associated with elementary particles. It is a purely quantum mechanical phenomenon without any analog in classical physics.\n"
        prompt += f"{ID}: What is Newton's first law?\n"
        prompt += f"{AI}: An object remains in the same state of motion unless a resultant force.\n"
        return prompt
    if program_type.lower() =="chatbot":
        ID = "Question"
        AI = "Physics guru answer"
        temperature = 0.3
        model = "j1-jumbo"
        chatbot = False
        prompt = "A specialist in theoretical physics concisely answers meaningful questions about the nature of the universe and mathematical laws.\n\n"
        prompt += f"{ID}: What is spin in quantum mechanics?\n"
        prompt += f"{AI}: Spin is intrinsic angular momentum associated with elementary particles. It is a purely quantum mechanical phenomenon without any analog in classical physics.\n"
        prompt += f"{ID}: What is Newton's first law?\n"
        prompt += f"{AI}: An object remains in the same state of motion unless a resultant force.\n"
        return prompt

on_start_up()

class MyGrid(GridLayout):
    def __init__(self,**kwargs):
        super(MyGrid,self).__init__(**kwargs)
        # Main Grid
        self.cols = 1

        # Lets add widgets
        self.title = Label(text="Ask me anything-AI21 Jurassic Model NLP", font_size = 40, size_hint=(0,1), underline=True)
        self.add_widget(self.title)
        self.subtitle2 = Label(text=f"Current Cost on model {model} = {find_total_cost(model)}", font_size=15)
        self.add_widget(self.subtitle2)
        self.subtitle3 = Label(text=f"Current Cost of conversation = {convo_cost}", font_size=15)
        self.add_widget(self.subtitle3)
        self.useless_bar = Label(text="-----------------------------------------------------------------------", font_size = 30)
        self.add_widget(self.useless_bar)
        self.subtitle1 = Label(text="Physics Related Conversation", font_size=18, underline=True)
        self.add_widget(self.subtitle1)
        self.chatbox = Label(text=f"""""",size_hint=(0,4))
        self.add_widget(self.chatbox)
        self.useless_bar2 = Label(text="-----------------------------------------------------------------------", font_size = 30)
        self.add_widget(self.useless_bar2)
        self.prompt = TextInput(multiline=False)
        self.prompt.bind(on_text_validate=self.enter_f)
        self.add_widget(self.prompt)


        #Inner grid:
        self.inside = GridLayout()
        self.inside.cols = 4

        self.enter = Button(text="Submit")
        self.inside.add_widget(self.enter)
        self.enter.bind(on_press=self.enter_f)
        self.reset = Button(text="Reset")
        self.inside.add_widget(self.reset)
        self.reset.bind(on_press=self.reset_f)
        self.new_day = Button(text="New Day")
        self.inside.add_widget(self.new_day)
        self.new_day.bind(on_press=self.new_day_f)
        self.model_switch = Button(text="Switch Models")
        self.inside.add_widget(self.model_switch)
        self.model_switch.bind(on_press=self.model_switch_f)


        # Lets chuck the inner grid into the main grid:
        self.add_widget(self.inside)

    def enter_f(self,instance):
        global full_prompt,convo_cost,ID,AI,initial_prompt
        text = self.prompt.text
        full_prompt += f"\n{ID}: {text}\n{AI}:"
        print(f"START:{full_prompt}")
        ai_output = run_chatbot(full_prompt)
        full_prompt += f"{ai_output[0]}"
        cost_of_op = ai_output[1]
        if ai_output[0].strip()=="":
            ai_output[0]="Sorry. I've had a brain fart and have no idea what we were just talking about. You should probably restart me."
        self.chatbox.text = self.chatbox.text+ f"{ID}: {text}\n{AI}:{ai_output[0]}\n"
        print(f"END:{full_prompt}")
        self.prompt.text = ""
        convo_cost+=cost_of_op
        self.subtitle3.text = f"Current Cost of Conversation = {convo_cost}"

        print("That cost:",cost_of_op)
        update_cost_files(model, cost_of_op)

        self.subtitle2.text = f"Current Cost of model {model} = {find_total_cost(model)}"
        print(f"Current cost of the {model} model is {find_total_cost(model)}.")
    def reset_f(self,instance):
        global convo_cost
        global full_prompt
        self.prompt.text = ""
        self.chatbox.text = ""
        full_prompt = ""
        self.subtitle2.text = f"Current Cost of model {model} = {find_total_cost(model)}"
        convo_cost =0
        self.subtitle3.text = f"Current Cost of Convosation = {convo_cost}"
        print("reset")
    def new_day_f(self,instance):
        global convo_cost
        print("new_day")
        set_files_to_0()
        convo_cost = 0
        self.subtitle3.text = f"Current Cost of Convosation = {convo_cost}"

        self.subtitle2.text = f"Current Cost of model {model} = {find_total_cost(model)}"
    def model_switch_f(self,instance):
        global model
        if model=="j1-large":
            model= "j1-jumbo"
        else:
            model = "j1-large"
        self.subtitle2.text = f"Current Cost of model {model} = {find_total_cost(model)}"


class MyApp(App):
    # Inherates from app
    def build(self):
        return MyGrid()






if __name__ == "__main__":
    MyApp().run()