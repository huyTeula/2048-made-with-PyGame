import random

GRID_SIZE = 7  # Thay đổi kích thước lưới thành 7x7

def add_new_tile(grid):
    """Thêm ô mới (2 hoặc 4) vào lưới."""
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = random.choices([2, 4], weights=[0.9, 0.1])[0] # 90% chance of 2, 10% chance of 4


def is_game_over(grid):
    """Kiểm tra trò chơi đã kết thúc chưa (phiên bản chính xác hơn)."""
    # Kiểm tra ô trống
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                return False

    # Kiểm tra khả năng di chuyển và gộp
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            # Kiểm tra hàng
            if c < GRID_SIZE - 1 and grid[r][c] == grid[r][c+1]:
                return False
            # Kiểm tra cột
            if r < GRID_SIZE - 1 and grid[r][c] == grid[r+1][c]:
                return False
    return True
def has_won(grid):
    """Kiểm tra xem người chơi đã thắng chưa."""
    for row in grid:
        if 1048576 in row:  # Thay đổi giá trị này nếu cần thiết
            return True
    return False