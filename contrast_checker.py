def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    values = []

    for value in rgb:
        channel = value / 255

        if channel <= 0.03928:
            values.append(channel / 12.92)
        else:
            values.append(((channel + 0.055) / 1.055) ** 2.4)

    return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]


def contrast_ratio(color1, color2):
    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)


def accessibility_report(text_color, background_color):
    ratio = contrast_ratio(text_color, background_color)

    print(f"Text color: {text_color}")
    print(f"Background color: {background_color}")
    print(f"Contrast ratio: {ratio:.2f}:1")

    if ratio >= 4.5:
        print("Result: Passes basic accessibility contrast for normal-sized text.")
    else:
        print("Result: Possible accessibility issue. Increase contrast between text and background.")


accessibility_report("#777777", "#FFFFFF")
