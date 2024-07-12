import cv2
import numpy as np

class TicTacToeDetector:
    def __init__(self):
        self.tic_tac_toe_board = [['-' for _ in range(3)] for _ in range(3)]
        self.roi_top_left = (90, 40)  # Adjust these coordinates as needed
        self.roi_bottom_right = (550, 450)  # Adjust these coordinates as needed
        self.cell_width = 145 # Adjust as needed
        self.cell_height = 145  # Adjust as needed

    # Get the current state of the board
    def get_board(self):
        return self.tic_tac_toe_board
    
    def print_board(self):
        print("Tic Tac Toe Board:")
        for row in self.tic_tac_toe_board:
            print(row)
    
    def process_image(self, image):
        # Your image processing logic here
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return processed_image

    def enhanced_edge_detection(self, image, min_threshold=50, max_threshold=150, aperture_size=3):
        # Your enhanced edge detection logic here
        blurred = cv2.GaussianBlur(
            image,
            (5, 5),  # Kernel size (width and height)
            1.0  # Gaussian kernel standard deviation in X direction
        )
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        thresholded = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        edges = cv2.Laplacian(thresholded, cv2.CV_8U, ksize=5)
        return edges

    def detect_circles(self, image):
        # TODO: Make parameters adjustable through a config file
        # Your circle detection logic here
        circles = cv2.HoughCircles(
            image,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=54,
            param1=90,
            param2=30,
            minRadius=20,
            maxRadius=70
        )

        if circles is not None:
            
            circles = np.round(circles[0, :]).astype("int")

            # Create a set to store the current state of the board
            current_board_state = set()

            for (x, y, r) in circles:
                # Adjust the coordinates based on the ROI
                x += self.roi_top_left[0]
                y += self.roi_top_left[1]

                # Calculate grid cell indices
                i = int((y - self.roi_top_left[1]) / self.cell_height)
                j = int((x - self.roi_top_left[0]) / self.cell_width)

                # Check if indices are within the valid range
                if 0 <= i < 3 and 0 <= j < 3:
                    current_board_state.add((i, j))

            # Check if the current state is different from the previous state
            if current_board_state != set([(i, j) for i, row in enumerate(self.tic_tac_toe_board) for j, val in enumerate(row) if val == 'O']):
                # Update the board and print the updated state
                self.tic_tac_toe_board = [['-' for _ in range(3)] for _ in range(3)]
                for i, j in current_board_state:
                    self.tic_tac_toe_board[i][j] = 'O'

        return circles

    def detect_grid(self, image, original_image):
        # Draw circles within the region of interest (ROI)
        roi_circles = self.detect_circles(image[self.roi_top_left[1]:self.roi_bottom_right[1], self.roi_top_left[0]:self.roi_bottom_right[0]])
        if roi_circles is not None:
            for (x, y, r) in roi_circles:
                # Adjust the coordinates based on the ROI
                x += self.roi_top_left[0]
                y += self.roi_top_left[1]

                cv2.circle(original_image, (x, y), r, (0, 0, 255), 4)
                cv2.rectangle(original_image, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)

        # Draw the grid box
        cv2.rectangle(original_image, self.roi_top_left, self.roi_bottom_right, (0, 255, 0), 2)

        # Draw numbers on the grid
        for i in range(3):
            for j in range(3):
                cell_x = self.roi_top_left[0] + j * self.cell_width
                cell_y = self.roi_top_left[1] + i * self.cell_height
                number = i * 3 + j + 1

                # Adjust text size
                font_size = 0.8
                cv2.putText(original_image, str(number), (cell_x + 10, cell_y + 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), 2, cv2.LINE_AA)

                # Adjust rectangle size
                rect_width = self.cell_width
                rect_height = self.cell_height
                cv2.rectangle(original_image, (cell_x, cell_y), (cell_x + rect_width, cell_y + rect_height), (255, 0, 0), 2)

        return original_image
'''
In order to test the detection module without using it as a module. This should only be used with pictures.

# Example usage
if __name__ == "__main__":
    # Create an instance of the TicTacToeDetector
    detector = TicTacToeDetector()

    # List of image paths
    image_paths = ["images/image1.jpeg", "images/image2.jpeg", "images/image3.jpeg", "images/image4.jpeg"]

    for image_path in image_paths:
        # Load the image
        image = cv2.imread(image_path)

        # Process the image and detect circles, grid, and numbers
        processed_image = detector.process_image(image)
        final_image = detector.detect_grid(processed_image, image.copy())

        # Print the Tic Tac Toe board
        detector.print_board()

        # Convert processed_image to three dimensions
        processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)

        # Display the current processed image and Tic-Tac-Toe board state
        cv2.imshow('Tic Tac Toe', np.hstack((processed_image_rgb, final_image)))

        # Press any key to proceed to the next image
        cv2.waitKey(0)

    # Release the OpenCV window
    cv2.destroyAllWindows()
    '''
