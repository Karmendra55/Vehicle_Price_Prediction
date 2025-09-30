import webcolors
import math
import streamlit as st

CSS3_NAMES_TO_HEX = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgreen": "#006400",
    "darkgrey": "#a9a9a9",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "grey": "#808080",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32"
}

def color_name(requested_hex):
    """
    Convert a hex color code to its closest CSS3 color name.

    This function attempts to find a direct CSS3 color name match for a given
    hex color code. If no exact match is found, it calculates the Euclidean
    distance in RGB space between the requested color and all CSS3 colors.

    Parameters
    ----------
    requested_hex : str
        Hexadecimal color code (e.g., "#ff5733" or "ff5733").

    Returns
    -------
    str
        The name of the closest CSS3 color, with title casing.
    """
    try:
        return webcolors.hex_to_name(requested_hex).title()
    except ValueError:
        requested_rgb = webcolors.hex_to_rgb(requested_hex)
        min_colors = {}

        for name, hex_code in CSS3_NAMES_TO_HEX.items():
            r, g, b = webcolors.hex_to_rgb(hex_code)
            distance = math.sqrt(
                (r - requested_rgb.red) ** 2 +
                (g - requested_rgb.green) ** 2 +
                (b - requested_rgb.blue) ** 2
            )
            min_colors[distance] = name

        return min_colors[min(min_colors.keys())].title()
    
def get_contrast_color(hex1, hex2):
    """
    Determine a contrasting text color (black or white) based on two background colors.

    This function computes the average luminance of two given hexadecimal colors
    and returns either black ("#000000") or white ("#ffffff") to ensure optimal
    contrast and readability.

    Parameters
    ----------
    hex1 : str
        First hexadecimal color code (e.g., "#ffffff").
    hex2 : str
        Second hexadecimal color code (e.g., "#000000").

    Returns
    -------
    str
        Either "#000000" (black) or "#ffffff" (white), depending on which provides
        better contrast against the average luminance of the two colors.

    """
    def luminance(hex_color):
        rgb = webcolors.hex_to_rgb(hex_color)
        # --- Standard formula for relative luminance ---
        return 0.299*rgb.red + 0.587*rgb.green + 0.114*rgb.blue

    avg_lum = (luminance(hex1) + luminance(hex2)) / 2
    return "#000000" if avg_lum > 128 else "#ffffff"

def card_style():
    CARD_STYLE = """
    <style>
    .card {
        background: #000000;
        border-radius: 60px;
        padding: 5px;
        padding-top: 15px;
        padding-left: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border-style: solid;
        border-color: #ff4b4b;
    }
    .title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
        color: #ff4b4b;
    }
    .card h3 {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
        color: #ff4b4b;
    }
    .stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
    }
    .stat {
        background: linear-gradient(135deg, #f5f7fa, #e6ebf2);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
    }
    .stat h4 {
        font-size: 16px;
        color: #ff4b4b;
        margin-bottom: 5px;
    }
    .stat p {
        font-size: 20px;
        font-weight: 600;
        color: #34495e;
    }
    </style>
    """
    st.markdown(CARD_STYLE, unsafe_allow_html=True)
    
    return CARD_STYLE