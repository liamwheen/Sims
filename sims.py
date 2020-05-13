
DEFAULT_TRAITS = {'age':25, 'gender':'m', 'hair':'brown', 'skin_tone':3, 'weight':5, 'height':175}

#States from are of the form  [amount (0 - 100), fixing (bool)]
DEFAULT_STATES = {'sleepy':[0,False], 'hungry':[0,False], 'bored':[20,False], 'horny':[0,False]} 

LINKS = ['partner', 'son', 'daughter', 'mother', 'father', 'sibling', 'friend', 'enemy']

class Sim:
    """
    Class for any living being in the Sim world
    """
    instances = []

    def __init__(self, name, links=None, traits=DEFAULT_TRAITS, states=DEFAULT_STATES):
        self.name = name
            
        # Check if input traits/states are correctly formatted - if not use defaults
        if not (all(in_key==key for in_key, key in zip(traits.keys(), DEFAULT_TRAITS.keys()))):
            print('\n---Sim traits not correctly entered - using defaults---\n')
            traits = DEFAULT_TRAITS
        if not (all(in_key==key for in_key, key in zip(traits.keys(),DEFAULT_STATES.keys()))):
            print('\n---Sim states not correctly entered - using defaults---\n')
            states = DEFAULT_STATES

        # Assign object attributes directly from dictionaries
        list(map(exec,('self.{0}="{1}"'.format(key,val) for key,val in traits.items())))
        list(map(exec,('self.{0}="{1}"'.format(key,val) for key,val in states.items())))
        
        # Handle links (if any)
        self.links = {}
        self.update_links(links)

        # Add to Class attribute list of Sims
        Sim.instances.append(self)
        
    def update_links(self, links):
        # Currently assumes max one instance of each link
        for link_type in LINKS:
            try:
                self.links[link_type] = links[link_type]
                # If link specified, create object attribute of that specific
                # case e.g. self.father = 'john'
                exec('self.{0} = "{1}"'.format(link_type, links[link_type]))
                # If link specified, look for that them and upate their links too
                for sim in Sim.instances:
                    if sim.name == links[link_type]:
                        matching_link_type = self.match_link_types(link_type)
                        sim.update_links({matching_link_type:self.name})
                        
            except KeyError:
                self.links[link_type] = None
            except TypeError:
                self.links = {}
                break

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
