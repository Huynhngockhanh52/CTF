nums = [14, 6, 11]
mod = 29

quad_residues = []

for x in nums:
    for a in range(mod):
        if (a * a) % mod == x % mod:
            quad_residues.append(a)
            break

if quad_residues:
    print("Các phần tử là phần dư bậc hai:", quad_residues)
    print("Số nhỏ nhất:", min(quad_residues))
else:
    print("Không có phần tử nào là phần dư bậc hai modulo", mod)
