def draw_packing(canvas, shelves, container_width, container_height, padding=20):
    """Draw the packing result on the canvas"""
    if not shelves:
        return
    
    # Calculate scale factor to fit in canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    scale_x = (canvas_width - 2 * padding) / container_width
    scale_y = (canvas_height - 2 * padding) / container_height
    scale = min(scale_x, scale_y)
    
    # Draw container
    canvas.create_rectangle(padding, padding,
                          padding + container_width * scale,
                          padding + container_height * scale,
                          outline="black", width=2)
    
    # Draw all shapes
    for shelf in shelves:
        for (w, h, shape) in shelf:
            shape.draw(canvas, scale)
    
    # Display container dimensions
    canvas.create_text(padding + 10, padding + 10,
                      text=f"{container_width}×{container_height}",
                      anchor="nw", fill="black")