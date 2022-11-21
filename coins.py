from itertools import permutations
coins = [2, 3, 5, 7, 9]


# _ + _ * _^2 + _^3 - _ = 399
perms = permutations(coins)
for perm in perms:
    answer = (perm[0] + perm[1] * perm[2]**2 + perm[3]**3 - perm[4])
    # print(f"{perm[0]} + {perm[1]} * {perm[2]}^2 + {perm[3]}^3 - {perm[4]} = {(perm[0] + perm[1] * perm[2]**2 + perm[3]**3 - perm[4])}")
    if answer == 399:
        print(f"Found it! {perm[0]} + {perm[1]} * {perm[2]}^2 + {perm[3]}^3 - {perm[4]} = {(perm[0] + perm[1] * perm[2]**2 + perm[3]**3 - perm[4])}")
        break
    # print(f"{(perm[0] + perm[1] * perm[2]**2 + perm[3]**3 - perm[4])=}")
