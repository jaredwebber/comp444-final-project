from utils import get_coords
import turtle
import io
from PIL import Image


class WallMapper:
    def __init__(self) -> None:
        pass

    def process_data(self, data: list, output_name: str) -> None:
        point_map = {}

        turtle.setup(1200, 700)

        for i in range(len(data)):
            point_map[i] = data[i]

        x, y = get_coords(0, point_map[1])
        turtle.penup()
        turtle.setposition(x, y)
        turtle.pendown()

        angle = 0.5
        for i in range(2, 722):
            x, y = get_coords(angle, point_map[i])
            # print(f"{x}, {y}")
            turtle.goto(x, y)
            angle += 0.5

        turtle.hideturtle()
        self._save_image(filename=output_name)
        # turtle.done

    def _save_image(self, filename="./output.png"):
        ps = turtle.getscreen().getcanvas().postscript(colormode="color")
        im = Image.open(io.BytesIO(ps.encode("utf-8")))
        im.save(filename, format="PNG")
