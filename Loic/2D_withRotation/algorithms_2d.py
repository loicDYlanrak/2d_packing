import math
from shapes import Circle, Rectangle, IsoscelesTriangle

def check_collision(shape, placed_shapes):
    for other in placed_shapes:
        if shape.intersects(other):
            return True
    return False

def ffdh(shapes, container_width, container_height):
    sorted_shapes = sorted(shapes, key=lambda s: max(s.get_bounding_box()), reverse=True)
    
    shelves = []  # Format: (height, shapes_list, y)
    current_y = 0
    placed_shapes = []

    for shape in sorted_shapes:
        placed = False
        
        # Essayer toutes les rotations
        for rotation in [0, math.pi/2, math.pi]:
            if placed:
                break
                
            shape.rotation = rotation
            w, h = shape.get_bounding_box()

            # Chercher dans les étagères existantes
            for shelf in shelves:
                shelf_height, shelf_shapes, shelf_y = shelf  # Décomposer les 3 éléments
                shelf_width_used = sum(s.get_bounding_box()[0] for s in shelf_shapes)
                
                if shelf_height >= h and shelf_width_used + w <= container_width:
                    shape.x = shelf_width_used
                    shape.y = shelf_y
                    
                    if not check_collision(shape, placed_shapes):
                        shelf_shapes.append(shape)
                        placed_shapes.append(shape)
                        placed = True
                        break
            
            if placed:
                break
                
            # Créer une nouvelle étagère (si possible)
            if not placed:
                if current_y + h <= container_height and w <= container_width:
                    shape.x = 0
                    shape.y = current_y
                    
                    if not check_collision(shape, placed_shapes):
                        new_shelf = (h, [shape], current_y)
                        shelves.append(new_shelf)
                        placed_shapes.append(shape)
                        current_y += h
                        placed = True
                        break

    # Affichage des résultats (amélioré)
    print("\n=== RESULT FROM ALGORITHM ===")
    for i, shelf in enumerate(shelves):
        shelf_height, shelf_shapes, shelf_y = shelf
        print(f"Shelf {i+1} (height={shelf_height}, y={shelf_y}):")
        for shape in shelf_shapes:
            bbox = shape.get_bounding_box()
            print(f"  {type(shape).__name__} at ({shape.x},{shape.y}) "
                  f"size={bbox[0]}x{bbox[1]} rotation={shape.rotation}")

    return [shelf[1] for shelf in shelves]


def nfdh(shapes, container_width, container_height):
    """Next-Fit Decreasing Height algorithm"""
    sorted_shapes = sorted(shapes, key=lambda s: max(s.get_bounding_box()), reverse=True)
    
    shelves = []
    current_shelf = []
    current_y = 0
    current_shelf_height = 0
    
    for shape in sorted_shapes:
        w, h = shape.get_bounding_box()
        
        # Try to place in current shelf
        shelf_width_used = sum(s[0] for s in current_shelf)
        
        if shelf_width_used + w <= container_width and current_shelf_height >= h:
            shape.x = shelf_width_used
            shape.y = current_y
            current_shelf.append((w, h, shape))
        else:
            # Start new shelf
            current_y += current_shelf_height
            current_shelf_height = h
            
            if current_y + h > container_height:
                continue  # Doesn't fit
                
            # Try all rotations
            best_rotation = None
            best_area = float('inf')
            
            for rotation in [0, math.pi/2, math.pi]:
                shape.rotation = rotation
                w, h = shape.get_bounding_box()
                
                if w <= container_width and current_y + h <= container_height:
                    area = w * h
                    if area < best_area:
                        best_area = area
                        best_rotation = rotation
            
            if best_rotation is not None:
                shape.rotation = best_rotation
                w, h = shape.get_bounding_box()
                shape.x = 0
                shape.y = current_y
                current_shelf = [(w, h, shape)]
                shelves.append(current_shelf)
                current_shelf_height = h
    
    return shelves


def best_fit(items, bin_capacity):
    bins = []
    for item in items:
        best_bin = None
        min_space = bin_capacity
        for bin in bins:
            space = bin_capacity - (sum(bin) + item)
            if 0 <= space < min_space:
                min_space = space
                best_bin = bin
        
        if best_bin is not None:
            best_bin.append(item)
        else:
            bins.append([item])
    return bins


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