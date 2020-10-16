# 
# PjSip python API wrapper class based on pjsua examples.
# 
# MIT License
# 
# Copyright (c) 2020 Dmitry Donskikh
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import pjsua as pj
import time

class simpleSipClient:
    __this_call=None
    __lib=None
    __transport=None
    __acc=None
    __self_uri=None
    call_state = pj.CallState.NULL
    # Callback to receive events from account
    class MyAccountCallback(pj.AccountCallback):
    
        def __init__(self,parent, account=None):
            pj.AccountCallback.__init__(self, account)
            self.__parent=parent
        # Notification on incoming call
        def on_incoming_call(self, call):
            
            if self.__parent.__this_call:
                call.answer(486, "Busy")
                return
                
            print "Incoming call from ", call.info().remote_uri
            print "Press 'a' to answer"
    
            self.__parent.__this_call = call
    
            call_cb = self.MyCallCallback(self.__parent, self.__parent.__this_call)
            self.__parent.__this_call.set_callback(call_cb)
    
            self.__parent.__this_call.answer(180)
            
            
    # Callback to receive events from Call
    class MyCallCallback(pj.CallCallback):
    
        def __init__(self,parent, call=None):
            pj.CallCallback.__init__(self, call)
            self.__parent=parent
    
        # Notification when call state has changed
        def on_state(self):
            print "Call with", self.call.info().remote_uri,
            print "is", self.call.info().state_text,
            print "last code =", self.call.info().last_code, 
            print "(" + self.call.info().last_reason + ")"
    
            if self.call.info().state == pj.CallState.DISCONNECTED:
                #current_call = None
                #current_call.hangup(603,"blala",None)
                #del current_call
                print "Current state: pj.CallState.DISCONNECTED\r\n"
                #current_call = CERT_NONE
            elif self.call.info().state == pj.CallState.CALLING:
                print "Current state: pj.CallState.CALLING\r\n"
            elif self.call.info().state == pj.CallState.CONFIRMED:
                print "Current state: pj.CallState.CONFIRMED\r\n"
            elif self.call.info().state == pj.CallState.CONNECTING:
                print "Current state: pj.CallState.CONNECTING\r\n"
            elif self.call.info().state == pj.CallState.EARLY:
                print "Current state: pj.CallState.EARLY\r\n"
            elif self.call.info().state == pj.CallState.INCOMING:
                print "Current state: pj.CallState.INCOMING\r\n"
            elif self.call.info().state == pj.CallState.NULL:
                print "Current state: pj.CallState.NULL\r\n"
            self.__parent.call_state = self.call.info().state   # Notification when call's media state has changed.
        
        def on_media_state(self):
            if self.call.info().media_state == pj.MediaState.ACTIVE:
                # Connect the call to sound device
                call_slot = self.call.info().conf_slot
                pj.Lib.instance().conf_connect(call_slot, 0)
                pj.Lib.instance().conf_connect(0, call_slot)
                print "Media is now active"
            else:
                print "Media is inactive"
                
                
    def __log_cb(self, level, str, len):
        print (str)
        
        
    def __init__(self):
        #self.__account_cb=self.MyAccountCallback()
        #self.__call_cb=self.MyCallCallback
        self.__lib=pj.Lib()
        self.__lib.init(log_cfg=pj.LogConfig(3,callback=self.__log_cb))
        self.__transport=self.__lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(0))
        print "\nListening on", self.__transport.info().host, 
        print "port", self.__transport.info().port, "\n"
        
        self.__lib.start(True)
        self.__acc = self.__lib.create_account_for_transport(self.__transport, cb=self.MyAccountCallback(self))
        
        self.__self_uri="sip:" + self.__transport.info().host + ":" + str(self.__transport.info().port)
    
    def wait4ready(self,timeout=-1):
        print "WAIT_4() STATE: ",self.call_state,"\r\n"
        while((self.call_state != pj.CallState.DISCONNECTED)and(self.call_state != pj.CallState.NULL)):
            if timeout==0:
                print "Timeout evet\r\n"
                return False
            time.sleep(1)
            timeout-=1
        return True
        
        
    def make_call(self, uri):
        print "MAKE_CALL() STATE: ",self.call_state,"\r\n"
        if (self.call_state == pj.CallState.DISCONNECTED)or(self.call_state == pj.CallState.NULL):
            try:
                print "Making call to" , uri
                self.__this_call=self.__acc.make_call(uri, cb=self.MyCallCallback(self))
                return True
            except pj.Error, e:
                print "Exception: " + str(e)
                return None
        else:
            print "Wrong state!!!: ", self.call_state
            return False
    
    def hang(self):
        print "HANG() STATE: ",self.call_state ,"\r\n"
        if (self.call_state == pj.CallState.DISCONNECTED)or(self.call_state == pj.CallState.NULL):
            return True
        else:
            self.__this_call.hangup()
            return self.wait4ready(60)
    
    def getSelfURI(self):   
        print "GET_URI() STATE: ",self.call_state,"\r\n"
        return self.__self_uri
    
        
        
        
        
        
        
        
        