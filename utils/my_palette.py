from matplotlib.colors import LinearSegmentedColormap

def get_my_palette(n=None, group=None, as_dict=False):
    """
    Returns color palette for the project.
    """
    my_palette = {
        'Cornflower': ['#dce8ff', '#bcd6fa', '#9ec0f7', '#7da7f2', '#6495ED'],
        'Lime Green': ['#EEFF99', '#E2FF66', '#C8FF00', '#9AC400', '#7EA600'],
        'Tomato': ['#ffe0db', '#ffc2b5', '#ff9f88', '#ff7a5f', '#ff6347'],
        'Yellowsoft': ['#fff9db', '#fff1b8', '#ffe78f', '#ffdc60', '#ffd700'],
        'Lavender': ['#D9D6FF', '#BEB3FF', '#A18EFF', '#7E6BFF', '#5A4AE0'],
        'Neutral': ['#FFFFFF', '#FAFAFA', '#E6E6E6', '#CCCCCC', '#999999'],
    }

    if as_dict:
        return my_palette

    if group:
        if group not in my_palette:
            raise ValueError(f'Unknown group {group}. Choose from {list(my_palette.keys())}.')
        colors = my_palette[group]
    else:
        colors = [color for group_colors in my_palette.values() for color in group_colors]

    if n is not None:
        return colors[:n]

    return colors

cmap_cornflower = LinearSegmentedColormap.from_list('cornflower', get_my_palette(group='Cornflower'))
cmap_lime = LinearSegmentedColormap.from_list('lime', get_my_palette(group='Lime Green'))
cmap_tomato = LinearSegmentedColormap.from_list('tomato', get_my_palette(group='Tomato'))
cmap_yellow = LinearSegmentedColormap.from_list('yellowsoft', get_my_palette(group='Yellowsoft'))
cmap_lavender = LinearSegmentedColormap.from_list('lavender', get_my_palette(group='Lavender'))
