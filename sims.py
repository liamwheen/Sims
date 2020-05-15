from itertools import chain

DEFAULT_TRAITS = {'age':25, 'gender':'m', 'hair':'brown', 'skin_tone':3, 'weight':5, 'height':175}

#States from are of the form  [amount (0 - 100), fixing (bool)]
DEFAULT_STATES = {'sleepy':[0,False], 'hungry':[0,False], 'bored':[20,False], 'horny':[0,False]} 

LINKS = ['partner', 'son', 'daughter', 'mother', 'father', 'sibling', 'friend', 'enemy']

class Sim:
    """
    Class for any living being in the Sim world
    """
    instances = []

    def __init__(self, name, links={}, traits=DEFAULT_TRAITS, states=DEFAULT_STATES):
        self.name = name
            
        # Check if input traits/states are correctly formatted - if not use defaults
        if not (all(in_key==key for in_key, key in zip(traits.keys(), DEFAULT_TRAITS.keys()))):
            print('\n---Sim traits not correctly entered - using defaults---\n')
            traits = DEFAULT_TRAITS
        if not (all(in_key==key for in_key, key in zip(states.keys(),DEFAULT_STATES.keys()))):
            print('\n---Sim states not correctly entered - using defaults---\n')
            states = DEFAULT_STATES

        # Assign object attributes directly from dictionaries
        list(map(exec,('self.{0}="{1}"'.format(key,val) for key,val in traits.items())))
        list(map(exec,('self.{0}="{1}"'.format(key,val) for key,val in states.items())))
        
        # Add to Class attribute list of Sims
        Sim.instances.append(self)

        # Handle links (if any)
        self.links = {}
        self.update_links(links)
        
    def update_links(self, links):
        
        for link_type in links.keys():
            if link_type not in LINKS:
                print('\n---Link ({}) is not in the correct form---\n'.format(link_type))
                continue

            new_links = [links[link_type]] if isinstance(links[link_type],str) else links[link_type]

            try:
                self.links[link_type] += new_links
                # Remove duplicates if any
                self.links[link_type]  = list(dict.fromkeys(self.links[link_type]))
                # If link specified, create object attribute of that specific
                # case e.g. self.father = 'john'
            except KeyError:
                # Link type did not exist already
                self.links[link_type] = new_links
                # Remove duplicates if any
                self.links[link_type]  = list(dict.fromkeys(self.links[link_type]))
            
            exec('self.{0} = "{1}"'.format(link_type, self.links[link_type]))

            # Update new links so they are linked to self
            for link in new_links:
                if link in self.get_instances('names'):
                    matching_link_type = self.match_link_types(link_type)
                    linked_sim = self.get_sim_by_name(link)
                    try:
                        # Make sure new link is not already linked to self
                        if self.name not in linked_sim.links[matching_link_type]:
                            linked_sim.update_links({matching_link_type:self.name})
                    except KeyError:
                        linked_sim.update_links({matching_link_type:self.name})

        # Check if other sims have already specified link to self
        for sim in self.get_instances():
            if self.name in chain.from_iterable(sim.links.values()) and\
            sim.name not in chain.from_iterable(self.links.values()):
                sim.update_links(sim.links)


    def match_link_types(self, link_type):
        # Produce matched link from other side's perspectives
        if link_type not in ['son', 'daughter', 'mother', 'father']:
            return link_type
        if link_type in ['mother', 'father']:
            if self.gender == 'm': return 'son'
            return 'daughter'
        if link_type in ['son', 'daughter']:
            if self.gender == 'm': return 'father'
            return 'mother'
    
        raise TypeError('Link type is incorrect')

    def get_instances(self, names=False):
        if not names: return Sim.instances
        return [sim.name for sim in Sim.instances]

    def get_sim_by_name(self, name):
        for sim in self.get_instances():
            if sim.name == name: return sim
        print('\n---Sim name is not recognised---\n')
        return 0


