import time

class Population:
    def __init__(self, first_generation:tuple|list, method:int):
        """
        Generator class for making a Population using wolfram code.
        """
        self.generations = [tuple(first_generation)]
        self.method = method
        self.stop_iteration = False

    def __iter__(self):
        return self

    def __next__(self):
        current_generation, new_generation = self.generations[-1][:], []
        method_bin = bin(self.method)[2:]
        while len(method_bin) < 8:
            method_bin = '0' + method_bin

        for i in range(len(current_generation)):
            if i-1 < 0:
                new = ''.join(map(str, (0, 
                                        current_generation[i], 
                                        current_generation[i+1])))
                surrounding = (0, current_generation[i], current_generation[i+1])
            elif i+1 >= len(current_generation):
                new = ''.join(map(str, (current_generation[i-1], 
                                        current_generation[i], 
                                        0)))
                surrounding = (current_generation[i-1], current_generation[i], 0)
            else:
                new = ''.join(map(str, (current_generation[i-1], 
                                        current_generation[i], 
                                        current_generation[i+1])))
                surrounding = (current_generation[i-1], current_generation[i], current_generation[i+1])
            
            new = int(new, 2)
            no = (-1-new, int(method_bin[-1-new]))
            new_generation.append(int(method_bin[-1-new]))

        new_generation = tuple(new_generation)
        if 1 not in current_generation or self.stop_iteration == True:
            raise StopIteration

        self.generations.append(new_generation)

        return new_generation

    def __len__(self):
        return len(self.generations)

    def __repr__(self):
        return '\n'.join([''.join(map(str, generation)) for generation in self.generations])
    
    def pop(self):
        return self.generations.pop()

    def stop_iteration(self):
        self.stop_iteration = True

    def resume_iteration(self):
        self.stop_iteration = False

def file_it_all():
    signs = (' ', '1')

    for wolfram_code in range(256):
        m = 81 ##generations' size

        ##FIRST GENERATION
        states = [1 for i in range(m)]
        #states[m//2] = 1

        pop = Population(states, wolfram_code)

        ##FILING
        population_file = open(f'populations\\one-dimentional\\all-alive\\population-{m}-{wolfram_code}.txt', 'w')
        population_file_content = f'wolfram: {wolfram_code}\n\nneighbourhood:\t'

        for i in range(8):
            b = bin(7-i)[2:].rjust(3, '0')
            population_file_content += b + ' '

        wolfram_bin = bin(wolfram_code)[2:].rjust(8, '0')
        population_file_content += '\nnew generation:\t '+'   '.join(wolfram_bin)+'\n\n'

        population_file_content += '1'.rjust(5)+': ' + str(pop) + '\n'
        try:
            for p in pop:
                if len(pop) > 10000:
                    raise KeyboardInterrupt
                population_file_content += str(len(pop)).rjust(5)+': '+''.join(signs[cell] for cell in p) + '\n'
                #time.sleep(0.2)
        except KeyboardInterrupt:
            pass
        
        #print(population_file_content)
        population_file.write(population_file_content)
        population_file.close()

def run_in_terminal():
    ##wolfram's code
    ## it's binary representation is a rule of creating the new generation from the previous one
    wolfram = 90

    for i in range(8):
        b = bin(7-i)[2:].rjust(3, '0')
        print(b, end=' ')

    ##printing new generations' creation method
    ## (numbers from 7 to 0 in binary - depictiong possible neighbourhoods in the previous generationg)
    ## (corresponding digits in wolfram's code binary representation - new unit created from previous neighbourhood)
    wolfram_bin = bin(wolfram)[2:].rjust(8, '0')
    print('\n '+'   '.join(wolfram_bin) +'\n')

    ##setting the FIRST GENERATION
    m = 81
    first_generation = [0 for i in range(m)]
    first_generation[m//2] = 1

    ##signs representing dead and alive (correspondingly) units
    signs = (' ', '1')

    pop = Population(first_generation, wolfram)
    
    ##printing the first generation
    print('1'.rjust(5)+': '+str(pop))
    for p in pop:
        ##(pretty) lines indexing        +       new generation printing
        print(str(len(pop)).rjust(5)+': '+''.join(signs[cell] for cell in p))
        time.sleep(0.2)

def main():
    """ wolfram = 90
    
    for i in range(8):
        b = bin(7-i)[2:].rjust(3, '0')
        print(b, end=' ')

    wolfram_bin = bin(wolfram)[2:].rjust(8, '0')
    print('\n '+'   '.join(wolfram_bin))

    m = 81
    states = [0 for i in range(m)]
    states[m//2] = 1

    signs = (' ', '1')
    pop = Population(states, wolfram)
    
    print('1'.rjust(5)+': '+str(pop))
    for p in pop:
        #if len(pop) > 150 and len(pop) < 300:
            print(str(len(pop)).rjust(5)+': '+''.join(signs[cell] for cell in p))
            time.sleep(0.2) """
    
    run_in_terminal()

if __name__ == "__main__":
    main()
    #file_it_all()