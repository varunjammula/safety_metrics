import cv2


def get_video_with_frames(input_file, output_file):
    cap = cv2.VideoCapture(input_file)
    counter = 0
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            counter += 1
            cv2.putText(frame, 'Frame: ' + str(int(counter)), (270, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            # cv2.imshow('result', frame)
            video.write(frame)

            # cv2.imwrite('./output_image.png', combo_image)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:
            break

    cap.release()
    video.release()
    cv2.destroyAllWindows()
