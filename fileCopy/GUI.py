import os.path
import tkinter as tk
from tkinter import filedialog,messagebox
from fileCopy import CopyOp

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.grid()
        self.row=0
        self.FilePathEntry=[]
        self.FileOpenButton=[]
        self.PathLabels=[]
        self.DeleteButton=[]
        master.geometry("700x300")
        master.title("FileCopy")
        self.root=master
        self.create_widgets()

    def create_widgets(self):

        self.AddFileButton = tk.Button(self)
        self.AddFileButton["text"] = "AddFile"
        self.AddFileButton["command"] = self.addFile
        self.AddFileButton.grid(row = 0, column = 0)
        self.PathFrame=tk.Frame(self.root,width=100)
        self.PathFrame.grid(row = 1, column = 0,sticky=tk.EW)

        self.addFile(text="Root Directory:Copy to")
        self.addFile(text="Root Directory:Copy from ")

        self.quit = tk.Button(self, text="QUIT",
                              command=self.root.destroy)
        self.quit.grid(row = 0, column = 2)
        self.CopyExecButton = tk.Button(self, text="Copy!", fg="red",
                              command=self.ExecCopy)
        self.CopyExecButton.grid(row=0, column=1)
    def addFile(self,text=None):
        if len(self.FilePathEntry)>=2:
            if len(self.FilePathEntry[1].get())<=0:
                messagebox.showwarning("warning", "input Root Path of CopyFrom")
                return
        self.FilePathEntry.append(tk.Entry(self.PathFrame,width=70))
        self.FilePathEntry[-1].grid(row = self.row, column = 1,sticky=tk.EW)
        self.FileOpenButton.append(tk.Button(self.PathFrame))
        self.FileOpenButton[-1]["command"]=self.openFileExp(number=self.row)
        self.FileOpenButton[-1]["text"] = "open"
        self.FileOpenButton[-1].grid(row = self.row, column = 2)
        if self.row>=2:
            self.DeleteButton.append(tk.Button(self.PathFrame))
            self.DeleteButton[-1]["text"] = "delete"
            self.DeleteButton[-1]["command"]=self.deleteRow(number=self.row)
            self.DeleteButton[-1].grid(row=self.row,column=3)
        else:
            self.DeleteButton.append(None)
        if text is not None:
            self.PathLabels.append(tk.Label(self.PathFrame, text=text))
        else:
            self.PathLabels.append(tk.Label(self.PathFrame, text="relative path of copy file {}".format(self.row-1)))
        self.PathLabels[-1].grid(row=self.row, column=0)

        self.row+=1
    def deleteRow(self,number):
        def _deleteNum():
            self.FilePathEntry.pop(number).destroy()
            self.FileOpenButton.pop(number).destroy()
            self.DeleteButton.pop(number).destroy()
            self.PathLabels.pop(number).destroy()
            self.row-=1
            for i in range(2,self.row):
                self.FilePathEntry[i].grid(row = i, column = 1,sticky=tk.EW)
                self.FileOpenButton[i]["command"] = self.openFileExp(number=i)
                self.FileOpenButton[i].grid(row = i, column = 2)
                self.DeleteButton[i]["command"] = self.deleteRow(number=i)
                self.DeleteButton[i].grid(row = i, column = 3)
                self.PathLabels[i]["text"]="relative path of copy file {}".format(i-1)
                self.PathLabels[i].grid(row=i,column=0)
        return _deleteNum

    def openFileExp(self,number):
        def _openExp():

            if number<2:

                file = filedialog.askdirectory()
                if file is None or file=="":
                    return
            else:
                res = messagebox.askyesno("select mode", "yes: select directory\n no: select file")
                if res:
                    file = filedialog.askdirectory()
                    if file is None or file=="":
                        return
                else:
                    file = filedialog.askopenfile()
                    if file is None or file=="":
                        return
                    file=file.name
            if number<2:
                self.FilePathEntry[number].delete(0, tk.END)
                self.FilePathEntry[number].insert(tk.END, file)
            else:
                root=self.FilePathEntry[1].get()
                relpath=os.path.relpath(file,root)
                if ".." in relpath:
                    messagebox.showwarning("error","select child of Copy-To Root Directory")
                    return
                self.FilePathEntry[number].delete(0, tk.END)
                self.FilePathEntry[number].insert(tk.END,relpath)
        return _openExp
    def ExecCopy(self):
        cp=CopyOp()
        cp.copyToRoot=self.FilePathEntry[0].get()
        cp.copyFromRoot=self.FilePathEntry[1].get()
        for i in range(2,len(self.FilePathEntry)):
            cp.copyFromChildDirs.append(self.FilePathEntry[i].get())
        result=cp.copyFile()
        if result:
            messagebox.showinfo("info","Copied")
        else:
            messagebox.showinfo("info","not copied")

def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()

if __name__ == "__main__":
    main()