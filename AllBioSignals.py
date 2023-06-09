from pylsl import StreamInlet, resolve_stream
import tkinter as tk
import threading

class GUI:

    def __init__(self):
        self.inlet = None

        self.root = tk.Tk()

        self.root.geometry("300x300")
        self.root.title("AllBioSignals")


        self.type = ""
        types = ["type","name","hostname"]
        ctypes = tk.StringVar(value=types)
        self.listbox = tk.Listbox(self.root,listvariable=ctypes,height=3)
        self.listbox.bind('<<ListboxSelect>>',self.item_selected)
        self.listbox.pack(padx=10,pady=10)

        self.name = tk.StringVar()
        self.entryName = tk.Entry(self.root,textvariable=self.name)
        self.entryName.pack(padx=10,pady=10)
        self.name.trace_add('write',self.has_written)

        self.labelResolveStream = tk.Label(self.root, text="Resolving Stream for info : \n"+"Type : "+self.type+" Name : "+self.name.get())
        self.labelResolveStream.pack(padx=10,pady=10)

        self.buttonResolveStream = tk.Button(self.root,text="Resolve Stream",command=threading.Thread(target=self.OpenStream).start)
        self.buttonResolveStream.pack(padx=10,pady=10)

        self.root.mainloop()


    def item_selected(self,event):
        selected_id = self.listbox.curselection()
        self.type = self.listbox.get(selected_id)
        self.labelResolveStream.config(text="Resolving Stream for info : \n"+"Type : "+self.type+" Name : "+self.name.get())

    def has_written(self,*args):
        self.labelResolveStream.config(text="Resolving Stream for info : \n"+"Type : "+self.type+" Name : "+self.name.get())

    def OpenStream(self):
        print(self.type,self.name.get())
        os_stream = resolve_stream(self.type,self.name.get())
        self.inlet = StreamInlet(os_stream[0])
        if self.inlet != None:
            self.SecondWindow()
    
    def SecondWindow(self):
        sw = tk.Tk()

        sw.title("Streaming Window")
        sw.geometry("500x400")

        labelConsole = tk.Label(sw,text="Console : ")
        labelConsole.pack(padx=10,pady=20,side='top')

        self.Console = tk.Text(sw,height = 10)
        self.Console.pack(padx=10,pady=20)

        self.stateShowStream = tk.IntVar()
        btnShowStream = tk.Checkbutton(sw,text="Show Stream",command=threading.Thread(target=self.ShowStream,args=(self.stateShowStream,)).start,variable=self.stateShowStream)
        btnShowStream.pack(padx=10,pady=20)

        sw.mainloop()

    def ShowStream(self):
        while self.stateShowStream:
            sample, timestamp = self.inlet.pull_sample()
            self.Console.insert(tk.END,"time: "+str(timestamp)+" val: "+str(sample[1])+"\n")


            

if __name__ == "__main__":
    GUI()