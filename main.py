#!/usr/bin/env python3
from sims import Sim

traits = {'age':24,'gender':'m','hair':'brown','skin_tone':2,'weight':6,'height':176}
ellie_traits = {'age':22,'gender':'f','hair':'black','skin_tone':1,'weight':4,'height':150}
my_sim = Sim(name='liam', traits=traits)
ellie = Sim(name='ellie', links={'partner':'liam'}, traits=ellie_traits)
print(my_sim.name)
print(my_sim.age)
print(my_sim.hair)
print(ellie.name)
print(my_sim.links)
print(ellie.links)
print(my_sim.partner)
print(ellie.partner)
