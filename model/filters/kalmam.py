from pykalman import KalmanFilter

def kalman(_list):
    kf = KalmanFilter(initial_state_mean=_list[0])

    res, _ = kf.em(_list, n_iter=2).smooth(_list)

    return res[-1][0]