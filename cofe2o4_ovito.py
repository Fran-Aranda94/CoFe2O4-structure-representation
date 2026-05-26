import numpy as np

# ==================================================
# CoFe2O4 spinel structure for OVITO visualization
# Output: cofe2o4.xyz
# ==================================================

a = 8.39  # lattice parameter in Angstrom
n_cells = 3  # increase to 4 or 5 for a bigger particle

output_file = "cofe2o4.xyz"

# Approximate spinel fractional coordinates
# Fe in tetrahedral sites
tetra_Fe = [
    (1/8, 1/8, 1/8),
    (1/8, 5/8, 5/8),
    (5/8, 1/8, 5/8),
    (5/8, 5/8, 1/8),
    (7/8, 7/8, 7/8),
    (7/8, 3/8, 3/8),
    (3/8, 7/8, 3/8),
    (3/8, 3/8, 7/8),
]

# Octahedral sites: half Co, half Fe
octa_sites = [
    (1/2, 1/2, 1/2),
    (1/2, 1/4, 1/4),
    (1/4, 1/2, 1/4),
    (1/4, 1/4, 1/2),
    (1/2, 3/4, 3/4),
    (3/4, 1/2, 3/4),
    (3/4, 3/4, 1/2),
    (3/4, 1/4, 1/4),
    (1/4, 3/4, 1/4),
    (1/4, 1/4, 3/4),
    (3/4, 3/4, 1/4),
    (3/4, 1/4, 3/4),
    (1/4, 3/4, 3/4),
    (0, 0, 0),
    (0, 1/2, 1/2),
    (1/2, 0, 1/2),
]

# Oxygen positions, approximate spinel oxygen parameter
u = 0.261
oxygen_base = [
    (u, u, u),
    (u, 0.5-u, 0.5+u),
    (0.5-u, 0.5+u, u),
    (0.5+u, u, 0.5-u),
]

# Generate equivalent oxygen positions by FCC translations
fcc_translations = [
    (0, 0, 0),
    (0, 0.5, 0.5),
    (0.5, 0, 0.5),
    (0.5, 0.5, 0),
]

atoms = []

for i in range(n_cells):
    for j in range(n_cells):
        for k in range(n_cells):
            cell_shift = np.array([i, j, k], dtype=float)

            # Fe tetrahedral
            for pos in tetra_Fe:
                r = (np.array(pos) + cell_shift) * a
                atoms.append(("Fe", r))

            # Octahedral sites: assign first 8 as Co, next 8 as Fe
            for idx, pos in enumerate(octa_sites):
                r = (np.array(pos) + cell_shift) * a
                element = "Co" if idx < 8 else "Fe"
                atoms.append((element, r))

            # Oxygen
            oxygen_positions = []
            for base in oxygen_base:
                for trans in fcc_translations:
                    p = (np.array(base) + np.array(trans)) % 1.0
                    oxygen_positions.append(tuple(p))

            # Duplicate symmetry-related oxygen set
            oxygen_positions += [(1-x, 1-y, 1-z) for x, y, z in oxygen_positions]

            for pos in oxygen_positions:
                r = (np.array(pos) + cell_shift) * a
                atoms.append(("O", r))

# Write XYZ
with open(output_file, "w") as f:
    f.write(f"{len(atoms)}\n")
    f.write("CoFe2O4 spinel structure for OVITO\n")
    for element, r in atoms:
        f.write(f"{element} {r[0]:.5f} {r[1]:.5f} {r[2]:.5f}\n")

print(f"File created: {output_file}")
print(f"Total atoms: {len(atoms)}")