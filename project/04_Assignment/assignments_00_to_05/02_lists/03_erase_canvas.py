# Implement an 'eraser' on a canvas.

# The canvas consists of a grid of blue 'cells' which are drawn as rectangles on the screen. We then create an eraser rectangle which, when dragged around the canvas, sets all of the rectangles it is in contact with to white.

from graphics import Canvas
import time

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

CELL_SIZE = 40
ERASE_SIZE = 20

def erase_objects(canvas, eraser):
    """Erase objects in contact with the eraser"""
    mouse_x = canvas.get_mouse_x()
    mouse_y = canvas.get_mouse_y()

    left_x = mouse_x
    top_y = mouse_y
    right_x = left_x + ERASE_SIZE
    bottom_y = top_y + ERASE_SIZE

    overlapping_objects = canvas.find_overlappng(left_x, top_y, right_x, bottom_y)

    for overlapping_object in overlapping_objects:

        if overlapping_object!= eraser:
            canvas.set_color(overlapping_object,'white')
def main():
    Canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    num_rows = CANVAS_HEIGHT // CELL_SIZE
    num_cols = CANVAS_WIDTH // CELL_SIZE

    for row in range(num_rows):
        for col in range(num_cols):
            left_x = col * CELL_SIZE
            top_y = row * CELL_SIZE
            right_x= left_x +CELL_SIZE
            bottom_y = top_y + CELL_SIZE

            cell = canvas.create_rangtangle(left_x, top_y ,right_x , bottom_y )

    canvas.wait_forclick()

    last_click_x, last_click_y = canvas.get_last_click()

    erase = canvas.create_rectangle(
        last_click_x,
        last_click_y,
        last_click_x + ERASE_SIZE,
        last_click_y + ERASE_SIZE,
        'pink'
    )

    while True:
        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()
        canvas.moveto(erase, mouse_x , mouse_y)

        erase_objects(canvas, erase)
        time.sleep(0.05)


if __name__ =='__main__':
    main()