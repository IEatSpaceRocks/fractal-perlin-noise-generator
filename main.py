import pygame, numpy
from functions import generate_array, assign_vectors, get_dot_products, lerp_horizontally, lerp_vertically, get_colour
from userinput import seed_value, chunk_side_length, grid_side_length, octave_count, lacunarity, persistence, possible_vector_orientations



if __name__ == "__main__":
    
    array = generate_array(grid_side_length, octave_count, lacunarity, seed_value, possible_vector_orientations)

    for current_octave_index in range(octave_count):
        
        density = lacunarity ** current_octave_index    # Each octave has a different density
        current_matrix_side_length = (grid_side_length + 1) * density
        current_grid_side_length = grid_side_length * density              # The denser the grid, the more vertices there are on it...
        current_chunk_side_length = chunk_side_length / density            # ...the denser the vertices are placed, the less pixels are in a chunk (As the resolution stays the same)
        current_grid_side_length, current_chunk_side_length = int(current_grid_side_length), int(current_chunk_side_length)     # Typecast to int
        
        octave_values, array = assign_vectors(int(current_matrix_side_length), array)
        
        data1 = get_dot_products(octave_values, current_grid_side_length, current_chunk_side_length, possible_vector_orientations, 1)
        data2 = get_dot_products(octave_values, current_grid_side_length, current_chunk_side_length, possible_vector_orientations, 2)
        data3 = get_dot_products(octave_values, current_grid_side_length, current_chunk_side_length, possible_vector_orientations, 3)
        data4 = get_dot_products(octave_values, current_grid_side_length, current_chunk_side_length, possible_vector_orientations, 4)

        lerp1 = lerp_horizontally(data1, data2, current_chunk_side_length, current_grid_side_length)
        lerp2 = lerp_horizontally(data3, data4, current_chunk_side_length, current_grid_side_length)
        
        lerp3 = lerp_vertically(lerp1, lerp2, current_chunk_side_length, current_grid_side_length)
        
        arr = numpy.array(lerp3)
        
        if current_octave_index == 0:
            data = arr
        else:
            data += arr * persistence ** current_octave_index
    
    
    # Clean-up needed from here onward
    
    
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
                colour = get_colour(new_data[i][j])
                pygame.draw.rect(screen, colour, (j, i, 1, 1))
                
        pygame.display.flip()
        pygame.time.Clock().tick(20)
    
    pygame.quit()
    
    
    
