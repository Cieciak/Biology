
type RGB = tuple[int, int, int]

def tkiner_color(rgb: RGB): return '#{:02x}{:02x}{:02x}'.format(*rgb)
