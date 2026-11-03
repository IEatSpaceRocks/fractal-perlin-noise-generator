import math, random
import numpy as np



# Turns a given value (in degrees) by a given turn value (in degrees). Return value range: 0 <= x < 360
def turn(to_turn, turn_degree):
    turned = to_turn + turn_degree
    while turned < 0:
        turned += 360
    while turned >= 360:
        turned -= 360
        
    return turned



# Converts a given degree value (0, 90, 180 or 270) over to a movement direction in a matrix. Returns [y, x]. 0 degrees is north, then clockwise
def matrix_movement_direction(degree):
    match degree:
        case 0:
            return [-1, 0]
        case 90:
            return [0, 1]
        case 180:
            return [1, 0]
        case 270:
            return [0, -1]



# Moves a given vertex along a given orientation
def move_current_vertex(current_vertex, orientation_degree):
    current_vertex[0] += matrix_movement_direction(orientation_degree)[0]   # Move in column (up or down)
    current_vertex[1] += matrix_movement_direction(orientation_degree)[1]   # Move in row (left or right)
    
    return current_vertex



# Assigns vectors in a spiral for every vertex on the matrix of a given size. Returns the resulting vector matrix (2D list).
def assign_vectors(matrix_side_length, vector_values):
    vector_matrix = [[""] * matrix_side_length for _ in range(matrix_side_length)]                                  # Create the matrix (2D list)
    
    current_vertex = [math.floor(matrix_side_length/2), math.floor(matrix_side_length/2)]                           # Starts in the middle
    
    orientation_degree = 0      # Which way is the spiral "facing" or "spiraling"
    x = 0.5                     # In a spiral, turning happens according to rules that would be too long to explain here
    assigned = 0                # How many vectors have already be assigned
    
    while True:
        for _ in range(math.ceil(x)):                                                       # x will be 1, 1, 2, 2, 3, 3, 4, 4... and make a nice spiral
            vector_matrix[current_vertex[0]][current_vertex[1]] = vector_values[0]          # Assign a vector to the current vertex
            del vector_values[0]                                                            # Delete the assigned vector value from the values list
            assigned += 1
            current_vertex = move_current_vertex(current_vertex, orientation_degree)        # Move the current vertex

        orientation_degree = turn(to_turn=orientation_degree, turn_degree=-90)              # Turn the orientation by -90 degrees
        x += 0.5
        if assigned == matrix_side_length ** 2:                                             # When all matrix points have been assigned
            break                                                                           # break the 'while True' loop

    return vector_matrix, vector_values                 # Return the finished matrix and the remaining vector values



# Generate the sequence of needed values (later used for vectors) based on a given seed and the generation parameters
def generate_sequence(matrix_side_length, octave_count, lacunarity, seed, max_value):
    sequence = []
    random.seed(seed)
    
    for i in range(octave_count):
        new_seed = random.random()
        octave_values = []
        vertex_count = int((matrix_side_length ** 2) * (lacunarity ** (i * 2)))
        
        for _ in range(vertex_count):
            octave_values.append(random.randint(1, max_value))
            
        random.seed(new_seed)
        print(octave_values[0])
        sequence.extend(octave_values)
        
    return sequence



# Get the value associated to a given sign, for dot product calculation. Variants: 1 - top left, 2 - top right, 3 - bottom left, 4 - bottom right
def get_value(sign, variable, chunk_side_length, variant):
    match sign:
        case "a":                                                   # relative x coordinate of pixel
            if variant == 1 or variant == 3:
                return variable % chunk_side_length + 1
            else:
                return chunk_side_length - variable % chunk_side_length
        case "b":                                                   # relative y coordinate of pixel
            if variant == 1 or variant == 2:
                return variable  % chunk_side_length + 1
            else:
                return chunk_side_length - variable % chunk_side_length
        case "x":                                                   # index for the vector's place in a row
            if variant == 1 or variant == 3:
                return int(variable / chunk_side_length)
            else:
                return int(variable / chunk_side_length) + 1
        case "y":                                                   # index for the vector's place in a column
            if variant == 1 or variant == 2:
                return int(variable / chunk_side_length)
            else:
                return int(variable / chunk_side_length) + 1
        


# Calculate the dot product values for one vector variant, for the current octave
def calc_dot_products(vector_values, grid_side_length, chunk_side_length, psbl_vect_orients, variant):
    pixel_count = grid_side_length * chunk_side_length
    pixel_values = []
    
    for y in range(pixel_count):
        b = get_value("b", y, chunk_side_length, variant)
        row = []
        
        for x in range(pixel_count):
            a = get_value("a", x, chunk_side_length, variant)
            val_x, val_y = get_value("x", x, chunk_side_length, variant), get_value("y", y, chunk_side_length, variant)
            degree = vector_values[val_y][val_x] * (360/psbl_vect_orients)
            row.append(math.sin(degree) * a + math.cos(degree) * b)
            
        pixel_values.append(row)
        
    return pixel_values



if __name__ == "__main__":
    
    print("~" * 50)
    print("Running this file does nothing. Please run main.py!")
    print("~" * 50)
