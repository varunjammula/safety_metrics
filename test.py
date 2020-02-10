import math
import sys

from SafetyMetrics import SafetyMetrics
import pandas as pd
from utils.video_frame_counter import get_video_with_frames
import numpy as np


def get_data_by_vehicle_ID(trajectory_data, id):
    data = trajectory_data.loc[trajectory_data['Vehicle_ID'] == id]
    return data


def get_vehicle_ids(trajectory_data):
    vehicle_ids = set(trajectory_data.Vehicle_ID)
    return vehicle_ids

def get_value(df):
    return df.values[0]

def compute_metrics(trajectory_data, v_following_id, v_leading_id, frame_id, spacing=None):
    try:
        vehicle_following = get_data_by_vehicle_ID(trajectory_data, id=v_following_id)
        vehicle_leading = get_data_by_vehicle_ID(trajectory_data, id=v_leading_id)

        d1_frame = vehicle_following[(vehicle_following['Preceding'] == v_leading_id) & (vehicle_following['Frame_ID'] == frame_id)]
        d2_frame = vehicle_leading[(vehicle_leading['Following'] == v_following_id) & (vehicle_leading['Frame_ID'] == frame_id)]

        # print(d1_frame)
        # print(d2_frame)

        velocity_following = get_value(d1_frame.v_Vel)
        vehicle_length_following = get_value(d1_frame.v_Length)
        local_y_following = get_value(d1_frame.Local_Y)
        acc_following = get_value(d1_frame.v_Acc)

        velocity_leading = get_value(d2_frame.v_Vel)
        vehicle_length_leading = get_value(d2_frame.v_Length)
        local_y_leading = get_value(d2_frame.Local_Y)
        acc_leading = get_value(d2_frame.v_Acc)
        print('acc ', end='')
        print(acc_following, acc_leading)
        #print(local_y_leading - local_y_following - vehicle_length_following)
        print('vel ', end='')
        print(velocity_following, velocity_leading)
        # print(d1_frame)
        sev_long = sm.compute_SEV_longitudinal(velocity_following, vf=velocity_leading, rho=2, a_accel=9.13, a_max_brake=-10.11, a_min_brake=-5.23)
        print('SEV: {}'.format(sev_long))

        ttc = sm.compute_TTC(local_y_leading, local_y_following, vehicle_length_following, velocity_following, velocity_leading)
        print('TTC: {}'.format(ttc))
        print('-----')
    except Exception as e:
        print(e)


def clean_data(trajectory_data):
    bad_data1 = trajectory_data[trajectory_data['v_Acc'] == 11.2].index
    # print(bad_data.index)
    print(len(bad_data1))

    bad_data2 = trajectory_data[trajectory_data['v_Acc'] == -11.2].index
    # print(bad_data.index)
    print(len(bad_data2))

    good_count = (len(trajectory_data) - len(bad_data1) - len(bad_data2))

    print('good_count: {}'.format(good_count))
    print('% good: {}'.format(good_count / len(trajectory_data)))

    trajectory_data.drop(bad_data1, inplace=True)
    print(len(trajectory_data))

    trajectory_data.drop(bad_data2, inplace=True)
    print(len(trajectory_data))

    trajectory_data.to_csv('data/trajectories-0400-0415_filtered.csv', index=False)


def acc_analysis(trajectory_data):
    ids = list(get_vehicle_ids(trajectory_data))
    print(len(ids))
    sampling_time = 0.1
    a_comp_min, a_comp_max, a_data_min, a_data_max, a_comp_avg, a_data_avg, a_comp_var, a_data_var = [], [], [], [], [], [], [], []
    v_id = []
    # ids = [213]
    for id in ids:
        print(id)
        data = get_data_by_vehicle_ID(trajectory_data, id)
        velocities = list(data.v_Vel)
        acc_data = list(data.v_Acc)
        acc_computed = []
        for i in range(1, len(velocities)):
            a = (velocities[i] - velocities[i - 1]) / sampling_time
            acc_computed.append(a)

            # print('vel_b: {}, vel_a:{}, computed: {}, data: {}, a_before:{}'.format(velocities[i - 1], velocities[i],
            #                                                                             a, acc_data[i], acc_data[i - 1]))
        a_comp_min.append(np.nanmin(acc_computed))
        a_comp_max.append(np.nanmax(acc_computed))
        a_comp_avg.append(np.nanmean(acc_computed))
        a_comp_var.append(np.nanvar(acc_computed))

        a_data_min.append(np.nanmin(acc_data[1:]))
        a_data_max.append(np.nanmax(acc_data[1:]))
        a_data_avg.append(np.nanmean(acc_data[1:]))
        a_data_var.append(np.nanvar(acc_data[1:]))
        v_id.append(id)

    df= pd.DataFrame({'vehicle_ID' : v_id, 'a_comp_min': a_comp_min, 'a_comp_max': a_comp_max, 'a_comp_avg': a_comp_avg, 'a_comp_var': a_comp_var,
         'a_data_min': a_data_min, 'a_data_max': a_data_max, 'a_data_avg': a_data_avg, 'a_data_var': a_data_var})

    df.to_csv('acc_analysis.csv', index=False)



if __name__ == '__main__':
    sm = SafetyMetrics()

    trajectory_data = pd.read_csv('data/trajectories-0400-0415.csv', low_memory=False)
    print(len(trajectory_data))

    compute_metrics(trajectory_data, 250, 243, frame_id=1301)
    compute_metrics(trajectory_data, 242, 231, frame_id=1301)
    compute_metrics(trajectory_data, 213, 210, frame_id=1301)

    # val = sm.compute_SEV_longitudinal(vr, vf=vf, rho=0.8, a_accel=8.42, a_max_brake=-4.31, a_min_brake=-11.1)
    # val = sm.compute_SEV_longitudinal(vr, vf=vf, rho=0.8, a_accel=6.2, a_max_brake=-4.42, a_min_brake=-10.84)



