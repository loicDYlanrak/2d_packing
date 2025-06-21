import math

class Shape:
    def __init__(self, x=0, y=0, rotation=0):
        self.x = x
        self.y = y
        self.rotation = rotation  # 0, π/2, π
    
    def rotate(self):
        """Rotate the shape by π/2"""
        self.rotation = (self.rotation + math.pi/2) % math.pi
    
    def get_bounding_box(self):
        """Return the width and height of the shape's bounding box"""
        raise NotImplementedError
    
    def draw(self, canvas, scale=1):
        """Draw the shape on the canvas"""
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius, x=0, y=0, rotation=0):
        super().__init__(x, y, rotation)
        self.radius = radius
    
    def get_bounding_box(self):
        # Circle's bounding box is always the same regardless of rotation
        return (2 * self.radius, 2 * self.radius)
    
    def draw(self, canvas, scale=1):
        x, y = self.x * scale, self.y * scale
        radius = self.radius * scale
        canvas.create_oval(x - radius, y - radius, 
                          x + radius, y + radius,
                          outline="black", fill="lightblue")

class Rectangle(Shape):
    def __init__(self, width, height, x=0, y=0, rotation=0):
        super().__init__(x, y, rotation)
        self.width = width
        self.height = height
    
    def get_bounding_box(self):
        if self.rotation == 0 or self.rotation == math.pi:
            return (self.width, self.height)
        else:  # π/2 rotation
            return (self.height, self.width)
    
    def draw(self, canvas, scale=1):
        w, h = self.get_bounding_box()
        x, y = self.x * scale, self.y * scale
        canvas.create_rectangle(x, y, 
                              x + w * scale, y + h * scale,
                              outline="black", fill="lightgreen")

class IsoscelesTriangle(Shape):
    def __init__(self, base, height=None, x=0, y=0, rotation=0):
        super().__init__(x, y, rotation)
        self.base = base
        self.height = height if height is not None else base * math.sqrt(3) / 2  # Default to equilateral
    
    def get_bounding_box(self):
        if self.rotation == 0 or self.rotation == math.pi:
            return (self.base, self.height)
        else:  # π/2 rotation
            return (self.height, self.base)
    
    def draw(self, canvas, scale=1):
        w, h = self.get_bounding_box()
        x, y = self.x * scale, self.y * scale
        
        if self.rotation == 0:
            points = [x, y + h * scale, 
                     x + w * scale, y + h * scale,
                     x + w * scale / 2, y]
        elif self.rotation == math.pi/2:
            points = [x, y + h * scale / 2,
                     x + w * scale, y,
                     x + w * scale, y + h * scale]
        elif self.rotation == math.pi:
            points = [x, y,
                     x + w * scale, y,
                     x + w * scale / 2, y + h * scale]
        
        canvas.create_polygon(points, outline="black", fill="pink")