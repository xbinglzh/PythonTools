import sys
import Tkinter
import tkMessageBox

from Scan_Excel import ScanExcel
from Scan_Plist import ScanPlist
from Scan_Map_Excel import ScanMapExcel
from ScanPlistToBin import ScanPlistToBin

########################################################################
class ToolGui:
    
    #----------------------------------------------------------------------
    def __init__(self):
        
        self.scanExcel = ScanExcel()
        self.scanPlist = ScanPlist()
        self.scanMap = ScanMapExcel()
        self.scanPlistToBin  = ScanPlistToBin()
        
        self.mainWindow = Tkinter.Tk()
        self.mainWindow.title("Excel Plist Tool")
        self.top_frame = Tkinter.Frame(self.mainWindow)
        self.center_frame = Tkinter.Frame(self.mainWindow)
        self.center_plist_frame = Tkinter.Frame(self.mainWindow)
        self.bottom_frame = Tkinter.Frame(self.mainWindow)
        self.center_bin_frame = Tkinter.Frame(self.mainWindow)
        self.center_bin_out_frame = Tkinter.Frame(self.mainWindow)
        self.bottom_bin_frame = Tkinter.Frame(self.mainWindow)
        
        self.inputResourse = Tkinter.Label( self.top_frame, text = " input Resourse " )
        self.outputResourse = Tkinter.Label( self.center_frame, text = "output Resourse" )
        self.plistResourse = Tkinter.Label(self.center_plist_frame,text ="  plist  Resourse")
        self.binPlistInputResourse = Tkinter.Label(self.center_bin_frame, text = "bin  in  Resourse")
        self.binPlistOutputResourse = Tkinter.Label(self.center_bin_out_frame , text = "binOut Resourse")
        
        self.inputentry = Tkinter.Entry(self.top_frame,width = 50)
        self.outEntry = Tkinter.Entry(self.center_frame,width = 50)
        self.plistEntry = Tkinter.Entry(self.center_plist_frame,width = 50)
        self.binPlistInEntry = Tkinter.Entry(self.center_bin_frame , width = 50)
        self.binPlistOutEntry = Tkinter.Entry(self.center_bin_out_frame, width = 50)
        
        self.buttonExcel2Plist = Tkinter.Button(self.bottom_frame,text = 'Excel2Plist', command = self.__excel2Plist__)
        self.buttonPlist2Excel = Tkinter.Button(self.bottom_frame,text = 'Plist2Excel', command = self.__plist2Excel__)
        self.buttonMap2Excel = Tkinter.Button(self.bottom_frame,text = 'Map2Plist', command =  self.__map2Plist__ )
        self.buttonPlist2Bin     =  Tkinter.Button(self.bottom_bin_frame , text = 'Plist2Bin' , command = self.__Plist2Bin__)
        
        self.buttonQuit = Tkinter.Button(self.bottom_bin_frame,text = 'Quit', command = self.mainWindow.quit)
        
        self.inputResourse.pack(side = 'left') 
        self.inputentry.pack(side = 'left')
        
        self.outputResourse.pack(side= 'left')
        self.outEntry.pack(side= 'left')
        
        self.plistResourse.pack(side= 'left')
        self.plistEntry.pack(side= 'left')
        
        self.buttonExcel2Plist.pack(side = 'left')
        self.buttonPlist2Excel.pack(side = 'left')
        self.buttonMap2Excel.pack(side = 'left')

        self.binPlistInputResourse.pack(side = 'left')
        self.binPlistInEntry.pack(side = 'left')
        self.binPlistOutputResourse.pack(side = 'left')
        self.binPlistOutEntry.pack(side = 'left')
        
        self.buttonPlist2Bin.pack(side = 'left')
        self.buttonQuit.pack(side = 'left')
        
        self.top_frame.pack()
        self.center_frame.pack()
        self.center_plist_frame.pack()
        self.bottom_frame.pack()
        self.center_bin_frame.pack()
        self.center_bin_out_frame.pack()
        self.bottom_bin_frame.pack()
        
       
        Tkinter.mainloop()
        
    #----------------------------------------------------------------------
    def __excel2Plist__(self):
        
        if self.inputentry.get() == "" or self.outEntry.get() =="":
            tkMessageBox.showerror('Result',"input res or output res is requested!")
            return
        info =  self.scanExcel.sacnExcelDir(self.inputentry.get(),self.outEntry.get())
        tkMessageBox.showinfo('Result',info)        
    
        #----------------------------------------------------------------------
    def __plist2Excel__(self):
        
        if self.outEntry.get() == "" or self.plistEntry.get() == "":
            tkMessageBox.showerror('Result',"input res or plist res is requested!")
            return
        info = self.scanPlist.scanPlistDir(self.outEntry.get(),self.plistEntry.get())
        tkMessageBox.showinfo('Result',info)      
        
        #----------------------------------------------------------------------
    def __map2Plist__(self):
        if self.inputentry.get() == "" or self.outEntry.get() =="" :
            tkMessageBox.showerror('Result',"input res or output res is requested!")
            return
        info = self.scanMap.scanMap(self.inputentry.get(),self.outEntry.get())
        tkMessageBox.showinfo('Result',info)
        
    #----------------------------------------------------------------------
    def __Plist2Bin__(self):
        if self.binPlistInEntry.get() =="" or self.binPlistOutEntry.get() == "" :
            tkMessageBox.showerror('Result',"bin input res or bin output res is requested!")
            return
        info = self.scanPlistToBin.sacnPlist2Bin(self.binPlistInEntry.get() , self.binPlistOutEntry.get())
        tkMessageBox.showinfo('Result', info)

def main():
    tool = ToolGui()

if __name__ == "__main__": 
    main()