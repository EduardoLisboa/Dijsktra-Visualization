import pygame
from random import randint
from queue import PriorityQueue
from spot import Spot, WHITE, GREY

WIDTH = HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A* Path Finding Visualizer')


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                spot.make_barrier()
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # LEFT MOUSE CLICK
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                if row != 0 and row != ROWS - 1 and col != 0 and col != ROWS - 1:
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    
                    elif spot != end and spot != start:
                        spot.make_barrier()
            
            # RIGHT MOUSE CLICK
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                if row != 0 and row != ROWS - 1 and col != 0 and col != ROWS - 1:
                    spot = grid[row][col]
                    spot.reset()

                    if spot == start:
                        start = None

                    if spot == end:
                        end = None
            
            if event.type == pygame.KEYDOWN:
                # LEAVES THE PROGRAM
                if event.key == pygame.K_ESCAPE:
                    run = False

                # START THE ALGORITHM
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                # CLEAR THE SCREEN
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                
                # MAKE RANDOM MAZE
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    row, col = randint(1, ROWS - 2), randint(1, ROWS - 2)
                    spot = grid[row][col]
                    spot.make_start()
                    start = spot

                    row, col = randint(1, ROWS - 2), randint(1, ROWS - 2)
                    while row == spot.row and col == spot.col or abs(row - spot.row) + abs(col - spot.col) < 40:
                        row, col = randint(1, ROWS - 2), randint(1, ROWS - 2)
                    
                    spot = grid[row][col]
                    spot.make_end()
                    end = spot

                    barriers = []
                    for _ in range(1, ROWS - 1):
                        for _ in range(1, ROWS - 1):
                            row, col = randint(1, ROWS - 2), randint(1, ROWS - 2)
                            spot = grid[row][col]
                            while spot in barriers or spot == start or spot == end:
                                row, col = randint(1, ROWS - 2), randint(1, ROWS - 2)
                                spot = grid[row][col]
                            
                            spot.make_barrier()
                            barriers.append(spot)

                            if len(barriers) >= ROWS ** 2 * 0.3:
                                break

    pygame.quit()



if __name__ == '__main__':
    main(WIN, WIDTH)

