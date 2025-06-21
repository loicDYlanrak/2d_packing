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
    
    def intersects(self, other):
        x1, y1 = self.x, self.y
        w1, h1 = self.get_bounding_box()
        
        x2, y2 = other.x, other.y
        w2, h2 = other.get_bounding_box()
        
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

class Circle(Shape):
    def __init__(self, radius, x=0, y=0, rotation=0):
        super().__init__(x, y, rotation)
        self.radius = radius
    
    def get_bounding_box(self):
        # Circle's bounding box is always the same regardless of rotation
        return (2 * self.radius, 2 * self.radius)
    
    def draw(self, canvas, scale=1):
        # For circle, scale affects the radius
        x0 = self.x
        y0 = self.y
        x1 = self.x + 2 * self.radius * scale
        y1 = self.y + 2 * self.radius * scale
        canvas.create_oval(x0, y0, x1, y1, outline="black", fill="lightblue", width=1)

    def intersects(self, other):
        x1, y1 = self.x, self.y
        w1, h1 = self.get_bounding_box()
        
        x2, y2 = other.x, other.y
        w2, h2 = other.get_bounding_box()
        
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)


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
        if self.rotation == 0 or self.rotation == math.pi:
            w = self.width * scale
            h = self.height * scale
        else:  # π/2 rotation
            w = self.height * scale
            h = self.width * scale
        
        canvas.create_rectangle(
            self.x, self.y,
            self.x + w, self.y + h,
            outline="black", fill="lightgreen", width=1
        )

    def intersects(self, other):
        x1, y1 = self.x, self.y
        w1, h1 = self.get_bounding_box()
        
        x2, y2 = other.x, other.y
        w2, h2 = other.get_bounding_box()
        
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)


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
        if self.rotation == 0:
            points = [
                self.x, self.y + self.height * scale,
                self.x + self.base * scale, self.y + self.height * scale,
                self.x + (self.base * scale) / 2, self.y
            ]
        elif self.rotation == math.pi/2:
            points = [
                self.x, self.y + (self.height * scale) / 2,
                self.x + self.height * scale, self.y,
                self.x + self.height * scale, self.y + self.base * scale
            ]
        elif self.rotation == math.pi:
            points = [
                self.x, self.y,
                self.x + self.base * scale, self.y,
                self.x + (self.base * scale) / 2, self.y + self.height * scale
            ]
        
        canvas.create_polygon(points, outline="black", fill="pink", width=1)
        
    def intersects(self, other):
        x1, y1 = self.x, self.y
        w1, h1 = self.get_bounding_box()
        
        x2, y2 = other.x, other.y
        w2, h2 = other.get_bounding_box()
        
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)
