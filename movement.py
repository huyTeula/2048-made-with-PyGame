GRID_SIZE = 7  # Cập nhật kích thước lưới

def slide_and_merge_row_left(row):
    """Trượt hàng sang trái và gộp ô."""
    new_row = [num for num in row if num != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [num for num in new_row if num != 0]
    return new_row + [0] * (GRID_SIZE - len(new_row))

def move_left(grid):
    """Di chuyển toàn bộ lưới sang trái."""
    new_grid = []
    for row in grid:
        new_grid.append(slide_and_merge_row_left(row))
    return new_grid

def rotate_grid(grid, times):
    """Xoay lưới theo chiều kim đồng hồ `times` lần."""
    for _ in range(times):
        grid = [list(row) for row in zip(*grid[::-1])]
    return grid

def handle_move(grid, direction):
    """Xử lý các hướng di chuyển."""
    if direction == "left":
        return move_left(grid)
    elif direction == "right":
        grid = rotate_grid(grid, 2)
        grid = move_left(grid)
        return rotate_grid(grid, 2)
    elif direction == "up":
        grid = rotate_grid(grid, 3) # Thay đổi thành 3
        grid = move_left(grid)
        return rotate_grid(grid, 1) # Thay đổi thành 1
    elif direction == "down":
        grid = rotate_grid(grid, 1) # Thay đổi thành 1
        grid = move_left(grid)
        return rotate_grid(grid, 3) # Thay đổi thành 3
    return grid
