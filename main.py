import math, pygame
import userinput as usrin
import matplotlib.pyplot as plt
import numpy as np
from functions import generate_sequence, assign_vectors, calc_dot_products, lerp_horizontally, lerp_vertically

matrix_side_len = usrin.grid_side_len + 1



# This is all quite a mess currently, but does the job for now... my first priority for now is the 'functions.py' file for inplementing the logic
if __name__ == "__main__":
    
    sequence = generate_sequence(matrix_side_len, usrin.octave_count, usrin.lacunarity, usrin.seed_val, usrin.psbl_vect_orients)

        
    for octave in range(usrin.octave_count):
        octave_values, sequence = assign_vectors(int(matrix_side_len * usrin.lacunarity ** octave), sequence)
        density = usrin.lacunarity ** octave
        
        data1 = calc_dot_products(octave_values, usrin.grid_side_len, usrin.chunk_side_len, usrin.psbl_vect_orients, 1, density)
        data2 = calc_dot_products(octave_values, usrin.grid_side_len, usrin.chunk_side_len, usrin.psbl_vect_orients, 2, density)
        data3 = calc_dot_products(octave_values, usrin.grid_side_len, usrin.chunk_side_len, usrin.psbl_vect_orients, 3, density)
        data4 = calc_dot_products(octave_values, usrin.grid_side_len, usrin.chunk_side_len, usrin.psbl_vect_orients, 4, density)

        lerp1 = lerp_horizontally(data1, data2, usrin.chunk_side_len, usrin.grid_side_len, density)
        lerp2 = lerp_horizontally(data3, data4, usrin.chunk_side_len, usrin.grid_side_len, density)
        
        lerp3 = lerp_vertically(lerp1, lerp2, usrin.chunk_side_len, usrin.grid_side_len, density)
        
        arr = np.array(lerp3)
        
        if octave == 0:
            data = arr
        else:
            data += arr * usrin.persistence ** octave
    
    
    
    
    
    max_val, min_val = 0, 0
    for row in data:
        if max(row) > max_val:
            max_val = max(row)
        if min(row) < min_val:
            min_val = min(row)
            
    print(min_val, max_val)
    scale = 0
    if max_val > - min_val:
        scale = max_val * 2
    else:
        scale = min_val * (-2)

    # Draw image from above in pygame
    new_data = []
    for row in data:
        new = []
        for item in row:
            new_item = item / scale + 0.5
            if new_item < 0 or new_item > 1:
                print("Error")
                print(new_item)
            new.append(new_item)
            
        new_data.append(new)
    
    x = len(data1)
    
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
    
    pygame.quit()
    
    
    
    # Show slices in matplotlib
    xpoints = []
    for i in range(len(data1[0])):
        xpoints.append(i + 1)

    current = 0

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 20))
    
    lerp_line1, = ax.plot(400, 60)
    lerp_line2, = ax.plot(0, -60)
    lerp_line3, = ax.plot(0, 0)
    
    while True:
        lerp_values_1, lerp_values_2, lerp_values_3 = [], [], []
        for i in range(len(lerp1)):
            lerp_values_1.append(lerp1[i][current])
            lerp_values_2.append(lerp2[i][current])
            lerp_values_3.append(lerp3[i][current])
        lerp_line1.set_data(xpoints, lerp_values_1)
        lerp_line2.set_data(xpoints, lerp_values_2)
        lerp_line3.set_data(xpoints, lerp_values_3)
#        line3.set_data(xpoints, data3[current])
#        line4.set_data(xpoints, data4[current])
        ax.set_title(f"Row {current + 1} of {len(data1)}")
        plt.pause(0.05)


        current +=1
        if current >= len(data1):
            current = 0