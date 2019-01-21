# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:26:38 2019

@author: Xingguang Zhang
"""

import wx
import wx.xrc
import cv2

##################################################################################################
## Class AnnoCheckTool
## Framework code generated with wxFormBuilder : http://www.wxformbuilder.org/
## You need python3 and wxPython, opencv-python module
## wxPython module: pip install wxPython
## The size of display area can be modified by setting VideoDisplaySize parameter in main function
## 
## Steps for using this tool:
## Check if the annotation and video file share the same path. They must be in the same path.
## Run this .py file, after entering the GUI successfully, press "load video" button.
## Select an .avi video, for other format, you need to change 
##		self.wildcard='Video Files(*.avi)|*.avi|All Files(*.*)|*.*'   
##      above two avi to another video format that opencv supports.
## Double click the target annotation, then the corresponding video slice will be played.
## If an annotation is selected and checked, press "Write to File" will add an check record to the 
## corresponding record file naming "(video name)_annotCheck.txt".
## The format of a record is annotation + Y/N + comment (the comment or note is alternative).  
## Before closing the window, you'd better pause the video.
##################################################################################################

class AnnoCheckTool ( wx.Frame ):
	
	def __init__( self, parent, VideoDisplaySize ):
        
		self.WindowWidth = VideoDisplaySize[0] + 440
		self.WindowHeight = VideoDisplaySize[1] + 190        
		self.ImWidth = VideoDisplaySize[0]
		self.ImHeight = VideoDisplaySize[1]
		self.wildcard='Video Files(*.avi)|*.avi|All Files(*.*)|*.*'        
		self.Annotation = []
		self.AnnoMark = []
		self.AnnoFilePath = ''  
		self.PausePoint = 4000
        
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, \
                     size = wx.Size(self.WindowWidth, self.WindowHeight ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
        
		bSizer1 = wx.BoxSizer( wx.VERTICAL )	
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer2.SetMinSize( wx.Size( -1,20 ) ) 
		self.m_load = wx.Button( self, wx.ID_ANY, u"Load Video", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_load, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.Inform_bar = wx.TextCtrl( self, wx.ID_ANY, u"Information is shown here", \
                                wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTRE|wx.TE_READONLY )
		self.Inform_bar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer2.Add( self.Inform_bar, 3, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
				
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"PlayVideo" ), wx.VERTICAL )		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap = wx.StaticBitmap( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, \
                                  wx.DefaultPosition, wx.Size( 960,540 ), 0 )
		bSizer4.Add( self.m_bitmap, 0, wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5.SetMinSize( wx.Size( 210,-1 ) ) 
		self.m_staticText = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, \
                                    u"Choose Annotation :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText.Wrap( -1 )
		bSizer5.Add( self.m_staticText, 0, wx.ALL, 5 )
		
		m_listBoxChoices = []
		self.m_listBox = wx.ListBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, \
                              wx.Size( 160,-1 ), m_listBoxChoices, wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB|wx.LB_SINGLE )
		self.m_listBox.SetFont( wx.Font( 10, 70, 90, 90, False, "Century" ) )
		self.m_listBox.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer5.Add( self.m_listBox, 8, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, \
                                     u"Add comment/note(No need):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer5.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_Comment = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, \
                                wx.DefaultPosition, wx.Size( 180,-1 ), wx.TE_CENTRE )
		self.m_Comment.SetFont( wx.Font( 13, 70, 90, 90, False, "Century" ) )
		self.m_Comment.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		self.m_Comment.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		self.m_Comment.SetMinSize( wx.Size( 180,-1 ) )
		self.m_Comment.SetMaxSize( wx.Size( 180,-1 ) )
		
		bSizer5.Add( self.m_Comment, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		m_radioBoxChoices = [ u"Agree(Y)", u"Disagree(N)" ]
		self.m_radioBox = wx.RadioBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Agree or Disagree", \
                                wx.DefaultPosition, wx.DefaultSize, m_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.m_radioBox.SetSelection( 0 )
		bSizer5.Add( self.m_radioBox, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_Write = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Write To File", \
                           wx.Point( -1,-1 ), wx.Size( 160,30 ), 0 )
		self.m_Write.SetMinSize( wx.Size( 160,30 ) )
		self.m_Write.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer5.Add( self.m_Write, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Checked annotations" ), wx.VERTICAL )
		
		sbSizer2.SetMinSize( wx.Size( 210,-1 ) ) 
		self.AnnotationArea = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, \
                                    wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		self.AnnotationArea.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Calibri" ) )
		
		sbSizer2.Add( self.AnnotationArea, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_delete = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, \
                            u"Delete Last Record", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.m_delete, 0, wx.ALL|wx.EXPAND, 5 )
				
		bSizer4.Add( sbSizer2, 1, wx.EXPAND, 5 )		
		sbSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )		
		bSizer1.Add( sbSizer3, 15, wx.EXPAND, 5 )		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5.SetMinSize( wx.Size( -1,50 ) ) 
		self.m_slider = wx.Slider( self, wx.ID_ANY, 0, 0, 4000, wx.DefaultPosition, wx.Size( -1,40 ), wx.SL_LABELS|wx.SL_TOP )
		self.m_slider.SetMinSize( wx.Size( -1,30 ) )
		self.m_slider.SetMaxSize( wx.Size( -1,50 ) )
		
		bSizer5.Add( self.m_slider, 1, wx.ALL|wx.EXPAND, 5 )		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )		
		bSizer6.SetMinSize( wx.Size( -1,20 ) ) 
		self.m_buttonSlow = wx.Button( self, wx.ID_ANY, u"0.5X", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer6.Add( self.m_buttonSlow, 1, wx.ALL, 5 )
		
		self.m_buttonBefore = wx.Button( self, wx.ID_ANY, u"Last Frame", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer6.Add( self.m_buttonBefore, 1, wx.ALL, 5 )
		
		self.m_toggleBtn = wx.ToggleButton( self, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer6.Add( self.m_toggleBtn, 2, wx.ALL, 5 )
		
		self.m_buttonNext = wx.Button( self, wx.ID_ANY, u"Next Frame", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer6.Add( self.m_buttonNext, 1, wx.ALL, 5 )
		
		self.m_buttonFast = wx.Button( self, wx.ID_ANY, u"2X", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer6.Add( self.m_buttonFast, 1, wx.ALL, 5 )		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )		
		bSizer1.Add( bSizer5, 0, wx.EXPAND, 5 )		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_load.Bind( wx.EVT_BUTTON, self.OnLoad )
		self.m_listBox.Bind( wx.EVT_LISTBOX, self.AnnoChosed )
		self.m_listBox.Bind( wx.EVT_LISTBOX_DCLICK, self.onDclick )
		self.m_Write.Bind( wx.EVT_BUTTON, self.AnnoCheckWrite )
		self.m_delete.Bind( wx.EVT_BUTTON, self.DeLastRecord )
		self.m_slider.Bind( wx.EVT_SCROLL, self.OnSliderScroll )
		self.m_buttonSlow.Bind( wx.EVT_BUTTON, self.OnSlow )
		self.m_buttonBefore.Bind( wx.EVT_BUTTON, self.LastFrame )
		self.m_toggleBtn.Bind( wx.EVT_TOGGLEBUTTON, self.Play_Pause )
		self.m_buttonNext.Bind( wx.EVT_BUTTON, self.NextFrame )
		self.m_buttonFast.Bind( wx.EVT_BUTTON, self.OnFast )
		self.Bind( wx.EVT_TIMER, self.OnTime, id=wx.ID_ANY )

		self.m_toggleBtn.Bind( wx.EVT_KEY_DOWN, self.KeyboardEvent )
		self.m_buttonNext.Bind( wx.EVT_KEY_DOWN, self.KeyboardEvent )
		self.m_buttonBefore.Bind( wx.EVT_KEY_DOWN, self.KeyboardEvent )
		self.Bind( wx.EVT_KEY_DOWN, self.KeyboardEvent )	
        
        #Set flags
		self.PAUSE_FLAG = False
		self.PROCESSING_FLAG = False	
		self.SELECTED_FLAG = False	
    
	def __del__( self ):
		self.m_timer1.Stop()
		pass	
	
	# Virtual event handlers, overide them in your derived class
	def OnLoad( self, event ):
		dlg = wx.FileDialog(self, message='Open Video File', 
                            defaultDir='',
                            defaultFile='', 
                            wildcard = self.wildcard, 
                            style = wx.FD_OPEN)
        
		if dlg.ShowModal() == wx.ID_OK:
		    self.PROCESSING_FLAG = True
		    video_path = dlg.GetPath()
		    dlg.Destroy()  
		    self.videoCapture = cv2.VideoCapture(video_path)
		    if(self.videoCapture == None):
		        wx.SafeShowMessage('start', 'Open Failed')
		        return
		    self.TotalFrame = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
		    self.PausePoint = self.TotalFrame
		    self.m_slider.SetMax(int(self.TotalFrame))
		    self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
		    self.FrameTime = 1000 / self.fps
		    self.m_timer1.Start(self.FrameTime)
		    self.Inform_bar.SetValue('Video Loaded : ' + video_path)
		    self.LoadAnnot(video_path)
    
	def AnnoChosed( self, event ):
		self.SELECTED_FLAG = True
		event.Skip()
	
	def onDclick( self, event ):
		if self.SELECTED_FLAG:
		    AnnoInd = self.m_listBox.GetSelections()
		    Selected = self.m_listBox.GetString(AnnoInd[0])
		    SeList = Selected.split(' ')
		    self.FrameNumber = int(SeList[0])
		    self.PausePoint = int(SeList[1])
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.FrameNumber)
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success):
		        self.MyImshow()
		    print(SeList)
		event.Skip()
	
	def AnnoCheckWrite( self, event ):
		if self.SELECTED_FLAG:
		    AnnoInd = self.m_listBox.GetSelections()
		    Selected = self.m_listBox.GetString(AnnoInd[0])
		    RadioInd = self.m_radioBox.GetSelection()
		    IsAgree = 'N' if RadioInd else 'Y'
		    Comment = self.m_Comment.GetLineText(0)
		    if Comment:
		        OneAnnoCheck = Selected + ' ' + IsAgree + ' ' +  Comment + '\n'   
		    else:
		        OneAnnoCheck = Selected + ' ' + IsAgree + '\n'
                
		    if OneAnnoCheck not in self.AnnoMark:
		        self.AnnoMark.append(OneAnnoCheck)  
		    else:
		        self.Inform_bar.SetValue('The record has been added, do not add again!')      
		    self.MyFileWriting(str(self.AnnoFilePath[0]) + '_annotCheck.txt')  
		    self.DisplayAnnotCheck()
		else:
		    self.Inform_bar.SetValue('Please select an annotation!')
		event.Skip()

    # delete the last annotation record	
	def DeLastRecord( self, event ):
		if self.AnnoMark:
		    self.AnnoMark.pop()
		    self.MyFileWriting(str(self.AnnoFilePath[0]) + '_annotCheck.txt')
		    self.DisplayAnnotCheck()
		else:
		    self.Inform_bar.SetValue('No record can be deleted!')
		event.Skip()
	
    # when the slider is used, set new framenumber and display the corresponding image
	def OnSliderScroll( self, event ):
		if self.PROCESSING_FLAG:
		    self.FrameNumber = self.m_slider.GetValue()
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.FrameNumber)
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success):
		        self.MyImshow()
		else:
		    event.Skip()
	
    # display the last frame
	def LastFrame( self, event ):
		try:
		    self.FrameNumber -= 1
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES , self.FrameNumber)
		except AttributeError:
		    self.Inform_bar.SetValue('Please load the video!')
		else:
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success) :
		        self.MyImshow()
		event.Skip()
	
    # toggle the playing and pausing condition of the video
	def Play_Pause( self, event ):
		if self.PROCESSING_FLAG:
		    self.PAUSE_FLAG = event.GetEventObject().GetValue()
		    if self.PAUSE_FLAG:
		        self.m_timer1.Stop()
		        event.GetEventObject().SetLabel("Play")
		    else:
		        self.m_timer1.Start(self.FrameTime)
		        event.GetEventObject().SetLabel("Pause")
		else:
		    self.Inform_bar.SetValue('Please load the video!')
		event.Skip()
	
	def NextFrame( self, event ):
		try:
		    self.FrameNumber += 1
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES , self.FrameNumber)
		except AttributeError:
		    self.Inform_bar.SetValue('Please load the video!')
		else:
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success) :
		        self.MyImshow()
		event.Skip()
    
    # slow down the fps to a half
	def OnSlow( self, event ):
		if self.FrameTime <= 200:
		    self.FrameTime = self.FrameTime * 2
		    if not self.PAUSE_FLAG: self.m_timer1.Start(self.FrameTime)
		    self.Inform_bar.SetValue('Current fps:' + str(1000/self.FrameTime))
		else:
		    self.Inform_bar.SetValue('Minimum fps reached!')
		event.Skip()	
	
    # set the fps doubly
	def OnFast( self, event ):
		if self.FrameTime >= 10:
		    self.FrameTime = self.FrameTime * 0.5
		    if not self.PAUSE_FLAG: self.m_timer1.Start(self.FrameTime)
		    self.Inform_bar.SetValue('Current fps:' + str(1000/self.FrameTime))
		else:
		    self.Inform_bar.SetValue('Maximum fps reached!')
		event.Skip()
	
	def KeyboardEvent( self, event ):
		keycode = event.GetKeyCode()
		if keycode in [wx.WXK_LEFT, wx.WXK_RIGHT] and self.PROCESSING_FLAG:
		    self.FrameNumber = self.FrameNumber - 1 if keycode == wx.WXK_LEFT else self.FrameNumber + 1
		    self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES , self.FrameNumber)
		    success, self.CurrentFrame = self.videoCapture.read()
		    if(success):
		        self.MyImshow()
		event.Skip()
        
	def OnTime( self, event ):
		if self.PROCESSING_FLAG:
		    success, self.CurrentFrame = self.videoCapture.read()
		    self.FrameNumber = self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES)
		    if(success):
		        self.MyImshow()
		else:
		    event.Skip()

	def MyImshow(self):
		if int(self.FrameNumber) == self.PausePoint+1:
		    self.m_timer1.Stop()
		    self.m_toggleBtn.SetValue(1)
		    self.m_toggleBtn.SetLabel(("Play"))
		else:
		    self.CurrentFrame = cv2.resize(self.CurrentFrame, (self.ImWidth, self.ImHeight), interpolation = cv2.INTER_CUBIC)
		    image = cv2.cvtColor(self.CurrentFrame, cv2.COLOR_BGR2RGB)
		    pic = wx.Bitmap.FromBuffer(self.ImWidth, self.ImHeight, image) 
		    self.m_bitmap.SetBitmap(pic)
		    self.m_slider.SetValue(int(self.FrameNumber))

	def LoadAnnot(self, vpath):
		self.AnnoFilePath = vpath.split('.')
		fpath = self.AnnoFilePath[0] + '_annot.txt'
		if self.Annotation:
		    for annot in self.Annotation:
		        self.m_listBox.Delete(0)
		    self.Annotation = []           
		try:
		    f = open(fpath, 'r')
		except FileNotFoundError:
		    self.Inform_bar.SetValue("File " + fpath + " is Not Found")
		else:
		    for line in f.readlines():
		        self.Annotation.append(line.strip())
		    f.close()
		if self.Annotation:
		    self.m_listBox.InsertItems(self.Annotation, 0)
		else:
		    self.Inform_bar.SetValue("Annotation is empty!")

	def MyFileWriting(self, write_path):
		f = open(write_path, 'w')
		for item in self.AnnoMark:
		    f.write(item)
		f.close()
        
	def DisplayAnnotCheck(self):
		self.AnnotationArea.Clear()
		for item in self.AnnoMark:
		    self.AnnotationArea.AppendText(item)
            
if __name__ =='__main__':
    # The size of display area and the path of video file, the annotation file will be in the same dictionary will the video file
    VideoDisplaySize = [960, 540] #For Taurus
#    VideoDisplaySize = [960, 700] #For Taurus Simulator  
    app = wx.App()
    frame = AnnoCheckTool(None, VideoDisplaySize)
    frame.Show()
    app.MainLoop()
    del app