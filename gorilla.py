import sys

# Keys are the different DNA-types and blosum is the cost combinations
keys, blosum = [], []
HYPHEN_COST = -4

def main():
    if len(sys.argv) != 2:
        print("Usage: python gorilla.py datafile")
        sys.exit(1)

    # Read from file
    with open(sys.argv[1], "r") as f:
        data = f.read()

    # Parse data
    load_blosum()    
    dna_map = load_dna_data(data)
    
    solve_and_print_dna_map(dna_map)
def load_dna_data(data):
    data = data.split(">")
    dna_map = {}

    for i in range(1, len(data)):
        dna = data[i].split("\n")
        key = dna[0].split()[0].strip()
        dna_map[key] = "".join(dna[1:])

    return dna_map

def solve_and_print_dna_map(dna_map):
    seen_keys = []
    for i_key in dna_map:
        for j_key in dna_map:
            if i_key == j_key or (j_key in seen_keys):
               continue
            else:
                match_result = initiate_solve(dna_map[i_key], dna_map[j_key])
                print(f"{i_key}--{j_key}: {str(match_result[0])}")
                print(f"{match_result[1][0]}\n{match_result[1][1]}")
        seen_keys.append(i_key)

def load_blosum():
    global keys, blosum

    f = open("data/BLOSUM62.txt", "r")
    first = True
    for line in f:
    # Skip comment lines and empty lines
        if not line.startswith("#") and line.strip():
            # Split the line by whitespace and convert values to integers
            if(first):
                for v in line.split():
                    keys.append(v)
                blosum = [[None for _ in range(len(keys))] for _ in range(len(keys))]
                first = False
            else:
                i = 0
                y = None
                for v in line.split():
                    if y is None:
                        y = v
                    else:
                        blosum[i-1][get_key_index(y)] = int(v)
                    i += 1

def blosum_cost(x,y):
    return blosum[get_key_index(x)][get_key_index(y)]

def get_key_index(key):
    k = keys.index(key)
    return k

def pretty_print_2D_array(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()

def print_2D_array_with_labels(A, x, y):
    print(" ", end=" ")
    print("*", end=" ")
    for i in range(len(x)):
        print(x[i], end=" ")
    print()
    for i in range(len(A)):
        print(y[i], end="  ")
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()

def initiate_solve(x, y):
    if x < y: 
        return solve(y,x) 
    else:
        return solve(x,y)

def solve(x, y):
    A = [[0 for _ in range(len(x)+1)] for _ in range(len(y)+1)]
    # B = [[0]*len(x)] * len(y)
    for i in range(len(y)+1):
        A[i][0] = HYPHEN_COST * i

    for j in range(len(x)+1):
        A[0][j] = HYPHEN_COST * j

    for row in range(1, len(y)+1):
        for col in range(1, len(x)+1):
            take   = blosum_cost(y[row-1], x[col-1]) + A[row-1][col-1]
            drop_i = HYPHEN_COST + A[row-1][col]
            drop_j = HYPHEN_COST + A[row][col-1]
            A[row][col] = max(take, drop_i, drop_j)
    
    # print("\nAfter solve:")
    # pretty_print_2D_array(A)

    return A[len(y)][len(x)], backtrack(A, x, y)

def backtrack(A, x, y):
    global HYPHEN_COST

    backtrack_x = ""
    backtrack_y = ""

    row = len(y)
    col = len(x)

    while (row > 0 or col > 0):

        v = A[row][col]
        v_take = A[row-1][col-1]
        v_drop_i = A[row-1][col]
        
        if blosum_cost(y[row-1], x[col-1]) + v_take == v:
            backtrack_x += x[col-1]
            backtrack_y += y[row-1]
            row -= 1
            col -= 1
        elif v_drop_i + HYPHEN_COST == v:      
            backtrack_x += "-"
            backtrack_y += y[row-1]
            row -= 1
        else: # v_drop_j
            backtrack_x += x[col-1]
            backtrack_y += "-"
            col -= 1
    backtrack_x_rev = backtrack_x[::-1]
    backtrack_y_rev = backtrack_y[::-1]

    return backtrack_x_rev, backtrack_y_rev

if __name__ == "__main__":
    main()
