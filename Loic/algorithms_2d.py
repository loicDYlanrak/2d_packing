def nfdh(rectangles, container_width, container_height):
    """Next-Fit Decreasing Height algorithm"""
    sorted_rects = sorted(rectangles, key=lambda x: -x[1])  # Tri par hauteur décroissante
    
    shelves = []
    current_shelf = []
    current_y = 0
    current_shelf_height = 0
    
    for rect in sorted_rects:
        w, h = rect
        if not current_shelf:
            if w <= container_width and h <= container_height - current_y:
                current_shelf.append((0, current_y, w, h))
                current_shelf_height = h
            else:
                continue
        else:
            last_rect = current_shelf[-1]
            next_x = last_rect[0] + last_rect[2]
            if next_x + w <= container_width:
                current_shelf.append((next_x, current_y, w, h))
            else:
                shelves.append(current_shelf)
                current_y += current_shelf_height
                if h <= container_height - current_y:
                    current_shelf = [(0, current_y, w, h)]
                    current_shelf_height = h
                else:
                    current_shelf = []
                    continue
    
    if current_shelf:
        shelves.append(current_shelf)
    
    return shelves

def ffdh(rectangles, container_width, container_height):
    """First-Fit Decreasing Height algorithm"""
    sorted_rects = sorted(rectangles, key=lambda x: -x[1])  # Tri par hauteur décroissante
    
    shelves = []
    
    for rect in sorted_rects:
        w, h = rect
        placed = False
        
        for shelf in shelves:
            shelf_height = shelf[0][3]
            if h <= shelf_height:
                last_rect = shelf[-1]
                available_width = container_width - (last_rect[0] + last_rect[2])
                if w <= available_width:
                    shelf.append((last_rect[0] + last_rect[2], last_rect[1], w, h))
                    placed = True
                    break
        
        if not placed:
            if not shelves:
                if h <= container_height:
                    shelves.append([(0, 0, w, h)])
            else:
                last_shelf = shelves[-1]
                last_rect = last_shelf[-1]
                new_y = last_rect[1] + last_rect[3]
                if new_y + h <= container_height:
                    shelves.append([(0, new_y, w, h)])
    
    return shelves

def best_fit_2d(rectangles, container_width, container_height):
    """Best-Fit algorithm for 2D packing"""
    sorted_rects = sorted(rectangles, key=lambda x: -x[0]*x[1])  # Tri par aire décroissante
    
    placed_rects = []
    free_rectangles = [(0, 0, container_width, container_height)]
    
    for rect in sorted_rects:
        w, h = rect
        best_score = float('inf')
        best_rect = None
        best_index = -1
        
        for i, free in enumerate(free_rectangles):
            fw, fh = free[2], free[3]
            if w <= fw and h <= fh:
                score = min(fw - w, fh - h)
                if score < best_score:
                    best_score = score
                    best_rect = (free[0], free[1], w, h)
                    best_index = i
            # Essayer aussi en rotation
            if h <= fw and w <= fh:
                score = min(fw - h, fh - w)
                if score < best_score:
                    best_score = score
                    best_rect = (free[0], free[1], h, w)
                    best_index = i
        
        if best_index != -1:
            placed_rects.append(best_rect)
            free = free_rectangles.pop(best_index)
            
            # Découper l'espace restant
            if free[2] > best_rect[2]:
                free_rectangles.append((
                    free[0] + best_rect[2],
                    free[1],
                    free[2] - best_rect[2],
                    free[3]
                ))
            
            if free[3] > best_rect[3]:
                free_rectangles.append((
                    free[0],
                    free[1] + best_rect[3],
                    free[2],
                    free[3] - best_rect[3]
                ))
    
    return [placed_rects]

def brute_force_2d(rectangles, container_width, container_height, max_time=10):
    """Brute-force approach with time limit"""
    import time
    from itertools import permutations
    
    start_time = time.time()
    best_placement = []
    best_area = 0
    
    # Try different orders
    for i, perm in enumerate(permutations(rectangles)):
        if time.time() - start_time > max_time:
            break
        
        current_placement = []
        free_spaces = [(0, 0, container_width, container_height)]
        placed_area = 0
        
        for rect in perm:
            w, h = rect
            placed = False
            
            for j, space in enumerate(free_spaces):
                if w <= space[2] and h <= space[3]:
                    # Place without rotation
                    current_placement.append((space[0], space[1], w, h))
                    placed_area += w * h
                    placed = True
                    
                    # Split remaining space
                    remaining_width = space[2] - w
                    remaining_height = space[3] - h
                    
                    if remaining_width > 0 and remaining_height > 0:
                        if remaining_width > remaining_height:
                            free_spaces.append((space[0] + w, space[1], remaining_width, h))
                            free_spaces.append((space[0], space[1] + h, space[2], remaining_height))
                        else:
                            free_spaces.append((space[0], space[1] + h, w, remaining_height))
                            free_spaces.append((space[0] + w, space[1], remaining_width, space[3]))
                    
                    del free_spaces[j]
                    break
                
                elif h <= space[2] and w <= space[3]:
                    # Place with rotation
                    current_placement.append((space[0], space[1], h, w))
                    placed_area += w * h
                    placed = True
                    
                    # Split remaining space
                    remaining_width = space[2] - h
                    remaining_height = space[3] - w
                    
                    if remaining_width > 0 and remaining_height > 0:
                        if remaining_width > remaining_height:
                            free_spaces.append((space[0] + h, space[1], remaining_width, w))
                            free_spaces.append((space[0], space[1] + w, space[2], remaining_height))
                        else:
                            free_spaces.append((space[0], space[1] + w, h, remaining_height))
                            free_spaces.append((space[0] + h, space[1], remaining_width, space[3]))
                    
                    del free_spaces[j]
                    break
            
            if not placed:
                break
        
        if placed_area > best_area:
            best_area = placed_area
            best_placement = current_placement
    
    return [best_placement] if best_placement else []