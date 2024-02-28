
'''
list all the commands in tmux and allow for them to be constructed
'''

#from Tkinter import *

import sys
if sys.version_info[0] == 3:
    from tkinter import *
    import _thread as thread #WTF Python!
else:
    from Tkinter import *
    import thread

from subprocess import call
import time
import functools

class UserInterface(Frame):
    def __init__(self, parent, logic):
        Frame.__init__(self, parent)
        self.parent = parent
        self.app = logic
        self.limit = None
        self.actions = {
            "Split Vertical":"split-window"
            , "Split Horizontaly": "split-window -h"
            , "Clock": "clock-mode"
        }
        self.init()
    def init(self):
        self.parent.title("TMUX-ER")
        self.pack(fill=BOTH, expand=True)
        
        self.limit = Scale(self.parent, from_=0, to=32, orient=HORIZONTAL)
        
        sizeLabel = Label(self.parent, text="Resize active panel")
        sizeLabel.pack()
        
        brow = Frame(self.parent)
        brow.pack(fill=X)
        
        bleft = Button(brow, text="L", command=self.app.callbackLeft)
        bdown = Button(brow, text="D", command=self.app.callbackDown)
        bup = Button(brow, text="U", command=self.app.callbackUp)
        bright = Button(brow, text="R", command=self.app.callbackRight)
        
        self.limit.pack()
        bleft.pack(side=LEFT)
        bdown.pack(side=LEFT)
        bup.pack(side=LEFT)
        bright.pack(side=LEFT)

        brot = Button(self.parent, text="Rotate Panels", command=self.app.callbackRotatePanels)
        brot.pack()
        
        self.commands = Listbox(self.parent)
        self.commands.pack()
        
        for o in self.actions:
            data = self.actions[o]
            parts = data.split(" ")
            args = ["tmux", parts[:1][0] ] + parts[1:]
            button = Button(self.parent, text=o,
                command=functools.partial(self.app.send2, o))
            button.pack()

    def fillList(self, list):
        pass

class AppLogic():
    def __init__(self, ui):
        self.view = ui
        self.rotating=False
    def send(self, cmd):
        call(cmd)
    def send2(self, which):
        cmd = ["tmux"] + self.view.actions[which].split(" ")
        self.send(cmd)
    
    def clockMode(self):
        self.send(["tmux", "clock-mode"])
    
    def callbackLeft(self):
        self.send(["tmux", "resize-pane", "-L"])
    def callbackDown(self):
        self.send(["tmux", "resize-pane", "-D"])
    def callbackUp(self):
        self.send(["tmux", "resize-pane", "-U"])
    def callbackRight(self):
        self.send(["tmux", "resize-pane", "-R"])
    
    def callbackRotatePanels(self):
        if self.rotating:
            #already running
            self.rotating=False
        else:
            #start the job
            self.rotating=True
            thread.start_new_thread(self.rotatePanels, ("rotater", 3,))
    def rotatePanels(self, threadName, delay):
        which = 0
        while self.rotating:
            self.send(["tmux", "select-pane", "-t", str(which)])
            self.send(["tmux", "resize-pane", "-Z"])
            which = which + 1
            if self.view.limit.get()<=which:
                which = 0
            time.sleep(delay)
    
def main():
    master = Tk()
    app=AppLogic(None)
    ui=UserInterface(master, app)
    app.view = ui
    master.mainloop()

if __name__ == "__main__":
    main()
