import sys
# Solution goes in here

# Key: name of type of dna, value: respective dna sequence
dnaMap = {}
# Keys are the different DNA-types and blosum is the cost combinations
keys, blosum = [], []

def main():
    if len(sys.argv) != 2:
        print("Usage: python gorilla.py datafile")
        sys.exit(1)

    # Read from file
    with open(sys.argv[1], "r") as f:
        data = f.read()

    # Parse data
    load_blosum()    
    data = data.split(">")
    
    for i in range(1, len(data)):
        dna = data[i].split("\n")
        dnaMap[dna[0].strip()] = "".join(dna[1:])
    output = solve(dnaMap.get("Snark"), dnaMap.get("Sphinx"))
    print(output)

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

def lookup_blosum(x,y):
    return blosum[get_key_index(x)][get_key_index(y)]

def get_key_index(key):
    k = keys.index(key)
    return k

def pretty_print_2D_array(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()

def print2DarrayWithLabels(A, x, y):
    print(" ", end=" ")
    for i in range(len(x)):
        print(x[i], end=" ")
    print()
    for i in range(len(A)):
        print(y[i], end="  ")
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()

def start_solve(x, y):
    # to be implemented
    # if x < y 
    return 0

def solve(x, y):
    HYPHEN_COST = -4
    A = [[0 for _ in range(len(x))] for _ in range(len(y))]
    # B = [[0]*len(x)] * len(y)
    for i in range(len(y)):
        # A[i][0] = lookup_blosum(x[0], y[i])
        A[i][0] = HYPHEN_COST

    for j in range(len(x)):
        # A[0][j] = lookup_blosum(x[j], y[0])
        A[0][j] = HYPHEN_COST

    pretty_print_2D_array(A)

    for row in range(1, len(y)):
        for col in range(1, len(x)):
            take   = lookup_blosum(y[row], x[col]) + A[row-1][col-1]
            drop_i = HYPHEN_COST + A[row-1][col]
            drop_j = HYPHEN_COST + A[row][col-1]
            A[row][col] = max(take, drop_i, drop_j)
    
    print("\nAfter solve:")
    print2DarrayWithLabels(A, x, y)

    return A[len(y)-1][len(x)-1]

if __name__ == "__main__":
    main()
