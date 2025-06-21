def draw_packing(canvas, shelves, container_width, container_height):
    """Draw the packing solution on the canvas"""
    scale = 15  # Scaling factor for visualization
    
    # Draw container
    canvas.create_rectangle(
        10, 10, 
        10 + container_width * scale, 
        10 + container_height * scale,
        outline="black", width=2
    )
    
    # Draw packed rectangles
    colors = ["#4a6fa5", "#166088", "#4fc3f7", "#59a5d8", "#386fa4"]
    
    for i, shelf in enumerate(shelves):
        for rect in shelf:
            x, y, w, h = rect
            color = colors[i % len(colors)]
            
            canvas.create_rectangle(
                10 + x * scale, 
                10 + y * scale,
                10 + (x + w) * scale,
                10 + (y + h) * scale,
                fill=color, outline="black"
            )
            
            # Display rectangle dimensions
            canvas.create_text(
                10 + (x + w/2) * scale,
                10 + (y + h/2) * scale,
                text=f"{w}x{h}", fill="white"
            )
    
    # Add legend
    canvas.create_text(
        10 + container_width * scale + 20,
        30,
        text=f"Container: {container_width}x{container_height}",
        anchor="w", font=("Arial", 10)
    )
    
    packed_count = sum(len(shelf) for shelf in shelves)
    canvas.create_text(
        10 + container_width * scale + 20,
        50,
        text=f"Packed: {packed_count} rectangles",
        anchor="w", font=("Arial", 10)
    )