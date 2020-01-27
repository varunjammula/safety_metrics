from SafetyMetrics import SafetyMetrics
import pandas as pd
from utils.video_frame_counter import get_video_with_frames

if __name__=='__main__':
    sm = SafetyMetrics()

    trajectory_data = pd.read_csv('data/trajectories-0400-0415.csv', low_memory=False)
    # print(trajectory_data[1])
    select_price = trajectory_data.loc[trajectory_data['Vehicle_ID'] == 1]
    print(select_price)

    get_video_with_frames('data/nb-camera5-0400pm-0415pm-processed.avi', 'data/output.avi')

