# -*- coding: utf-8 -*-

import sys
class Node:
    def __init__(self,data,level,fval):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = data
        self.level = level
        self.fval = fval
    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        x,y = self.find_blank(self.data,'_')
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. """
        val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data,x,y,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                children.append(child_node)
        return children
    
    def shuffle(self,puz,x1,y1,x2,y2):
        """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
    def copy(self,root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
                
    def find_blank(self,puz,x):
        """ Used to find the position of the blank space """
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    return i,j
class Puzzle:
    def __init__(self):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.open = []
        self.closed = []
        
    def f(self,start,goal):
            """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
            return self.h(start.data,goal)+start.level
        
    def h(self,initial_state,goal_state):
            if sys.argv[1] == '0':
                return 0
            initial_config = []
            
            for i in initial_state:
                for j in i:
                    if j == '_':
                        initial_config.append(0)
                    else:
                        initial_config.append(int(j))
            
            manDict = 0
            for i,item in enumerate(initial_config):
                prev_row,prev_col = int(i/ 3) , i % 3
                goal_row,goal_col = int(item /3),item % 3
                manDict += abs(prev_row - goal_row) + abs(prev_col - goal_col)
            return manDict


    def process(self): 
            start = []
            temp = sys.argv[2:]
            for i in range(0, 3):
                start.append(temp[i*3:(i*3)+3])
            goal = [['_', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]
            start = Node(start,0,0)
            start.fval = self.f(start,goal)
            """ Put the start node in the open list"""
            self.open.append(start)
            print("\n")
            while True:
                cur = self.open[0]
                if len(self.open) > 1:
                    print("\n* * * \n")
                    print('Level: '+str(cur.level))
                print('Heuristic: '+str(cur.fval - cur.level))
                for i in cur.data:
                    for j in i:
                        print(j,end=" ")
                    print("")
                """ If the difference between current and goal node is 0 we have reached the goal node"""
                if cur.data == goal:
                    print('Goal')
                    break
                for i in cur.generate_child():
                    i.fval = self.f(i,goal)
                    self.open.append(i)
                self.closed.append(cur)
                del self.open[0]
                self.open.sort(key = lambda x:x.fval,reverse=False)
puz = Puzzle()
puz.process()