import cv2
import numpy as np

# Global variables
img = None
params = {
    'drawing': False,
    'start_x': -1,
    'start_y': -1,
    'end_x': -1,
    'end_y': -1,
    'rect': None
}


def load_image():
    global img
    img = cv2.imread("../img/img_3.png")
    if img is None:
        raise ValueError("Could not load the image. Please check the path.")
    return img


def traitement():
    global img
    if params['rect'] is not None:
        # Create a mask based on the selected rectangle
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        x1, y1 = min(params['start_x'], params['end_x']), min(params['start_y'], params['end_y'])
        x2, y2 = max(params['start_x'], params['end_x']), max(params['start_y'], params['end_y'])
        mask[y1:y2, x1:x2] = 255

        # Create a darkened version of the image
        darkened_img = img.copy()
        darkened_img = cv2.addWeighted(darkened_img, 0.3, np.zeros_like(darkened_img), 0, 0)

        # Use the mask to keep the selected person's original colors
        result = darkened_img.copy()
        result[mask > 0] = img[mask > 0]

        # Show the result
        cv2.imshow('img', result)


def select_region(event, x, y, flags, param):
    global img

    if event == cv2.EVENT_LBUTTONDOWN:
        params['drawing'] = True
        params['start_x'], params['start_y'] = x, y
        params['end_x'], params['end_y'] = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if params['drawing']:
            imgbis = img.copy()
            params['end_x'], params['end_y'] = x, y
            # Draw rectangle preview
            cv2.rectangle(imgbis,
                          (params['start_x'], params['start_y']),
                          (params['end_x'], params['end_y']),
                          (0, 255, 0), 2)
            cv2.imshow('InvSelect', imgbis)

    elif event == cv2.EVENT_LBUTTONUP:
        params['drawing'] = False
        params['end_x'], params['end_y'] = x, y
        params['rect'] = True
        # Draw final rectangle
        cv2.rectangle(img.copy(),
                      (params['start_x'], params['start_y']),
                      (params['end_x'], params['end_y']),
                      (0, 255, 0), 2)
        traitement()


def main():
    global img
    try:
        # Load the image
        img = load_image()

        # Create windows
        cv2.namedWindow('InvSelect')
        cv2.imshow('InvSelect', img)

        # Mouse callback for rectangle selection
        cv2.setMouseCallback('InvSelect', select_region)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Press 'Esc' to exit
                break
            elif key == ord('r'):  # Press 'r' to reset
                params['rect'] = None
                img = load_image()
                cv2.imshow('InvSelect', img)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()