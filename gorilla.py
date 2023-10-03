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

def solve(dna_sequence_x, dna_sequence_y):
    # initialiase 2-d array - tabulation for storing solutions to subproblems 
    alignment = [[0 for _ in range(len(dna_sequence_x)+1)] for _ in range(len(dna_sequence_y)+1)]
    for i in range(len(dna_sequence_y)+1):
        alignment[i][0] = HYPHEN_COST * i

    for j in range(len(dna_sequence_x)+1):
        alignment[0][j] = HYPHEN_COST * j

    for row in range(1, len(dna_sequence_y)+1):
        for col in range(1, len(dna_sequence_x)+1):
            take   = blosum_cost(dna_sequence_y[row-1], dna_sequence_x[col-1]) + alignment[row-1][col-1]
            drop_i = HYPHEN_COST + alignment[row-1][col]
            drop_j = HYPHEN_COST + alignment[row][col-1]
            alignment[row][col] = max(take, drop_i, drop_j)

    return alignment[len(dna_sequence_y)][len(dna_sequence_x)], backtrack(alignment, dna_sequence_x, dna_sequence_y)

def backtrack(alignment, dna_sequence_x, dna_sequence_y):
    global HYPHEN_COST

    backtrack_dna_sequence_x = ""
    backtrack_dna_sequence_y = ""

    row = len(dna_sequence_y)
    col = len(dna_sequence_x)

    while (row > 0 or col > 0):

        v = alignment[row][col]
        v_take = alignment[row-1][col-1]
        v_drop_i = alignment[row-1][col]
        
        if blosum_cost(dna_sequence_y[row-1], dna_sequence_x[col-1]) + v_take == v:
            backtrack_dna_sequence_x += dna_sequence_x[col-1]
            backtrack_dna_sequence_y += dna_sequence_y[row-1]
            row -= 1
            col -= 1
        elif v_drop_i + HYPHEN_COST == v:      
            backtrack_dna_sequence_x += "-"
            backtrack_dna_sequence_y += dna_sequence_y[row-1]
            row -= 1
        else: # v_drop_j
            backtrack_dna_sequence_x += dna_sequence_x[col-1]
            backtrack_dna_sequence_y += "-"
            col -= 1
    
    return backtrack_dna_sequence_x[::-1], backtrack_dna_sequence_y[::-1]

def initiate_solve(dna_sequence_x, dna_sequence_y):
    if dna_sequence_x < dna_sequence_y: 
        return solve(dna_sequence_y, dna_sequence_x) 
    return solve(dna_sequence_x, dna_sequence_y)

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
                # initiate_solve returns a tuple - (match_score,(backtrack_x,backtrack_y))
                alignment_result = initiate_solve(dna_map[i_key], dna_map[j_key])
                print(f"{i_key}--{j_key}: {str(alignment_result[0])}")
                print(f"{alignment_result[1][1]}\n{alignment_result[1][0]}")
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
    return keys.index(key)

if __name__ == "__main__":
    main()
