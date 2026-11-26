def Metropolis(names, step):
    from imports import PARAMS, ERRORS, DC1, DFN, pd, np, pybamm
    from datetime import datetime
    
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = np.loadtxt("data1C.data")
    
    params = PARAMS.paramsDFN()
    params["I"] = lambda t: np.mean(data[:,2]) / 0.1027
    params["Fk_anode"] = "[input]"
    params["Fk_cathode"] = "[input]"
    params["D_s_anode"] = "[input]"
    params["D_s_cathode"] = "[input]"
    
    inputs = {
        "Fk_anode": 6.48e-7,
        "Fk_cathode": 3.42e-6,
        "D_s_anode": 3.3e-14,
        "D_s_cathode": 4e-15,
    }

    model = DFN()
    model.init(params, 30, 30)

    # Parameters
    n_steps = 1000
    accept_th = 1.5

    rng = np.random.default_rng(0)
    
    def evaluate(theta):
        run_inputs = dict(inputs, **{k: 10 ** t for k, t in zip(names, theta)})
        
        try:
            t_eval = np.linspace(0, data[:,0][-1] * 1.1, 1000)
            sol = model.run(inputs=run_inputs, t_eval=t_eval)
        
        except Exception as e:
            return np.sqrt(np.mean(ERRORS.penalty()**2)) * 100
        
        return np.sqrt(np.mean(ERRORS.calc_errors(data, np.column_stack([sol.t, sol["voltage"].entries]))**2)) * 100


    theta = np.log10([inputs[k] for k in names])
    state = evaluate(theta)
    
    theta0 = np.log10([inputs[k] for k in names])

    chain = [theta.copy()]
    history = [state]
    n_acc = 1

    for i in range(n_steps):
        prop = theta + step * rng.standard_normal(len(names))
        out = evaluate(prop)

        if out < accept_th:
            theta, state = prop, out
            n_acc += 1

        chain.append(prop.copy())
        history.append(out)
        
        print(f"{names[0]}-{names[1]} Step {i} of {n_steps}, accepted percentage: {n_acc / (i + 2) * 100:.2f}%")
        
    chain = np.array(chain)
    history = np.array(history)

    np.savetxt(f"data_metropolis/{names[0]}-{names[1]}.data", np.column_stack((chain, history, history < accept_th)),
        header=f"log10 {names[0]}, log10 {names[1]}, mean error, accepted\n"
        "model : DFN\n"
        f"accept_th = {accept_th}%\n"
        f"theta0 = {theta0}\n"
        f"accepted percentage = {n_acc / (n_steps + 1) * 100:.2f}%\n"
        f"start time = {start_time}; end time = {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    )
    
    
if __name__ == "__main__":
    from multiprocessing import Pool
    import numpy as np
    import os
            
    os.makedirs("data_metropolis", exist_ok=True)

    args = [
    #    (("Fk_cathode", "D_s_cathode"), np.array([1, 1])),
   #     (("Fk_anode", "D_s_anode"), np.array([0.5, 0.5])),
  #      (("Fk_cathode", "Fk_anode"), np.array([1, 1])),
 #       (("D_s_cathode", "D_s_anode"), np.array([0.5, 0.5])),
#        (("Fk_cathode", "D_s_anode"), np.array([1, 0.5])),
        (("Fk_anode", "D_s_cathode"), np.array([0.5, 1])),
    ]
    
    n_proc = min(len(args), os.cpu_count())

    with Pool(processes=n_proc) as pool:
        pool.starmap(Metropolis, args)
