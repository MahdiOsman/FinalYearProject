# NAO SDK
from naoqi import ALProxy
# OpenCV
import cv2
# NumPy
import numpy as np
# TicTacToeDetector class
from detection import TicTacToeDetector
import copy
import minimax

class TicTacToeGame:
    def __init__(self, ip_address, port_number):
        # CAMERA SUB NAME
        self._camera_sub = "test2"
        
        # Initialize NAOQI proxies
        awareness_proxy = ALProxy("ALBasicAwareness", ip_address, port_number)
        motion_proxy = ALProxy("ALMotion", ip_address, port_number)
        posture_proxy = ALProxy("ALRobotPosture", ip_address, port_number)
        behavior_manager_proxy = ALProxy("ALBehaviorManager", ip_address, port_number)
        # Initialize NAOQI proxy for image acquisition
        self.camera_proxy = ALProxy("ALVideoDevice", ip_address, port_number)
        # tts
        self.tts = ALProxy("ALTextToSpeech", ip_address, port_number)
        self.tts.setVolume(1.9) # NAO Speech Volume 0.0-1.0
        
        
        #life_proxy = ALProxy("ALAutonomousLife", ip_address, port_number)
        #life_proxy.setState("disabled")
        
        # Go to position
        #posture_proxy.goToPosture("Stand", 0.5) 
        posture_proxy.goToPosture("Sit", 0.5) 
        #posture_proxy.goToPosture("StandZero", 0.5) 
        
        
        # TODO: Still need to move the arm to each cell per move, 
        # got to make sure the paper is correctly places,
        # remeber to turn off autonomous mode
        # Set the joint angles to extend the arm forward
        #joint_names = ["RShoulderPitch", "RElbowYaw", "RElbowRoll"]
        #joint_angles = [0.34, 1.65, 0]
        #speed = 0.1 
        #motion_proxy.setAngles(joint_names, joint_angles, speed)
        
        
        # Set the head position to center
        motion_proxy.setAngles("HeadYaw", 0, 0.1)  # Center the head horizontally
        # DEFAULT VALUE: -0.12 (for whiteboard)
        motion_proxy.setAngles("HeadPitch", -0.35, 0.1)  # Look at the board down
        
        # Set stiffness to 1.0 for all joints
        stiffness_value = 1.0
        joint_names = "Body"
        motion_proxy.stiffnessInterpolation(joint_names, stiffness_value, 1.0)

        # Set L/R stiffness to 0.0
        #stiffness_values = [0.0, 0.0, 0.0, 0.0, 0.0]
        #joint_names = ["RHand", "RElbowYaw", "RElbowRoll", "RShoulderRoll", "RShoulderPitch"]
        #motion_proxy.stiffnessInterpolation(joint_names, stiffness_values, 1.0)
                
        # Stop all running behaviors
        behavior_manager_proxy.stopAllBehaviors()                
        # Stop awareness mode
        awareness_proxy.stopAwareness()

        # CAMERA CONFIG STUFF
        #top/bottom camera
        camera_pos = 1
        self.resolution = 2  # VGA
        self.color_space = 11  # RGB
        fps = 30 # fps
        
        self.video_client = self.camera_proxy.subscribeCamera(self._camera_sub, camera_pos, self.resolution, self.color_space, fps)

        # TICTACTOE DETECTOR
        # Create an instance of the TicTacToeDetector
        self.detector = TicTacToeDetector()
        
        # Board state
        self.current_board = [['-' for _ in range(3)] for _ in range(3)]
        self.previous_board = [['-' for _ in range(3)] for _ in range(3)]

    def acquire_image_from_nao(self):
        # Get image from NAO camera
        image_data = self.camera_proxy.getImageRemote(self.video_client)
        
        image_array = None
        # Convert image data to OpenCV format
        if image_data is not None:
            image_array = np.frombuffer(image_data[6], dtype=np.uint8).reshape((image_data[1], image_data[0], 3))

        return image_array
    
    def print_board(self):
        print("Tic Tac Toe Board:")
        for row in self.current_board:
            print(row)
            
    def update_previous_board(self):
        self.previous_board = copy.deepcopy(self.current_board)

    def join_boards(self, circles_board):
        # Iterate over each cell in the circles_board
        for i in range(3):
            for j in range(3):
                # If the circles_board contains an 'O' and the corresponding cell in self.board is not 'X', update self.board
                if circles_board[i][j] == 'O' and self.current_board[i][j] != 'X':
                    self.current_board[i][j] = 'O'
                    
    def check_winner(self):
        # Check if there is a winner
        if minimax.is_winner(self.current_board, 'X'):
            self.print_board()
            print("AI Won!")
            self.tts.say("Better luck next time, I win.")
            return 0
        elif minimax.is_winner(self.current_board, 'O'):
            self.print_board()
            print("You Won!")
            self.tts.say("Great Job! You win!")
            return 1
        else:
            return None
        
    def nao_playing_social(self):
        # Randomly say a random phrase
        # Randomise the phrases
        phrases = ["I am thinking...", "Let me think...", "Hmm...", "Umm...", "Let me see...", "I am thinking hard..."]
        phrase = np.random.choice(phrases)
        self.tts.say(phrase)
        
        # Wait 1 second MAYBE DOESNT WORK?!?!?!
        cv2.waitKey(1000)
        

    def play_game(self):
        # Player or AI goes first
        player_first = True
        if player_first == False:
            print("AI Move: ")
            ai_move = minimax.make_ai_move(self.current_board)
            print(ai_move)
            self.current_board[ai_move[0]][ai_move[1]] = 'X'
            self.print_board()
            self.update_previous_board()
            
            if ai_move[0] == 0 and ai_move[1] == 0:
                print("AI is moving to the top left grid.")
                self.tts.say("I am moving to the top left grid.")
            elif ai_move[0] == 0 and ai_move[1] == 1:
                print("AI is moving to the top middle grid.")
                self.tts.say("I am moving to the top middle grid.")
            elif ai_move[0] == 0 and ai_move[1] == 2:
                print("AI is moving to the top right grid.")
                self.tts.say("I am moving to the top right grid.")
            elif ai_move[0] == 1 and ai_move[1] == 0:
                print("AI is moving to the middle left grid.")
                self.tts.say("I am moving to the middle left grid.")
            elif ai_move[0] == 1 and ai_move[1] == 1:
                print("AI is moving to the center grid.")
                self.tts.say("I am moving to the center grid.")
            elif ai_move[0] == 1 and ai_move[1] == 2:
                print("AI is moving to the middle right grid.")
                self.tts.say("I am moving to the middle right grid.")
            elif ai_move[0] == 2 and ai_move[1] == 0:
                print("AI is moving to the bottom left grid.")
                self.tts.say("I am moving to the bottom left grid.")
            elif ai_move[0] == 2 and ai_move[1] == 1:
                print("AI is moving to the bottom middle grid.")
                self.tts.say("I am moving to the bottom middle grid.")
            elif ai_move[0] == 2 and ai_move[1] == 2:
                print("AI is moving to the bottom right grid.")
                self.tts.say("I am moving to the bottom right grid.")
        
        # Start the game loop
        while True:
            # Acquire image from NAO camera
            current_image = self.acquire_image_from_nao()

            # Process the image and detect circles
            processed_image = self.detector.process_image(current_image)
            final_image = self.detector.detect_grid(processed_image, current_image)
            
            # Get the current state of the board
            self.join_boards(self.detector.get_board())

            # Check if there is a winner
            if self.check_winner() is not None:
                break
            
            # If the state of the board is different from the previous state, print the board and apply logic
            if self.current_board != self.previous_board: 
                self.nao_playing_social()
                
                # Print the Tic Tac Toe board
                self.print_board()
                
                print("AI Move: ")
                ai_move = minimax.make_ai_move(self.current_board)
                print(ai_move)
                
                if ai_move is None:
                    # If AI won, print the board and break the loop
                    if minimax.is_winner(self.current_board, 'X'):
                        self.print_board()
                        print("AI Won!")
                        break
                    elif minimax.is_winner(self.current_board, 'O'):
                        self.print_board()
                        print("You Won!")
                        break
                    elif minimax.is_board_full(self.current_board):
                        self.tts.say("It's a tie!")
                        self.print_board()
                        print("It's a tie!")
                        break
                    else:
                        print("Error: AI Move is None.")
                        break
                    
                # TODO: Change this to the AIs actual move,
                # probably should start with getting the coordinates from image -> real life
                # then apply animation 'draw' to the corresponding grid
                # then once comepleted move back to the previous position to ensure board is visible
                # Say which grid the AI is going to move to
                if ai_move[0] == 0 and ai_move[1] == 0:
                    print("AI is moving to the top left grid.")
                    self.tts.say("I am moving to the top left grid.")
                elif ai_move[0] == 0 and ai_move[1] == 1:
                    print("AI is moving to the top middle grid.")
                    self.tts.say("I am moving to the top middle grid.")
                elif ai_move[0] == 0 and ai_move[1] == 2:
                    print("AI is moving to the top right grid.")
                    self.tts.say("I am moving to the top right grid.")
                elif ai_move[0] == 1 and ai_move[1] == 0:
                    print("AI is moving to the middle left grid.")
                    self.tts.say("I am moving to the middle left grid.")
                elif ai_move[0] == 1 and ai_move[1] == 1:
                    print("AI is moving to the center grid.")
                    self.tts.say("I am moving to the center grid.")
                elif ai_move[0] == 1 and ai_move[1] == 2:
                    print("AI is moving to the middle right grid.")
                    self.tts.say("I am moving to the middle right grid.")
                elif ai_move[0] == 2 and ai_move[1] == 0:
                    print("AI is moving to the bottom left grid.")
                    self.tts.say("I am moving to the bottom left grid.")
                elif ai_move[0] == 2 and ai_move[1] == 1:
                    print("AI is moving to the bottom middle grid.")
                    self.tts.say("I am moving to the bottom middle grid.")
                elif ai_move[0] == 2 and ai_move[1] == 2:
                    print("AI is moving to the bottom right grid.")
                    self.tts.say("I am moving to the bottom right grid.")
                # Apply the AI Move
                self.current_board[ai_move[0]][ai_move[1]] = 'X'
                
                # Print the board
                self.print_board()
                
                # Update the previous board
                self.update_previous_board()
                
            # Display the current processed image and Tic-Tac-Toe board state
            final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Tic Tac Toe', np.hstack((processed_image, final_image)))
            
            # wait for x seconds
            cv2.waitKey(800)
            
            # Press 'q' to exit the game loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        # Clean up 
        cv2.destroyAllWindows()
        self.camera_proxy.unsubscribe(self._camera_sub)
        
if __name__ == "__main__":
    game = TicTacToeGame("nao.local", 9559)
    
    # Start the game
    game.play_game()
