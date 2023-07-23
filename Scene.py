from manim import *
import colorsys


# Function to convert RGB values to hexadecimal color representation

# Create a scene that animates moving vertices in a graph
class MovingVertices(Scene):
    def __init__(self, N=2, EDGES=None, LAY="shell", GRAD= False, GS=None, GE=None ,**kwargs):
        self.N = N
        self.EDGES = EDGES
        self.LAY = LAY
        self.gs=GS
        self.gradient=GRAD
        self.ge=GE
        super().__init__(**kwargs)

    parent = []
    dict = {}
    SetSize = []
    colors = []

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    # Function to generate a list of vibrant colors based on the number 'n'
    def generate_vibrant_colors(self, n):
        colors = []
        hue_values = [i / n for i in range(n)]
        saturation = 0.9
        value = 0.9

        # Convert each HSV value to RGB and then to hexadecimal color
        for hue in hue_values:
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            hex_color = self.rgb_to_hex((r, g, b))
            colors.append(hex_color)

        return colors

    # Function to generate a list of vibrant colors in gradiant based on the number 'n'
    def generate_gradient_colors(self,n, start_color='#00FFFF', end_color='#FF0000'):
        colors = []
        start_h, start_s, start_v = colorsys.rgb_to_hsv(int(start_color[1:3], 16),
                                                        int(start_color[3:5], 16),
                                                        int(start_color[5:7], 16))
        end_h, end_s, end_v = colorsys.rgb_to_hsv(int(end_color[1:3], 16),
                                                  int(end_color[3:5], 16),
                                                  int(end_color[5:7], 16))

        for i in range(n):
            t = i / (n - 1)  # Interpolation factor from 0 to 1
            current_h = start_h + t * (end_h - start_h)
            r, g, b = colorsys.hsv_to_rgb(current_h, start_s, start_v)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            hex_color = self.rgb_to_hex((r, g, b))
            colors.append(hex_color)

        return colors
    # Function to find the parent of a set using path compression
    def find(self, v):
        if self.parent[v] == v:
            return v
        self.parent[v] = self.find(self.parent[v])  # Path compression
        return self.parent[v]

    # Function to perform union of two sets using rank-based optimization
    def union__(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.SetSize[a] < self.SetSize[b]:
            a, b = b, a
        self.parent[b] = a
        self.SetSize[a] += self.SetSize[b]

    def construct(self):
        n = self.N
        edges = self.EDGES
        layout = self.LAY
        if edges is None:
            edges = [(1, 2)]
        vertices = [i for i in range(n)]
        if self.gradient:
            self.colors = self.generate_gradient_colors(n,self.gs,self.ge)
        else: self.colors = self.generate_vibrant_colors(n)
        self.parent = [i for i in range(n)]  # Initialize self.parent list to track sets
        vertex_color = {i: {"fill_color": self.colors[i]} for i in range(n)}  # Initialize color dictionary for vertices
        self.SetSize = [1] * n  # Initialize list to store set sizes

        # Create the initial graph with colored vertices
        g = Graph(vertices=vertices, edges=edges, labels=True, layout=layout, vertex_config=vertex_color)
        self.play(Create(g))
        self.wait()

        # Animation to merge sets and update vertex and edge colors
        for i in edges:
            self.union__(i[0], i[1])  # Merge sets of the two vertices connected by the edge
            for j in range(n):
                self.colors[j] = self.colors[self.find(j)]  # Update colors based on the new sets after union
            vertex_color = {}
            vertex_color = {ij: {"fill_color": self.colors[ij]} for ij in range(n)}  # Update vertex colors
            edge_color = {}
            edge_color = {e: {"stroke_color": self.colors[e[0]] if self.colors[e[0]] == self.colors[e[1]] else WHITE}
                          for e in edges}
            edge_color.update({(i[0], i[1]): {"stroke_color": YELLOW}})  # Highlight the edge being merged

            # Perform animation to transform the graph with updated colors
            self.play(Transform(g, Graph(
                vertices=vertices, edges=edges, labels=True, layout=layout,
                vertex_config=vertex_color,
                edge_config=edge_color
            )))
            self.wait()
