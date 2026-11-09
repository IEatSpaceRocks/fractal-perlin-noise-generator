import math, random



# Generate an array of random values (later used for vectors) based on a given seed and the generation parameters
def generate_array(grid_side_length, octave_count, lacunarity, seed, max_value):
    
    matrix_side_length = grid_side_length + 1   # The number of vertices in a row is one greater than the number of chunks (0 - 0 - 0) (0 vertex, - chunk/side)
    array = []                                  # array will contain the generated values
    random.seed(seed)                           # Set the generation seed to the user input seed
    
    for i in range(octave_count):                                                   # For every octave values are generated separately
        new_seed = random.random()                                                  # Every octave uses a different seed, which is generated here
        octave_values = []                                                          # Values for the current octave
        vertex_count = int((matrix_side_length ** 2) * (lacunarity ** (i * 2)))     # Calculate the number of vertices in the current octave
        
        for _ in range(vertex_count):
            octave_values.append(random.randint(1, max_value))                      # Generate the values for the current octave
            
        random.seed(new_seed)                                                       # Set the new seed
        array.extend(octave_values)                                                 # Append the generated values to the main array
        
    return array                    # Return the finished list



# Turns a given value (in degrees) by a given turn value (in degrees). Return value range: 0 <= x < 360
def turn(to_turn, turn_degree):
    
    turned = to_turn + turn_degree
    while turned < 0:
        turned += 360
    while turned >= 360:
        turned -= 360
        
    return turned



# Converts a given orientation degree (0, 90, 180 or 270) over to a movement direction in a matrix. Returns [y, x].
def get_direction(degree):
    
    match degree:
        case 0:                     # North (+y)
            return [-1, 0]
        case 90:                    # East  (+x)
            return [0, 1]
        case 180:                   # South (-y)
            return [1, 0]
        case 270:                   # West  (-x)
            return [0, -1]



# Moves a given vertex along a direction based on the given orientation degree. Vertex is a coordinate, in this format: [y, x]. More about 'get_direction' above.
def move_vertex(vertex, orientation_degree):
    
    vertex[0] += get_direction(orientation_degree)[0]       # Move in column (up or down)
    vertex[1] += get_direction(orientation_degree)[1]       # Move in row (left or right)
    
    return vertex



# Assigns vectors in a spiral for every vertex on a matrix of a given size. Returns the resulting vector matrix (2D list).
def assign_vectors(matrix_side_length, vector_values):
    
    vector_matrix = [[""] * matrix_side_length for _ in range(matrix_side_length)]          # Create the empty matrix (2D list)
    current_vertex = [math.floor(matrix_side_length/2), math.floor(matrix_side_length/2)]   # Starts in the middle, moves in a spiral and assigns vectors
    
    orientation_degree = 0      # Which way is the spiral "facing" or "spiraling"
    x = 0.5                     # math.ceil(x) will show how long the current spiral arm should be
    assigned = 0                # How many vectors have already be assigned
    
    while True:
        for _ in range(math.ceil(x)):                                                   # x will be 1, 1, 2, 2, 3, 3, 4, 4... and make a nice spiral
            vector_matrix[current_vertex[0]][current_vertex[1]] = vector_values[0]      # Assign a vector to the current vertex
            del vector_values[0]                                                        # Delete the assigned vector value from the values list
            assigned += 1
            current_vertex = move_vertex(current_vertex, orientation_degree)            # Move the current vertex

        orientation_degree = turn(orientation_degree, -90)                              # Turn the orientation by -90 degrees (Spiral anti-clockwise)
        x += 0.5
        
        if assigned == matrix_side_length ** 2:         # When all matrix points have been assigned...
            break                                       # ...break the 'while True' loop

    return vector_matrix, vector_values                 # Return the finished matrix and the remaining vector values



# Get the value for the given variable (var1), for dot product calculation. Variants: 1 - top left, 2 - top right, 3 - bottom left, 4 - bottom right
def get_value(var1, var2, chunk_side_length, variant):          # var2 is a variable that influences the value of var1
    
    match var1:
        case "a":                                                       # a = relative x coordinate of pixel
            if variant == 1 or variant == 3:
                return var2 % chunk_side_length + 0.5
            else:
                return var2 % chunk_side_length - chunk_side_length + 0.5
            
        case "b":                                                       # b = relative y coordinate of pixel
            if variant == 1 or variant == 2:
                return var2 % chunk_side_length + 0.5
            else:
                return var2 % chunk_side_length - chunk_side_length + 0.5
            
        case "val_x":                                                       # val_x = index for the vector's place in a row
            if variant == 1 or variant == 3:
                return int(var2 / chunk_side_length)
            else:
                return int(var2 / chunk_side_length) + 1
            
        case "val_y":                                                       # val_y = index for the vector's place in a column
            if variant == 1 or variant == 2:
                return int(var2 / chunk_side_length)
            else:
                return int(var2 / chunk_side_length) + 1
        


# Calculate the dot product values for one vector variant, for the given octave
def get_dot_products(vector_values, grid_side_length, chunk_side_length, psbl_vect_orients, variant):
    
    pixel_count = grid_side_length * chunk_side_length              # Pixel count in 1 row
    pixel_values = []                                               # A matrix containing the dot product values for each pixel
    
    for y in range(pixel_count):
        b = get_value("b", y, chunk_side_length, variant)           # Get the value for b
        row = []                                                    # Empty the row array
        
        for x in range(pixel_count):
            a = get_value("a", x, chunk_side_length, variant)                                                                       # Get value for a
            val_x, val_y = get_value("val_x", x, chunk_side_length, variant), get_value("val_y", y, chunk_side_length, variant)     # Get value for val_x and val_y
            radian = math.radians(vector_values[val_y][val_x] * (360/psbl_vect_orients))                                            # Convert the vector value to radians
            row.append(math.sin(radian) * a + math.cos(radian) * b)                                                                 # Add the dot product to the row
            
        pixel_values.append(row)
        
    return pixel_values



# Linear interpolation between 2 matrices horizontally. Applies smoothening function too.
def lerp_horizontally(matrix_left, matrix_right, chunk_side_length, grid_side_length):
    
    new_matrix = []
    
    for i in range(grid_side_length * chunk_side_length):       # Go through each row one by one
        row_l, row_r = matrix_left[i], matrix_right[i]          # Get the current rows from both matrices
        new_row = []
        
        for j in range(grid_side_length):                                                   # For every chunk in the row...
            
            for k in range(chunk_side_length):                                                  # For every pixel in the chunk...
                r, l = row_r[j * chunk_side_length + k], row_l[j * chunk_side_length + k]           # Get current pixel values from both matrices
                x = (k + 0.5) / (chunk_side_length)                                                 # x grows linearly as a chunk's pixels are being iterated through
                new_value = (r - l) * (6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3) + l                  # New value is calculated with a simple lerp + smoothening function
                new_row.append(new_value)                                                           # Append the interpolated value to the new row
        
        new_matrix.append(new_row)
    
    return new_matrix
        

# Linear interpolation between 2 matrices vertically. Applies smoothening function too.
def lerp_vertically(matrix_up, matrix_down, chunk_side_length, grid_side_length):

    pixels = grid_side_length * chunk_side_length               # Pixel count in a row
    new_matrix = [[] for _ in range(pixels)]                    # Define new matrix to be 'pixels * pixels' in size
    
    for i in range(pixels):                                     # For every column...
        col_u, col_d = [], []
        
        for s in range(pixels):                                     # For every row...
            col_u.append(matrix_up[s][i])                               # Create an array of the column values for the upper matrix
            col_d.append(matrix_down[s][i])                             # Create an array of the column values for the lower matrix
            
        for j in range(grid_side_length):                           # For every chunk in the column...
            
            for k in range(chunk_side_length):                          # For every pixel in the chunk...
                u, d = col_u[j * chunk_side_length + k], col_d[j * chunk_side_length + k]       # Get current pixel values from both matrices
                x = (k + 0.5) / (chunk_side_length)                                             # x grows linearly as a chunk's pixels are being iterated through
                new_value = (d - u) * (6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3) + u              # New value is calculated with a simple lerp + smoothening function
                new_matrix[j * chunk_side_length + k].append(new_value)                         # Append the interpolated value to the correct row in the new matrix

    return new_matrix



# ~~~~~  WIP  ~~~~~

# Apply a certain color gradient to the finished data
def get_colour(value):
    if value < 0:
        colour = (71, 59, 120)
    elif value < 0.3:
        colour = (75, 91, 171)
    elif value < 0.35:
        colour = (250, 246, 170)
    elif value < 0.6:
        colour = (76, 255, 97)
    elif value < 0.8:
        colour = (143, 222, 93)
    elif value < 0.9:
        colour = (126, 126, 143)
    elif value <= 1:
        colour = (255, 255, 255)
    
    return colour



if __name__ == "__main__":
    
    print("~" * 50)
    print("Running this file does nothing. Please run main.py!")
    print("~" * 50)
