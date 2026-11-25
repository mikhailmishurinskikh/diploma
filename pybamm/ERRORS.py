import numpy as np

def calc_errors(data_exp, data_sim, w_voltage=1, w_time=1, w_start=1):
    """
    data is np.column_stack([t, voltage])
    
    voltage error, time error, start error
    """
    
    t_exp = data_exp[:, 0][-1]
    t_sim = data_sim[:, 0][-1]
    time_error = (t_sim - t_exp) / t_exp
    
    t_rmse = np.arange(0, int(t_exp * 0.9) + 1)
    voltage_error = np.sqrt(np.sum((
        np.interp(t_rmse, data_exp[:,0], data_exp[:,1]) -
        np.interp(t_rmse, data_sim[:,0], data_sim[:,1])
    )**2) / t_rmse.shape[0]) / np.mean(data_exp[:, 1])
    
    start_error = (data_exp[:,1][0] - data_sim[:,1][0]) / data_exp[:,1][0]
    
    return np.array([voltage_error * w_voltage, time_error * w_time, start_error * w_start])


def penalty():
    return np.full(3, 1.0)