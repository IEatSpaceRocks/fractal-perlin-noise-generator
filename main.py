import math, pygame
import userinput as usrin
from functions import generate_sequence, assign_vectors, calc_dot_products

matrix_side_len = usrin.grid_side_len + 1



# This is all quite a mess currently, but does the job for now... my first priority for now is the 'functions.py' file for inplementing the logic
if __name__ == "__main__":
    
    sequence = generate_sequence(matrix_side_len, usrin.octave_count, usrin.lacunarity, usrin.seed_val, usrin.psbl_vect_orients)
    print(sequence)
    
    for i in range(usrin.octave_count):
        octave, sequence = assign_vectors(int(matrix_side_len * usrin.lacunarity ** i), sequence)
        print()
        for row in octave:
            print(row)
        print()
        print(sequence)

    data = calc_dot_products(octave, usrin.grid_side_len, usrin.chunk_side_len, usrin.psbl_vect_orients, 4)



    new_data = []
    max, min = 0, 0
    for row in data:
        new = []
        for item in row:
            if item < min:
                min = item
            if item > max:
                max = item
            new_item = item / (usrin.chunk_side_len * 2 * math.sqrt(2)) + 0.5
            if new_item < 0 or new_item > 1:
                print("Error found")
                print(new_item)
            new.append(new_item)
            
        new_data.append(new)
        
    print(min, max)

    x = len(data[0])
    print(x)

    pygame.init()
    screen = pygame.display.set_mode((x, x))
    pygame.display.set_caption("Perlin Noise") 

    running = True
    while running:
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
        for i in range(x):
            for j in range(x):
                colour = ((255 * new_data[i][j], 255 * new_data[i][j], 255 * new_data[i][j]))
                pygame.draw.rect(screen, colour, (j, i, 1, 1))
                
        pygame.display.flip()
        pygame.time.Clock().tick(20)
    