#!/usr/bin/env python
# coding: utf-8

# # SETUP

# ## imports

# In[39]:


import string
import numpy as np
from itertools import cycle
import requests
import collections
from pprint import pprint
import operator


# ## constants

# In[40]:


lowercase=string.ascii_lowercase

# ## helpers

# In[41]:


def get_level_input(lvl_num):
    with open('advent_inputs/%d.txt' %lvl_num) as f:
        level_input=f.read()
        return level_input[:-1]
    
def print_result(answer):
    pprint("RESULT: "+str(answer))
    print()
    pprint("TIME"+"."*60)
    
class StopExecution(Exception):
    def _render_traceback_(self):
        pass

# # LEVEL 1

# ## setup

# In[42]:


frequencies=get_level_input(1)
frequencies=frequencies.splitlines()
frequencies=[int(x[1:]) if x[0]=='+' else int(x) for x in frequencies]

# ## part one

# In[43]:


%%time
print_result(sum(frequencies))

# ## part two

# In[44]:


%%time
y=set({})
current_sum = 0
for i in cycle(frequencies):
    current_sum+=i
    if current_sum in y:
        print_result(current_sum)
        break
    else:
        y.add(current_sum)

# # LEVEL 2

# ## setup

# In[45]:


input_boxes=get_level_input(2)
input_boxes=input_boxes.split('\n')
count_boxes = [collections.Counter(a) for a in input_boxes]

# ## part one

# In[46]:


%%time
twos=0
threes=0
for box_id in count_boxes:
    if 2 in box_id.values():
        twos+=1
    if 3 in box_id.values():
        threes+=1
print_result(str(twos*threes))

# ## part two

# In[47]:


%%time
for i, box_one in enumerate(input_boxes):
    for box_two in input_boxes[i+1:]:
        diff=0
        wrong_letter_index=0
        for j in range(len(box_one)):
            if box_one[j]==box_two[j]: continue
            diff+=1
            wrong_letter_index=j
            if(diff>1): break
        if(diff==1): 
            print_result(box_one[:wrong_letter_index]+box_one[wrong_letter_index+1:])
            raise StopExecution     

# # LEVEL 3

# ## setup

# In[48]:


fabric_list=get_level_input(3).splitlines()
fabric_list=[x.split(" ") for x in fabric_list]

# ## part one

# In[49]:


%%time
fabric=np.zeros((1000,1000))
for i in fabric_list:
    dim=tuple([int(z) for z in i[2][:-1].split(",")])
    size=tuple([int(z) for z in i[3].split("x")])
    fabric[dim[0]:dim[0]+size[0],dim[1]:dim[1]+size[1]]+=1
    NUM_SINGLE_USED=(fabric > 1).sum()
print_result(NUM_SINGLE_USED)

# ## part two

# In[50]:


%%time
for i in fabric_list:
    dim=tuple([int(z) for z in i[2][:-1].split(",")])
    size=tuple([int(z) for z in i[3].split("x")])
    if((fabric[dim[0]:dim[0]+size[0],dim[1]:dim[1]+size[1]]==1).all()):
        print_result(i[0])

# # LEVEL 4

# ## setup

# In[51]:


guards = get_level_input(4)
guards = guards.splitlines()
guards.sort()
guards = [[x[0][-2:], x[1][1:]] for x in [j.split(']') for j in guards]]

# ## part one

# In[52]:


%%time

cur_guard=0
guard_to_min={}
for i, log in enumerate(guards):
    if(log[1][0]=='G'):
        cur_guard=int(log[1].split(" ")[1][1:])
        if cur_guard not in guard_to_min.keys():
            guard_to_min[cur_guard]=np.zeros(60)
    elif(log[1][0]=='f'):
        if(int(log[0])<int(guards[i+1][0])):
            guard_to_min[cur_guard][int(log[0]):int(guards[i+1][0])]+=1
        else:
            guard_to_min[cur_guard][int(log[0]):]+=1
            guard_to_min[cur_guard][:int(guards[i+1][0])]+=1
m = max([sum(v) for v in guard_to_min.values()])

for key,value in guard_to_min.items():
    if( m==sum(value)):
        print_result(list(value).index(max(value))*key)

# ## part two

# In[53]:


%%time

cur_guard=0
guard_to_min={}
for i, log in enumerate(guards):
    if(log[1][0]=='G'):
        cur_guard=int(log[1].split(" ")[1][1:])
        if cur_guard not in guard_to_min.keys():
            guard_to_min[cur_guard]=np.zeros(60)
    elif(log[1][0]=='f'):
        if(int(log[0])<int(guards[i+1][0])):
            guard_to_min[cur_guard][int(log[0]):int(guards[i+1][0])]+=1
        else:
            guard_to_min[cur_guard][int(log[0]):]+=1
            guard_to_min[cur_guard][:int(guards[i+1][0])]+=1
m = max(i for v in guard_to_min.values() for i in v)

for key,value in guard_to_min.items():
    if( m in value ):
        print_result(list(value).index(m)*key)

# # LEVEL 5

# ## setup

# In[54]:


polymers=get_level_input(5)

# ## part one

# In[55]:


%%time
polymer_temp=polymers
i=0
while i!=len(polymer_temp)-1:
    if(abs(ord(polymer_temp[i])-ord(polymer_temp[i+1]))==32):
        polymer_temp=polymer_temp[0:i]+polymer_temp[i+2:]
        i=max(0,i-1)
    else:
        i+=1
print(len(polymer_temp))

# ## part two

# In[56]:


%%time
scores=[]
for letter in lowercase:
    polymer_temp=polymers
    i=0
    polymer_temp=polymer_temp.translate(str.maketrans('', '', letter+letter.upper()))
    while i!=len(polymer_temp)-1:
        if(abs(ord(polymer_temp[i])-ord(polymer_temp[i+1]))==32):
            polymer_temp=polymer_temp[0:i]+polymer_temp[i+2:]
            i=max(0,i-1)
        else:
            i+=1
    scores.append(len(polymer_temp))
print_result(min(scores))

# # LEVEL 6

# ## setup

# In[61]:


coords=get_level_input(6)
coords=set([tuple([int(coord.split(", ")[0]), int(coord.split(", ")[1])]) for coord in coords.splitlines()])
print((coords))

def l1(c1, c2):
    return abs(c1[0]-c2[0])+abs(c1[1]-c2[1])
GRID_SIZE=1000

# In[74]:


# TEST_COORDS
coords= set([(1, 1),(1, 6),(8, 3),(3, 4),(5, 5),(8, 9)])
GRID_SIZE=10
print(coords)

# ## part one

# ### thoughts
# 
# - Need to determine which areas are infinite
#     - are these automatically the points that have the lowest or highest x or y coordinate?
# - Need to limit scope and calculate each grdp points relation to our coordinates
# - Assign the minimum distance to a points area score
# - Pick the point that has the minimum area score that is not infiinite
# 
# ### EPIPHANY
# CHANGING THE SIZE OF THE GRID WILL NOT CHANGE THE NUMBER OF RESULTS FOR NON-INFINITE OPTIONS. THIS CAN ONLY BE THE CASE FOR NON INF OPTIONS SO TRY TWO GRIDS ONE OF SMALL SIZE, ONF OF LARGER SIZE AND CHOOSE MAX VALUE THAT DOESN"T CHANGE.
# 
# **NOTE**: the grid size must expand in all directions for this method to work. This means points need to be recentered
# 
# 

# In[112]:


def get_index_min_l1(pos):
    coord_min=[]
    for coord in coords:
        coord_min.append(l1(coord, pos))
    x=np.where(np.array(coord_min) == np.array(coord_min).min())
    if(len(x[0])>1): return -1
    return x[0]

test_grid = np.zeros((GRID_SIZE,GRID_SIZE))
for i, coord in enumerate(coords):
    test_grid[coord[0], coord[1]]=i+1
pprint([list(i) for i in zip(*test_grid)])
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        test_grid[i][j]=get_index_min_l1((i,j))+1
print()
pprint([list(i) for i in zip(*test_grid)])

# ## part two

# In[77]:


%%time
scores=[]
for letter in lowercase:
    polymer_temp=polymers
    i=0
    polymer_temp=polymer_temp.translate(str.maketrans('', '', letter+letter.upper()))
    while i!=len(polymer_temp)-1:
        if(abs(ord(polymer_temp[i])-ord(polymer_temp[i+1]))==32):
            polymer_temp=polymer_temp[0:i]+polymer_temp[i+2:]
            i=max(0,i-1)
        else:
            i+=1
    scores.append(len(polymer_temp))
print_result(min(scores))

# In[ ]:



