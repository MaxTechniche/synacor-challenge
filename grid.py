grid = [[22, '+', 4, '*'],
        ['-', 4, '*', 8],
        [9, '-', 11, '-'],
        ['*', 18, '*', 1]]

visited = [[False] * len(grid[0]) for _ in range(len(grid))]


def traverse(grid, x, y, path=[22], visited=[]):
    # print(path)
    # print(''.join(str(s) for s in path)+'1')
    if x == 0 and y == 0 and len(path) > 1:
        return
    if len(path) > 13:
        return
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
        return

    if x == len(grid) - 1 and y == len(grid[0]) - 1:
        # print(''.join(str(s) for s in path)+'1')
        try:
            nums = []
            num = path.pop(0)
            nums.append(num)
            while path:
                n = path.pop(0)
                m = path.pop(0)
                num = eval(f'{num}{n}{m}')
                nums.append(n)
                nums.append(m)
            if num == 30:
                print(' '.join(str(s) for s in nums))
        except ZeroDivisionError:
            pass
        except SyntaxError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass
        return
    if x + 1 < len(grid):
        traverse(grid, x + 1, y, path + [grid[x+1][y]], visited)
    if x > 0:
        traverse(grid, x - 1, y, path + [grid[x-1][y]], visited)
    if y + 1 < len(grid[0]):
        traverse(grid, x, y + 1, path + [grid[x][y+1]], visited)
    if y > 0:
        traverse(grid, x, y - 1, path + [grid[x][y-1]], visited)


traverse(grid, 0, 0)
