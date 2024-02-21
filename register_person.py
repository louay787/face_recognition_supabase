import cv2
import os 




def create_folder_if_not_exists(folder_path):
    """
    Create a folder if it does not exist.

    Parameters:
    - folder_path (str): Path to the folder.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def capture_images(name, camera_index, num_images=5):
    """
    Capture images from the specified camera and save them in a folder.

    Parameters:
    - name (str): Name used to create a folder for saving images.
    - camera_index (int): Index of the camera to use.
    - num_images (int): Number of images to capture (default is 30).
    """
    # Open the camera
    capture = cv2.VideoCapture(camera_index)

    # Create a folder for saving images
    image_folder = f'images/{name}'
    create_folder_if_not_exists(image_folder)

    # Create a window to display the camera feed
    cv2.namedWindow("Face Capture", cv2.WINDOW_NORMAL)

    for i in range(num_images):
        # Capture a frame from the camera
        ret, frame = capture.read()

        # Display the camera feed
        cv2.imshow("Face Capture", frame)

        # Save the captured image
        image_path = os.path.join(image_folder, f'{name}_{i+1}.jpg')
        cv2.imwrite(image_path, frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # Release the camera and close the window
    capture.release()
    cv2.destroyAllWindows()

def main():
    # Prompt user for camera index and name
    camera_index = 0 # default camera index is 0
    name = input("Chkoun syedeeetk : ")
    # print("1. khadeem")
    # print("2. tahaan")
    # print("3. stagiaire")
    # role = input("Enter your role (1 or 2 or 3): ")
    # if role not in ['1', '2','3']:
    #     print("Invalid role. Exiting...")
    #     return

    # # Capture images using the specified camera and save them
    capture_images(name, camera_index)

if __name__ == "__main__":
    main()
# import cv2
# import os 


# def create_folder_if_not_exists(folder_path):
#     """
#     Create a folder if it does not exist.

#     Parameters:
#     - folder_path (str): Path to the folder.
#     """
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

# def capture_images(name, camera_index, num_images=5):
#     """
#     Capture images from the specified camera and save them in a folder.

#     Parameters:
#     - name (str): Name used to create a folder for saving images.
#     - camera_index (int): Index of the camera to use.
#     - num_images (int): Number of images to capture (default is 30).
#     """
#     # Open the camera
#     capture = cv2.VideoCapture(camera_index)

#     # Create a folder for saving images
#     image_folder = f'images/{name}'
#     create_folder_if_not_exists(image_folder)

#     # Create a window to display the camera feed
#     cv2.namedWindow("Face Capture", cv2.WINDOW_NORMAL)

#     for i in range(num_images):
#         # Capture a frame from the camera
#         ret, frame = capture.read()

#         # Display the camera feed
#         cv2.imshow("Face Capture", frame)

#         # Save the captured image
#         image_path = os.path.join(image_folder, f'{name}_{i+1}.jpg')
#         cv2.imwrite(image_path, frame)

#         print(f'Image {i+1} captured and saved.')

#         # Break the loop if 'q' key is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the camera and close the window
#     capture.release()
#     cv2.destroyAllWindows()

# def main():
#     # Prompt user for camera index and name
#     camera_index = 0 # default camera index is 0
#     name = input("Chkoun syedeeetk : ")

#     # Capture images using the specified camera and save them
#     capture_images(name, camera_index)

# if __name__ == "__main__":
#     main()
