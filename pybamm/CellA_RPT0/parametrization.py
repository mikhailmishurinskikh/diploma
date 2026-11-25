from imports import *
from scipy.optimize import least_squares

def theta_optimize(d, params):
    data = np.loadtxt(d)
    dfn = DFN()
    
    theta0 = (
        params["C_s_0_anode"] / params["C_max_anode"],
        params["C_s_0_cathode"] / params["C_max_cathode"]            
    )
    
    params["I"] = lambda t: np.mean(data[:,2]) / 0.1027
    params["C_s_0_anode"] = "[input]"
    params["C_s_0_cathode"] = "[input]"
    
    t_eval = np.linspace(0, data[:,0][-1] * 1.1, 1000)
    
    dfn.init(params, 30, 30)
    
    def optimize(theta):
        try:
            sol = dfn.run({
                "C_s_0_anode" : theta[0] * params["C_max_anode"],
                "C_s_0_cathode" : theta[1] * params["C_max_cathode"]
            }, t_eval=t_eval)
        
        except Exception as e:
            print("penalty")
            return ERRORS.penalty()
        
        errors = ERRORS.calc_errors(data, np.column_stack([sol.t, sol["voltage"].entries]))
        
        print(f"voltage error = {errors[0]}; time error = {errors[1]}; start error = {errors[2]}")
        return errors
    
    fit = least_squares(
        optimize,
        theta0,
        diff_step=1e-2
    )
    
    dfn = DFN()    
    theta = fit.x
    params["C_s_0_anode"] = theta[0] * params["C_max_anode"]
    params["C_s_0_cathode"] = theta[1] * params["C_max_cathode"]
    
    dfn.init(params, 30, 30)
    sol = dfn.run({}, t_eval)
    
    plt.figure()
    plt.plot(sol.t, sol["voltage"].entries, label="model")
    plt.plot(data[:,0], data[:,1], label="experiment")
    plt.legend()
    plt.show()
    
    return params


def Ds_optimize(d, params):
    data = np.loadtxt(d)
    dfn = DFN()
    
    log_Ds0 = (
        np.log10(params["D_s_anode"]),
        np.log10(params["D_s_cathode"])
    )
    
    params["I"] = lambda t: np.mean(data[:,2]) / 0.1027
    params["D_s_anode"] = "[input]"
    params["D_s_cathode"] = "[input]"
    
    t_eval = np.linspace(0, data[:,0][-1] * 1.1, 1000)
    
    dfn.init(params, 30, 30)
    
    def optimize(log_Ds):
        try:
            sol = dfn.run({
                "D_s_anode" : 10 ** log_Ds[0],
                "D_s_cathode" : 10 ** log_Ds[1]
            }, t_eval=t_eval)
        
        except Exception as e:
            print("penalty")
            return ERRORS.penalty()
        
        errors = ERRORS.calc_errors(data, np.column_stack([sol.t, sol["voltage"].entries]))
        
        print(f"voltage error = {errors[0]}; time error = {errors[1]}; start error = {errors[2]}")
        return errors
    
    fit = least_squares(
        optimize,
        log_Ds0,
        diff_step=1e-2
    )
    
    dfn = DFN()    
    log_Ds = fit.x
    params["D_s_anode"] = 10 ** log_Ds[0]
    params["D_s_cathode"] = 10 ** log_Ds[1]
    
    dfn.init(params, 30, 30)
    sol = dfn.run({}, t_eval)
    
    plt.figure()
    plt.plot(sol.t, sol["voltage"].entries, label="model")
    plt.plot(data[:,0], data[:,1], label="experiment")
    plt.legend()
    plt.show()
    
    return params


if __name__ == "__main__":
    params = theta_optimize("01C.data", PARAMS.paramsDFN())
    params = Ds_optimize("05C.data", params)