import math


def metric_line_length(position: int) -> float:
    if position % 10 == 0:
        line_length = 2
    elif position % 5 == 0:
        line_length = 1
    else:
        line_length = 0
    return line_length


def inch_to_mm(inch: float) -> float:
    return inch * 25.4


def imperial_line_length(position: int) -> float:
    inch_space = 0.025
    if position % 16 == 0:
        multiplier = 5
    elif position % 8 == 0:
        multiplier = 4
    elif position % 4 == 0:
        multiplier = 3
    elif position % 2 == 0:
        multiplier = 2
    else:
        multiplier = 1
    return inch_to_mm(inch_space * multiplier)


def ruler(
    length: int,
    start_x: float = 0,
    start_y: float = 0,
    skip: int = 0,
    length_multiplier: float = 1,
    move_length: float = 1,
    is_horizontal: bool = False,
    line_len_func=metric_line_length,
):
    path = [start(x=start_x, y=start_y)]
    for i in range(length):
        if i >= skip:
            path.append(
                line(
                    length=length_multiplier * line_len_func(i),
                    is_horizontal=is_horizontal,
                )
            )
        path.append(
            move(
                length=move_length,
                is_horizontal=is_horizontal,
            )
        )
    path.append(
        line(
            length=length_multiplier * line_len_func(i + 1),
            is_horizontal=is_horizontal,
        )
    )

    path_string = " ".join(path)
    return path_string


def imperial_rulers():
    card_horizontal = 85
    card_vertical = 54
    top_right = start(87.75, 3, absolute=True)
    imperial_move_length = inch_to_mm(1) / 16
    top_ruler = ruler(
        length=16 * 3 + 5,
        line_len_func=imperial_line_length,
        move_length=-imperial_move_length,
    )
    right_ruler = ruler(
        length=16 * 2 + 1,
        skip=1,
        is_horizontal=True,
        length_multiplier=-1,
        move_length=imperial_move_length,
        line_len_func=imperial_line_length,
    )
    bot_ruler = ruler(
        length=16 * 3 + 2,
        start_x=-3,
        start_y=card_vertical,
        length_multiplier=-1,
        move_length=-imperial_move_length,
        line_len_func=imperial_line_length,
    )
    path_string = "\n".join(
        (
            top_right,
            top_ruler,
            top_right,
            right_ruler,
            top_right,
            bot_ruler,
        )
    )
    print("imperial rulers")
    print(path_string)


def metric_rulers():
    card_horizontal = 85
    card_vertical = 54
    top_left = start(x=2.25, y=3, absolute=True)
    top_ruler = ruler(length=80, start_x=3, skip=1)
    left_ruler = ruler(
        length=53,
        start_y=card_vertical,
        skip=1,
        is_horizontal=True,
        move_length=-1,
    )
    bot_ruler = ruler(
        length=85,
        start_y=card_vertical,
        skip=3,
        length_multiplier=-1,
    )
    path_string = "\n".join(
        (top_left, top_ruler, top_left, left_ruler, top_left, bot_ruler)
    )
    print("metric rulers")
    print(path_string)


def start(x: float, y: float, absolute=False,) -> str:
    move_command = "m"
    if absolute:
        move_command = move_command.upper()
    return f"{move_command} {x},{y}"


def line(length: float, is_horizontal: bool,) -> str:
    direction = "h" if is_horizontal else "v"
    return f"{direction} {length} z"


def move(length: float, is_horizontal: bool = False,) -> str:
    if is_horizontal:
        return f"m 0,{length}"
    else:
        return f"m {length},0"
    

def move_rel(x: float, y: float,) -> str:
    return f"m {x},{y}"


def line_to(x: float, y: float,) -> str:
    return f"l {x},{y}"


def circle_markings(
    radius: float,
    num_markings: int,
    line_length: float = 0.5,
    start_degree: float = 0,
    start_x: float = 0,
    start_y: float = 0,
):
    start_pos = (start_x, start_y)
    svg_path = [start(*start_pos, absolute=True)]

    marking_absolute_start_positions = []
    marking_absolute_end_positions = []
    for i in range(num_markings):
        angle_deg = start_degree + i * (360 // num_markings)
        # start from the top
        angle_deg -= 90
        angle_rad = math.radians(angle_deg)

        x1 = radius * math.cos(angle_rad)
        y1 = radius * math.sin(angle_rad)
        marking_absolute_start_positions.append((x1, y1))

        x2 = (radius + line_length) * math.cos(angle_rad)
        y2 = (radius + line_length) * math.sin(angle_rad)
        marking_absolute_end_positions.append((x2, y2))

    last = (0, 0)
    marking_relative_move_positions = []
    marking_relative_draw_positions = []
    for abs_move_to, abs_draw_to in zip(
        marking_absolute_start_positions, marking_absolute_end_positions
    ):
        last_x, last_y = last
        move_x, move_y = abs_move_to
        marking_relative_move_positions.append((move_x - last_x, move_y - last_y))

        draw_x, draw_y = abs_draw_to
        marking_relative_draw_positions.append((draw_x - move_x, draw_y - move_y))

        last = abs_draw_to

    marking_relative_move_positions = [
        (round(x, 3), round(y, 3)) for x, y in marking_relative_move_positions
    ]
    marking_relative_draw_positions = [
        (round(x, 3), round(y, 3)) for x, y in marking_relative_draw_positions
    ]

    for rel_move_to, rel_draw_to in zip(
        marking_relative_move_positions,
        marking_relative_draw_positions,
    ):
        svg_path.append(move_rel(*rel_move_to))
        svg_path.append(line_to(*rel_draw_to))

    svg_path.append("z")
    return " ".join(svg_path)


def two_dollar_circle_markings():
    print("$2/36:")
    degree = 36
    num_markings = 360 // degree
    diameter = 20.350
    print(
        circle_markings(
            radius=diameter / 2,
            num_markings=num_markings,
            start_x=45.475,
            start_y=28.125,
            # start_degree=degree//2
        )
    )


def one_dollar_circle_markings():
    print("$1/15:")
    num_markings = 360 // 15
    radius = 12.45
    print(
        circle_markings(
            radius=radius,
            num_markings=num_markings,
        )
    )


def curve(radius: float, is_horizontal: bool = True,) -> str:
    control_point = f"{radius}, 0" if is_horizontal else f"0, {radius}"
    return f"q {control_point}, {radius},{radius}"


def wrench():
    start_x = 6.8
    start_y = 7
    width = 77.45
    height = 14.7
    thickness = 0.75
    curve_outer = 1.75
    curve_inner = 0.5
    width_outer = width - curve_outer
    height_outer = height - curve_outer
    height_inner = height - thickness - curve_inner
    width_inner = width - thickness - curve_inner
    svg_path = [
        start(start_x, start_y, absolute=True),
        line_to(width_outer, 0),
        curve(curve_outer),
        line_to(0, height_outer),
        line_to(-thickness, 0),
        line_to(0, -height_inner),
        curve(-curve_inner, is_horizontal=False),
        line_to(-width_inner, 0),
        line_to(0, -thickness),
        "z",
    ]
    print("wrench:")
    print(" ".join(svg_path))


def print_card_paths():
    two_dollar_circle_markings()
    one_dollar_circle_markings()
    metric_rulers()
    imperial_rulers()
    wrench()


if __name__ == "__main__":
    print_card_paths()
