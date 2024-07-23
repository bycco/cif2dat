# Ensure mendeleev package is installed
# !pip install mendeleev

from mendeleev import element

# Prompt the user for the input file name
input_file = input("Enter the input file name: ")

# Open the input file and count the number of lines
with open(input_file, 'r') as f:
    lines = f.readlines()
natoms = len(lines) - 27
print(natoms)
atomconfig = [line.split() for line in lines[27:]]

# Extract unique elements from the first column starting from line 28
elements = list(set(row[0][:2] if len(row[0]) > 1 and row[0][1].islower() else row[0][0] for row in atomconfig if row[0][0].isalpha()))

# Replace the first column with the corresponding numbers using unique elements
element_map = {elem: str(i+1) for i, elem in enumerate(elements)}

# Print the unique number of each element
for elem, num in element_map.items():
    print(f"Element: {elem}, Number: {num}")

# Get atomic masses using mendeleev
atomic_masses = {elem: element(elem).atomic_weight for elem in elements}

# Replace the first column in atomconfig with the mapped numbers
for row in atomconfig:
    for elem in elements:
        if row[0].startswith(elem):
            row[0] = element_map[elem]
            break

# Extract the number of atom types
atom_line = lines[5]
natomtypes = len([c for c in atom_line.split("'")[1] if c.isupper()])

# Extract the cell parameters
cell_lines = lines[10:13]
lx, ly, lz = [float(line.split()[1]) for line in cell_lines]
for row in atomconfig:
    row[3] = str(float(row[3]) * lx)
    row[4] = str(float(row[4]) * ly)
    row[5] = str(float(row[5]) * lz)

# Open the output file and write the number of atoms
with open('output.dat', 'w') as f:
    f.write('\n')  # Copy the first two lines from input.cif to output.dat
    f.write('\n')
    f.write(f'{natoms} atoms\n')  # Write the number of atoms on line 3
    f.write('\n')
    f.write(f'{natomtypes} atom types\n')
    f.write('\n')
    f.write(f'0.0000 {lx} xlo xhi\n')
    f.write(f'0.0000 {ly} ylo yhi\n')
    f.write(f'0.0000 {lz} zlo zhi\n')
    f.write('\n')
    f.write('Masses \n')
    f.write('\n')

    # Write the unique number and atomic weights
    for elem, num in element_map.items():
        f.write(f'{num} {atomic_masses[elem]}\n')

    f.write('\n')
    f.write('Atoms\n')
    f.write('\n')
    for i in range(natoms):
        f.write(f'{i+1} {atomconfig[i][0]} 0 {atomconfig[i][3]} {atomconfig[i][4]} {atomconfig[i][5]} \n')
