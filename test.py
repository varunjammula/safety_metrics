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


def get_vehicle_ids_no_set(trajectory_data):
    vehicle_ids = trajectory_data.Vehicle_ID
    return vehicle_ids


def get_value(df):
    return df.values[0]


def get_values_list(df):
    return df.values


def get_frames_cars(trajectory_data, v_following_id, v_leading_id):
    vehicle_following = get_data_by_vehicle_ID(trajectory_data, id=v_following_id)
    # vehicle_leading = get_data_by_vehicle_ID(trajectory_data, id=v_leading_id)

    d1_frame = vehicle_following[
        (vehicle_following['Preceding'] == v_leading_id)]
    # d2_frame = vehicle_leading[
    #     (vehicle_leading['Following'] == v_following_id)]
    # print(get_values_list(d1_frame.Frame_ID))
    return get_values_list(d1_frame.Frame_ID)


def compute_metrics(trajectory_data, v_following_id, v_leading_id, frame_id, spacing=None):
    try:

        vehicle_following = get_data_by_vehicle_ID(trajectory_data, id=v_following_id)
        vehicle_leading = get_data_by_vehicle_ID(trajectory_data, id=v_leading_id)

        d1_frame = vehicle_following[
            (vehicle_following['Preceding'] == v_leading_id) & (vehicle_following['Frame_ID'] == frame_id)]
        d2_frame = vehicle_leading[
            (vehicle_leading['Following'] == v_following_id) & (vehicle_leading['Frame_ID'] == frame_id)]

        # print(d1_frame)
        # print(d2_frame)

        velocity_following = get_value(d1_frame.v_Vel)
        vehicle_length_following = get_value(d1_frame.v_Length)
        local_y_following = get_value(d1_frame.Local_Y)
        acc_following = get_value(d1_frame.v_Acc)
        acc_min_brake_fol = get_acc_range(trajectory_data, v_following_id)[0]

        velocity_leading = get_value(d2_frame.v_Vel)
        vehicle_length_leading = get_value(d2_frame.v_Length)
        local_y_leading = get_value(d2_frame.Local_Y)
        acc_leading = get_value(d2_frame.v_Acc)
        acc_max_brake_lead = get_acc_range(trajectory_data, v_leading_id)[1]
        spacing = get_value(d1_frame.Space_Headway)
        dlong = spacing - vehicle_length_leading

        # print(d1_frame)
        sev_long = sm.compute_SEV_longitudinal(velocity_following, velocity_leading, rho=2, acc_fol=acc_following,
                                               acc_max_brake_lead=acc_max_brake_lead,
                                               acc_min_brake_fol=acc_min_brake_fol)


        # sev_slide = sm.compute_SEV_longitudinal(velocity_following, velocity_leading, rho=2, acc_fol=9.13,
        #                                        acc_max_brake_lead=-10.11, acc_min_brake_fol=-5.23)
        # print('SEV_slide: {}'.format(sev_slide))

        # print(acc_following, acc_max_brake_lead, acc_min_brake_fol)
        # print(9.13, -10.11, -5.23)
        if sev_long > dlong:
            sev = 1
        else:
            sev = 0

        ttc = sm.compute_TTC(local_y_leading, local_y_following, vehicle_length_leading, velocity_following,
                             velocity_leading)
        mttc =0
        # mttc = sm.compute_MTTC(velocity_following, velocity_leading, acc_following, acc_leading, local_y_leading,
        #                        local_y_following, vehicle_length_leading)
        if ttc < 3:
            ttc_f = 1
        else:
            ttc_f = 0

        if mttc < 3:
            mttc_f = 1
        else:
            mttc_f = 0

        if not math.isnan(mttc):
            print(v_following_id, v_leading_id, frame_id)
            print('acc ', end='')
            print(acc_following, acc_leading, acc_min_brake_fol, acc_max_brake_lead)
            # print(local_y_leading - local_y_following - vehicle_length_following)
            print('vel ', end='')
            print(velocity_following, velocity_leading)
            # print(velocity_following, velocity_leading)
            # print(acc_following, acc_leading)

            print('RSS-SEV: {}, dlong:{}'.format(sev_long, dlong))
            print('SEV: {}'.format(sev))
            print('TTC: {}, ttc_f: {}'.format(ttc, ttc_f))
            print('MTTC: {}, mttc_f: {}'.format(mttc, mttc_f))

            print('-----')
            return (v_following_id, v_leading_id, frame_id, velocity_following, velocity_leading, acc_following, acc_leading, spacing, dlong, sev_long, sev, ttc, ttc_f, mttc, mttc_f)
    except Exception as e:
        print(e)


def get_acc_range(trajectory_data, vehicle_ID):
    vehicle_data = get_data_by_vehicle_ID(trajectory_data, id=vehicle_ID)
    acc_neg = []
    acc_pos = []
    all_data = []
    new_data = []
    for val in vehicle_data.v_Acc:
        all_data.append(val)
    # return np.min(vehicle_data.v_Acc), np.max(vehicle_data.v_Acc), np.max(temp)
    # print(all_data)
    # print(len(all_data))
    n1 = list(filter(lambda a: a != -11.2, all_data))
    n2 = list(filter(lambda a: a != 11.2, n1))
    # all_data.remove(11.2)
    # all_data.remove(-11.2)
    # print(len(n2))
    # print(n2)
    # print('----')

    for val in n2:
        # print(val)
        if val < 0:
            acc_neg.append(val)
    return np.mean(acc_neg), np.min(acc_neg)
    # return np.mean(acc_neg), np.mean(acc_pos), np.min(acc_neg), np.max(acc_neg)

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
        # print(id)
        data = get_data_by_vehicle_ID(trajectory_data, id)
        velocities = list(data.v_Vel)
        frames = list(data.Frame_ID)
        acc_data = list(data.v_Acc)
        acc_computed = []
        for i in range(1, len(velocities)):
            frame_diff = frames[i] - frames[i - 1]
            # if frame_diff > 1:
            #     print(frame_diff)
            #     sys.exit()
            a = (velocities[i] - velocities[i - 1]) / (sampling_time * frame_diff)
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

    df = pd.DataFrame({'vehicle_ID': v_id, 'a_comp_min': a_comp_min, 'a_comp_max': a_comp_max, 'a_comp_avg': a_comp_avg,
                       'a_comp_var': a_comp_var,
                       'a_data_min': a_data_min, 'a_data_max': a_data_max, 'a_data_avg': a_data_avg,
                       'a_data_var': a_data_var})

    df.to_csv('acc_analysis_filtered.csv', index=False)


def get_pairs(trajectory_data):
    # get cars where it has preceding and following
    pairs_data = trajectory_data[(trajectory_data['Following'] != 0) & (trajectory_data['Preceding'] != 0)]
    print(len(pairs_data))

    vehicle_ids = get_vehicle_ids_no_set(pairs_data)
    # print(len(vehicle_ids))
    # print(pairs_data)
    fol_vehicles = pairs_data.Following
    lead_vehicles = pairs_data.Preceding
    # print(len(fol_vehicles))
    # print(len(lead_vehicles))

    all_pairs = [(f_id, l_id) for (f_id, l_id) in zip(fol_vehicles, vehicle_ids)]
    other_pairs = [(f_id, l_id) for (f_id, l_id) in zip(vehicle_ids, lead_vehicles)]

    total_pairs = all_pairs + other_pairs

    pairs_set = set(total_pairs)
    print(len(pairs_set))
    f_ids = []
    l_ids = []
    frame_ids = []
    i = 0
    for (f_id, l_id) in pairs_set:
        i += 1
        if i %100 == 0:
            print(i)
        # print(f_id, l_id)
        f_data = get_data_by_vehicle_ID(trajectory_data, id=f_id)
        l_data = get_data_by_vehicle_ID(trajectory_data, id=l_id)
        d1_frame = f_data[(f_data['Preceding'] == l_id)]
        d2_frame = l_data[(l_data['Following'] == f_id)]
        # print(len(d1_frame))
        # print(len(d2_frame))
        #
        # print(get_values_list(d1_frame.Frame_ID))
        # print(get_values_list(d2_frame.Frame_ID))

        for frame in d1_frame.Frame_ID:
            f_temp = d1_frame[d1_frame['Frame_ID'] == frame]
            f_temp_prev = d1_frame[d1_frame['Frame_ID'] == frame-1]
            l_temp = d2_frame[d2_frame['Frame_ID'] == frame]
            try:
                v_f = get_value(f_temp.v_Vel)
                v_l = get_value(l_temp.v_Vel)
                a_f = get_value(f_temp.v_Acc)
                a_l = get_value(l_temp.v_Acc)
                a_f_prev = get_value(f_temp_prev.v_Acc)

                # case-1
                # if (v_f > v_l) and (a_f < a_l) and a_f < 0:
                #     f_ids.append(f_id)
                #     l_ids.append(l_id)
                #     frame_ids.append(frame)

                # # case-2
                # if (v_f > v_l) and (a_f > a_l) and a_f < 0:
                #     f_ids.append(f_id)
                #     l_ids.append(l_id)
                #     frame_ids.append(frame)

                # # case-3 - evasive action
                if (v_f > v_l) and a_f < 0:
                    f_ids.append(f_id)
                    l_ids.append(l_id)
                    frame_ids.append(frame)

            except IndexError:
                continue

    df = pd.DataFrame({'follower_ID': f_ids, 'lead_ID': l_ids, 'frame_id': frame_ids})
    df.to_csv('data/data_case3.csv', index=False)


if __name__ == '__main__':
    sm = SafetyMetrics()

    trajectory_data = pd.read_csv('data/i-80/trajectories-0400-0415.csv', low_memory=False)
    # # trajectory_data = pd.read_csv('data/lanker/trajectories.csv', low_memory=False)
    # print(len(trajectory_data))
    #
    # # acc_analysis(trajectory_data)
    # get_pairs(trajectory_data)
    #
    # # SEV_long, TTC, MTTC
    #
    frame_id = 3244
    # # vehicles - (1024, 1015); (1031, 1024); (1001, 994)
    #
    # frames = get_frames_cars(trajectory_data, 250, 243)
    # get_frames_cars(trajectory_data, 250, 243)
    #
    # compute_metrics(trajectory_data, 250, 243, frame_id=1301)
    compute_metrics(trajectory_data, 1024, 1015, frame_id=frame_id)
    compute_metrics(trajectory_data, 1023, 1013, frame_id=frame_id)
    compute_metrics(trajectory_data, 1020, 1016, frame_id=frame_id)

    compute_metrics(trajectory_data, 1026, 1014, frame_id=frame_id)
    compute_metrics(trajectory_data, 1025, 1004, frame_id=frame_id)
    compute_metrics(trajectory_data, 1024, 1015, frame_id=frame_id)

    #
    # # val = sm.compute_SEV_longitudinal(vr, vf=vf, rho=0.8, a_accel=8.42, a_max_brake=-4.31, a_min_brake=-11.1)
    # # val = sm.compute_SEV_longitudinal(vr, vf=vf, rho=0.8, a_accel=6.2, a_max_brake=-4.42, a_min_brake=-10.84)


    # pair_data = pd.read_csv('data/data_case3.csv', low_memory=False)
    # # print(pair_data.)
    # f_ids = list(pair_data.follower_ID)
    # l_ids = list(pair_data.lead_ID)
    # frame_ids = list(pair_data.frame_id)
    # data = []
    # i= 0
    # for (f_id, l_id, frame_id) in zip(f_ids, l_ids, frame_ids):
    #     i += 1
    #     f_data = get_data_by_vehicle_ID(trajectory_data, f_id)
    #     l_data = get_data_by_vehicle_ID(trajectory_data, l_id)
    #
    #     f_frame_data = f_data[(f_data['Preceding'] == l_id) & (f_data['Frame_ID'] == frame_id)]
    #     l_frame_data = l_data[(l_data['Following'] == f_id) & (l_data['Frame_ID'] == frame_id)]
    #     data.append(compute_metrics(trajectory_data, f_id, l_id, frame_id=frame_id))
    #
    # # print(data)
    # df = pd.DataFrame(data, columns=['f_id', 'l_id', 'frame_id', 'velocity_following', 'velocity_leading',
    #         'acc_following', 'acc_leading', 'spacing', 'dlong', 'sev_long', 'sev', 'ttc', 'ttc_f', 'mttc', 'mttc_f'])
    #
    # df.to_csv('data/metrics_case3.csv', index=False)


