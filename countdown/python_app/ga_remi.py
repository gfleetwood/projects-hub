import countdown_ga
import numpy as np
import random
import remi.gui as gui
from remi import start, App
import sys
import re
import time
from threading import Timer
from concurrent.futures import ThreadPoolExecutor

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.time = -1
        self.best_individual = None

        container_main = gui.Widget(width ='100%', height = '100%', margin = '0px')
        container_main.style['display'] = 'block'
        container_main.style['overflow'] = 'auto'
        container_main.style['position'] = "absolute"

        title = gui.Label('COUNTDOWN NUMBER\'S ROUND')
        title.style['margin'] = "0px auto"
        title.style['left'] = "450px"
        title.style['height'] = "40px"
        title.style['display'] = "block"
        title.style['font-weight'] = "bolder"
        title.style['width'] = "250px"
        title.style['top'] = "21px"
        title.style['position'] = "absolute"
        title.style['overflow'] = "auto"

        intro = gui.Label("Compete against a genetic algorithm this section of the famous game show. \
                           The goal is to construct a valid mathematical expression that is as close to\
                           the target as possible. Only addition, subtraction, multiplication, and division\
                           are allowed. The closest answer wins. Press 'PLAY' to begin and 'REPLAY' and \
                           then 'PLAY' to compete again. ")
        intro.style['margin'] = "0px auto"
        intro.style['left'] = "150px"
        intro.style['height'] = "250px"
        intro.style['display'] = "block"
        intro.style['width'] = "269px"
        intro.style['top'] = "59px"
        intro.style['position'] = "absolute"
        intro.style['overflow'] = "auto"

        self.code_link = gui.Link("", "CODE", width = 200, height = 30)
        self.code_link.style['margin'] = "0px auto"
        self.code_link.style['left'] = "200px"
        self.code_link.style['height'] = "250px"
        self.code_link.style['display'] = "block"
        self.code_link.style['width'] = "200px"
        self.code_link.style['top'] = "280px"
        self.code_link.style['position'] = "absolute"
        self.code_link.style['overflow'] = "auto"

        self.blog_link = gui.Link("", "BLOG", width = 200, height = 30)
        self.blog_link.style['margin'] = "0px auto"
        self.blog_link.style['left'] = "280px"
        self.blog_link.style['height'] = "250px"
        self.blog_link.style['display'] = "block"
        self.blog_link.style['width'] = "200px"
        self.blog_link.style['top'] = "280px"
        self.blog_link.style['position'] = "absolute"
        self.blog_link.style['overflow'] = "auto"

        #Buttons

        self.reset = gui.Button('RESET')
        self.reset.style['margin'] = "0px auto"
        self.reset.style['left'] = "801px"
        self.reset.style['height'] = "30px"
        self.reset.style['display'] = "block"
        self.reset.style['width'] = "100px"
        self.reset.style['top'] = "59px"
        self.reset.style['position'] = "absolute"
        self.reset.style['overflow'] = "auto"
        self.reset.set_on_click_listener(self.reset_game)

        self.play = gui.Button('PLAY')
        self.play.style['margin'] = "0px auto"
        self.play.style['left'] = "657px"
        self.play.style['height'] = "30px"
        self.play.style['display'] = "block"
        self.play.style['width'] = "100px"
        self.play.style['top'] = "59px"
        self.play.style['position'] = "absolute"
        self.play.style['overflow'] = "auto"
        self.play.set_on_click_listener(self.on_button_pressed)

        #Data
 
        target_title = gui.Label('Target')
        target_title.style['margin'] = "0px auto"
        target_title.style['left'] = "810px"
        target_title.style['height'] = "30px"
        target_title.style['display'] = "block"
        target_title.style['width'] = "50px"
        target_title.style['top'] = "120px"
        target_title.style['position'] = "absolute"
        target_title.style['overflow'] = "auto"

        self.target_num = gui.Label('')
        self.target_num.style['text-align'] = 'center'
        self.target_num.style['margin'] = "0px auto"
        self.target_num.style['left'] = "886px"
        self.target_num.style['height'] = "30px"
        self.target_num.style['display'] = "block"
        self.target_num.style['border-style'] = "solid"
        self.target_num.style['width'] = "100px"
        self.target_num.style['top'] = "120px"
        self.target_num.style['position'] = "absolute"
        self.target_num.style['overflow'] = "auto"

        nums_title = gui.Label('Numbers')
        nums_title.style['margin'] = "0px auto"
        nums_title.style['left'] = "550px"
        nums_title.style['height'] = "30px"
        nums_title.style['display'] = "block"
        nums_title.style['width'] = "100px"
        nums_title.style['top'] = "120px"
        nums_title.style['position'] = "absolute"
        nums_title.style['overflow'] = "auto"

        self.nums_to_use = gui.Label('')
        self.nums_to_use.style['text-align'] = 'center'
        self.nums_to_use.style['margin'] = "0px auto"
        self.nums_to_use.style['left'] = "635px"
        self.nums_to_use.style['height'] = "30px"
        self.nums_to_use.style['display'] = "block"
        self.nums_to_use.style['border-style'] = "solid"
        self.nums_to_use.style['width'] = "150px"
        self.nums_to_use.style['top'] = "120px"
        self.nums_to_use.style['position'] = "absolute"
        self.nums_to_use.style['overflow'] = "auto"

        ga_soln_title = gui.Label('G.A Solution')
        ga_soln_title.style['margin'] = "0px auto"
        ga_soln_title.style['left'] = "550px"
        ga_soln_title.style['height'] = "30px"
        ga_soln_title.style['display'] = "block"
        ga_soln_title.style['width'] = "100px"
        ga_soln_title.style['top'] = "180px"
        ga_soln_title.style['position'] = "absolute"
        ga_soln_title.style['overflow'] = "auto"

        self.ga_soln = gui.Label('')
        self.ga_soln.style['margin'] = "0px auto"
        self.ga_soln.style['text-align'] = 'center'
        self.ga_soln.style['left'] = "635px"
        self.ga_soln.style['height'] = "25px"
        self.ga_soln.style['display'] = "block"
        self.ga_soln.style['border-style'] = "solid"
        self.ga_soln.style['font-weight'] = "normal"
        self.ga_soln.style['width'] = "150px"
        self.ga_soln.style['top'] = "180px"
        self.ga_soln.style['position'] = "absolute"
        self.ga_soln.style['overflow'] = "auto"

        user_soln_title = gui.Label('Your Solution')
        user_soln_title.style['margin'] = "0px auto"
        user_soln_title.style['left'] = "550px"
        user_soln_title.style['height'] = "30px"
        user_soln_title.style['display'] = "block"
        user_soln_title.style['width'] = "100px"
        user_soln_title.style['top'] = "240px"
        user_soln_title.style['position'] = "absolute"
        user_soln_title.style['overflow'] = "auto"

        self.user_soln = gui.TextInput(True,'')
        self.user_soln.style['margin'] = "0px auto"
        self.user_soln.style['text-align'] = 'center'
        self.user_soln.style['font-weight'] = "normal"
        self.user_soln.style['left'] = "635px"
        self.user_soln.style['border-style'] = "solid"
        self.user_soln.style['height'] = "25px"
        self.user_soln.style['display'] = "block"
        self.user_soln.style['width'] = "150px"
        self.user_soln.style['top'] = "240px"
        self.user_soln.style['position'] = "absolute"
        self.user_soln.style['overflow'] = "auto"
        self.user_soln.set_on_change_listener(self.on_text_area_change)

        timer_title = gui.Label('TIMER')
        timer_title.style['margin'] = "0px auto"
        timer_title.style['left'] = "550px"
        timer_title.style['height'] = "30px"
        timer_title.style['display'] = "block"
        timer_title.style['width'] = "100px"
        timer_title.style['top'] = "280px"
        timer_title.style['position'] = "absolute"
        timer_title.style['overflow'] = "auto"

        self.timer = gui.TextInput('00:00')
        self.timer.style['margin'] = "0px auto"
        self.timer.style['text-align'] = 'center'
        self.timer.style['font-weight'] = "normal"
        self.timer.style['left'] = "635px"
        self.timer.style['border-style'] = "solid"
        self.timer.style['height'] = "25px"
        self.timer.style['display'] = "block"
        self.timer.style['width'] = "150px"
        self.timer.style['top'] = "280px"
        self.timer.style['position'] = "absolute"
        self.timer.style['overflow'] = "auto"      

        w_title = gui.Label('WINNER')
        w_title.style['margin'] = "0px auto"
        w_title.style['left'] = "810px"
        w_title.style['height'] = "30px"
        w_title.style['display'] = "block"
        w_title.style['width'] = "100px"
        w_title.style['top'] = "280px"
        w_title.style['position'] = "absolute"
        w_title.style['overflow'] = "auto"

        self.winner = gui.TextInput('')
        self.winner.style['margin'] = "0px auto"
        self.winner.style['text-align'] = 'center'
        self.winner.style['font-weight'] = "normal"
        self.winner.style['left'] = "886px"
        self.winner.style['border-style'] = "solid"
        self.winner.style['height'] = "25px"
        self.winner.style['display'] = "block"
        self.winner.style['width'] = "150px"
        self.winner.style['top'] = "280px"
        self.winner.style['position'] = "absolute"
        self.winner.style['overflow'] = "auto"   

        ga_soln_result_title = gui.Label('G.A Result')
        ga_soln_result_title.style['margin'] = "0px auto"
        ga_soln_result_title.style['left'] = "810px"
        ga_soln_result_title.style['height'] = "30px"
        ga_soln_result_title.style['display'] = "block"
        ga_soln_result_title.style['width'] = "100px"
        ga_soln_result_title.style['top'] = "180px"
        ga_soln_result_title.style['position'] = "absolute"
        ga_soln_result_title.style['overflow'] = "auto"

        self.ga_soln_result = gui.Label('')
        self.ga_soln_result.style['text-align'] = 'center'
        self.ga_soln_result.style['margin'] = "0px auto"
        self.ga_soln_result.style['border-style'] = "solid"
        self.ga_soln_result.style['left'] = "886px"
        self.ga_soln_result.style['height'] = "30px"
        self.ga_soln_result.style['display'] = "block"
        self.ga_soln_result.style['width'] = "100px"
        self.ga_soln_result.style['top'] = "180px"
        self.ga_soln_result.style['position'] = "absolute"
        self.ga_soln_result.style['overflow'] = "auto"

        user_soln_result_title = gui.Label('Your Result')
        user_soln_result_title.style['margin'] = "0px auto"
        user_soln_result_title.style['left'] = "810px"
        user_soln_result_title.style['height'] = "30px"
        user_soln_result_title.style['display'] = "block"
        user_soln_result_title.style['width'] = "100px"
        user_soln_result_title.style['top'] = "240px"
        user_soln_result_title.style['position'] = "absolute"
        user_soln_result_title.style['overflow'] = "auto"

        self.user_soln_result = gui.Label('')
        self.user_soln_result.style['border-style'] = "solid"
        self.user_soln_result.style['text-align'] = 'center'
        self.user_soln_result.style['margin'] = "0px auto"
        self.user_soln_result.style['left'] = "886px"
        self.user_soln_result.style['height'] = "30px"
        self.user_soln_result.style['display'] = "block"
        self.user_soln_result.style['width'] = "150px"
        self.user_soln_result.style['top'] = "240px"
        self.user_soln_result.style['position'] = "absolute"
        self.user_soln_result.style['overflow'] = "auto"

        #Concatenation

        container_main.append(ga_soln_title,'ga_soln_title')
        container_main.append(target_title,'target_title')
        container_main.append(self.play,'play')
        container_main.append(self.reset ,'reset')
        container_main.append(title,'title')
        container_main.append(self.nums_to_use,'nums_to_use')
        container_main.append(user_soln_title,'user_soln_title')
        container_main.append(nums_title,'nums_title')
        container_main.append(self.ga_soln,'ga_soln')
        container_main.append(intro,'intro')
        container_main.append(self.user_soln,'user_soln')
        container_main.append(self.target_num,'target_num')

        container_main.append(timer_title,'timer_title')
        container_main.append(self.timer,'timer')
        container_main.append(w_title,'w_title')
        container_main.append(self.winner,'winner')
        #container_main.append(self.code_link,'code_link')
        #container_main.append(self.blog_link,'blog_link')

        container_main.append(ga_soln_result_title,'ga_soln_result_title')
        container_main.append(self.ga_soln_result,'ga_soln_result')
        container_main.append(user_soln_result_title,'user_soln_result_title')
        container_main.append(self.user_soln_result,'user_soln_result')   

        return container_main

    def on_text_area_change(self, widget, newValue):
        if self.time < 0:
            return None
        user_input = self.user_soln.get_value()
        nums = self.nums_storage
        numbers = [int(i) for i in re.findall('\d+', user_input) if i.isdigit()]

        if (set(numbers)!=set(nums)):
            self.user_soln_result.set_text(str('Use The Numbers Given'))
        elif (set(numbers)==set(nums)) and (eval(user_input) < 0):
            self.user_soln_result.set_text(str('Not Positive'))
        elif (set(numbers)==set(nums)) and ((np.abs(eval(user_input) - int(eval(user_input))) > 0)):
            self.user_soln_result.set_text(str('Not An Integer'))            
        else:
            self.user_soln_result.set_text(str(eval(user_input)))

    def reset_game(self, widget):

        if self.time > -1:
            pass
        else:
            self.target_num.set_text('')
            self.nums_to_use.set_text('')  
            self.ga_soln.set_text('')  
            self.ga_soln_result.set_text('')  
            self.winner.set_text('')
            self.user_soln_result.set_text('')

    def on_button_pressed(self, widget):

        if len(self.target_num.get_text()) == 0:
            target, nums, ops = countdown_ga.setup()
            self.target = target
            self.nums_storage = nums
            self.ops = ops
       
        if self.time > -1:
            pass
        else:
            self.time = 40
            self.target_num.set_text(str(self.target))
            self.nums_to_use.set_text(', '.join([str(num) for num in self.nums_storage]))
            funcs = [self.run_genetic_algorithm, self.display_counter]

            with ThreadPoolExecutor(max_workers=3) as e:
                result = e.map(lambda x: x(), funcs)
                self.best_individual = list(result)[0]

    def run_genetic_algorithm(self):
        _, best_individual = countdown_ga.run_count_down(self.nums_storage, self.ops, self.target, times = 10000)        
        return best_individual

    def display_counter(self):
        if self.time>-1:
            self.timer.set_text('00:{:02d}'.format(self.time))
            self.time -= 1
            Timer(1, self.display_counter).start()
        else:
            self.ga_soln.set_text(''.join(self.best_individual[0]))
            self.ga_soln_result.set_text(str(int(self.best_individual[1])))
            verdict = self.determine_winner()
            self.winner.set_text(verdict)

    def determine_winner(self):
        result = 'Algorithm Wins!'
        ga_score = np.abs(self.target - int(self.ga_soln_result.get_text()))
        try:
            user_score = np.abs(self.target - int(self.user_soln_result.get_text()))
        except:
            user_score = 10**6
        if ga_score > user_score:
            result = 'User Wins!'
        elif ga_score == user_score:
            result = 'Draw!'
        return  result 
            

if __name__ == "__main__":
    # starts the webserver
    start(MyApp, port=5000)