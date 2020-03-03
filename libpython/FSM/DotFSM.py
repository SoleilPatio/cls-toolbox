import re

"""
[Rule]:
    1. 1st node in .dot is initial node
    2. node with no transition regards end
"""

class DotFSM(object):

    def __init__(self):
        """
        FSM[src] = [
                    (dest1, criteria1={function:'f1' , ...} ),
                    (dest1, criteria2={function:'f2' , ...} ),
                    .
                    .
                    ]
        
        """
        self.FSM = {}
        self.current_state = None
        self.init_state = None
        self.is_finish = False
        
        
        
    def __str__(self):
        ret_strs = ["\n"] 
        ret_strs.append(str(type(self))+":")
        ret_strs.append("\tcurrent_state = %s" % self.current_state)
        ret_strs.append("\t-----------------------")
        
        for src in self.FSM:
            ret_strs.append("\t"+src)
            for dest,criteria in self.FSM[src]:
                ret_strs.append( "\t\t-> " + dest + " " + str(criteria))

            ret_strs.append("\t-----------------------")
        
        return "\n".join(ret_strs)


    def reset_state(self):
        self.current_state = self.init_state
        self.is_finish = False
        #==> Call the event driven callback
        on_event_call = getattr(self, "on_"+self.init_state)
        if on_event_call:
            on_event_call(None, None)
        
    
    def load_fsm_from_dot(self, dotfile):
        #info
        print "[info]: Load FSM from file : %s"%dotfile
        
        self.FSM = {}
        self.current_state = None
        self.init_state = None
        self.is_finish = False
        
        
        #src->dest [label="....."]
        trans_pattern = re.compile(r"\s+(.*)->(.*)\s+\[.*label\s*=\s*\"(.*)\"", re.M|re.I)
        #key1='vale1', key2='vale2', key3='vale3', ....
        critera_pattern = re.compile(r"\s*([^,]+)='([^,]+)'")
        
        with open(dotfile,"r") as in_file:
            for line in in_file:
                matchObj = trans_pattern.match(line)
                if matchObj:
                    src = matchObj.group(1)
                    dest = matchObj.group(2)
                    criteria_str = matchObj.group(3)
                    criteria = dict(critera_pattern.findall(criteria_str))
                    
                    if src not in self.FSM:
                        self.FSM[src] = []
                        
                    self.FSM[src].append((dest,criteria))
                    
                    print "\t- transition add: %s -> %s [%s]" % (src, dest, str(criteria))
                    
                    #1st src as initial state
                    if self.current_state == None:
                        self.current_state = src
                        self.init_state = src
                        
                        #==> Call the event driven callback
                        on_event_call = getattr(self, "on_"+src)
                        if on_event_call:
                            on_event_call(None, None)
                    
        
    
    
    def fsm_loop(self, **inputs_from_outside):
        
        """
        trans_list = [
                    (dest1, criteria1={function:'f1' , ...} ),
                    (dest1, criteria2={function:'f2' , ...} ),
                    .
                    .
                    ]
        """
        
        # ==> if this is a node without transition, indcate that it's a end
        #
        if self.current_state not in self.FSM:
            self.is_finish = True
            return
        
        trans_list = self.FSM[self.current_state]
        
        for trans in trans_list:
            dst = trans[0]
            criteria = trans[1]
            function_name = criteria["function"]
            
#             print dst, criteria, function_name
            
            function_call = getattr(self, function_name)
            if function_call == None:
                print "[ERR]:missing transition function %s" % function_name
            else:
                #==> Find the 1st "True" transition, then execute->transit->return (ignore the rest posibilities)
                #        criteria : pass the criteria for this transition
                #        kwargs : pass from ouside world of current situation
                if function_call(criteria, inputs_from_outside):
                    self.current_state = dst
                    #==> Call the event driven callback
                    #
                    #
                    on_event_call = getattr(self, "on_"+dst)
                    if on_event_call:
                        on_event_call(criteria, inputs_from_outside)
                    
                    
                    break
        
    
    #
    # [CLS]:For Test Only
    #        criteria : pass the criteria for this transition
    #        kwargs : pass from ouside world of current situation
    #
    #
    def check_if(self, criteria, inputs_from_outside):
        import numpy as np
        print "dummy check_if"
        return True if np.random.rand() > 0.5 else False
        
                    
                    


if __name__ == '__main__':
    fsm = DotFSM()
    
    fsm.load_fsm_from_dot("FSM_mmsys_isp_pass2.dot")
    
    print fsm
    
    for i in range(100):
        print "-->",fsm.current_state
        fsm.fsm_loop(v1="1",v2="2",v3="3")
    
    
    
    
    pass