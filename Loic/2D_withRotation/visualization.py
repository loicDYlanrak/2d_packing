from shapes import Circle

def draw_packing(canvas, shelves, container_width, container_height, padding=20):
    """Draw the packing result on the canvas with proper scaling and centering"""
    canvas.delete("all")
    
    if not shelves:
        return
    
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    available_width = canvas_width - 2 * padding
    available_height = canvas_height - 2 * padding
    
    scale_x = available_width / container_width
    scale_y = available_height / container_height
    scale = min(scale_x, scale_y)
    
    offset_x = (canvas_width - container_width * scale) / 2
    offset_y = (canvas_height - container_height * scale) / 2
    
    canvas.create_rectangle(
        offset_x, 
        offset_y,
        offset_x + container_width * scale,
        offset_y + container_height * scale,
        outline="black", width=2, tags="container"
    )
    
    for shelf in shelves:
        for (shape) in shelf:
            shape.x = offset_x + shape.x * scale
            shape.y = offset_y + shape.y * scale
            
            original_scale = scale
            if isinstance(shape, Circle):
                original_scale = scale
            
            shape.draw(canvas, original_scale)
    
    canvas.create_text(
        offset_x + 10, 
        offset_y + 10,
        text=f"Container: {container_width}×{container_height}",
        anchor="nw", 
        fill="black",
        tags="info"
    )