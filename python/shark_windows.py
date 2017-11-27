#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# author dpc
   
import wx
import random
   
class cry(wx.App):
   
    def OnInit(self):
        mm = wx.DisplaySize()
        w = mm[0] / 2 + random.uniform(10, 20)
        h = mm[1] / 2 + random.uniform(10, 20)
        self.frame = wx.Frame(parent=None, title="shake windows", pos=(w, h))
         
        self.timer = wx.Timer(self)  #
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)  #
        self.timer.Start(10)
         
        self.frame.Show()
        self.frame.ToggleWindowStyle(wx.STAY_ON_TOP)
         
        return True
 
         
    def OnTimer(self, evt):  #
        #print self.frame.GetPosition()
        mm = wx.DisplaySize()
        w = mm[0] / 2 + random.uniform(10, 20)
        h = mm[1] / 2 + random.uniform(10, 20)
        self.frame.SetPosition((w, h))
        r=random.uniform(0, 255)
        g=random.uniform(0, 255)
        b=random.uniform(0, 255)
        self.frame.SetBackgroundColour((r, g, b))
         
app = cry()
app.MainLoop()