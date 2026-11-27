def Metropolis(names, step, chain_i):
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

    rng = np.random.default_rng(np.random.SeedSequence(12345 + chain_i))

    def evaluate(theta):
        run_inputs = dict(inputs, **{k: 10 ** t for k, t in zip(names, theta)})
        
        try:
            t_eval = np.linspace(0, data[:,0][-1] * 1.1, 1000)
            sol = model.run(inputs=run_inputs, t_eval=t_eval)
        
        except Exception as e:
            return ERRORS.penalty()
        
        return ERRORS.calc_errors(data, np.column_stack([sol.t, sol["voltage"].entries]))


    theta = np.log10([inputs[k] for k in names])
    state = evaluate(theta)
    
    theta0 = np.log10([inputs[k] for k in names])

    chain = [theta.copy()]
    history = [state]
    n_acc = 1

    lower = np.array([ERRORS.BOUNDS[k][0] for k in names])
    upper = np.array([ERRORS.BOUNDS[k][1] for k in names])

    for i in range(n_steps):
        while True:
            prop = theta + step * rng.standard_normal(len(names))
            if np.all((prop >= lower) & (prop <= upper)):
                break
        out = evaluate(prop)

        if out[3] < accept_th:
            theta, state = prop, out
            n_acc += 1

        chain.append(prop.copy())
        history.append(out)
        
        print(f"CHAIN: {chain_i} -- Step {i} of {n_steps}, accepted percentage: {n_acc / (i + 2) * 100:.2f}%")
        
    chain = np.array(chain)
    history = np.array(history)

    np.savetxt(f"data_metropolis/chain{chain_i}.data", np.column_stack((chain, history, history[:, 3] < accept_th)),
        header=f"log10 {names[0]}, log10 {names[1]}, log10 {names[2]}, log10 {names[3]}, voltage error, time error, start error,  full error, accepted\n"
        "model : DFN\n"
        f"accept_th = {accept_th}%\n"
        f"theta0 = {theta0}\n"
        f"accepted percentage = {n_acc / (n_steps+1) * 100:.2f}%\n"
        f"start time = {start_time}; end time = {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    )
    
    
if __name__ == "__main__":
    from multiprocessing import Pool
    import numpy as np
    import os
    
    os.makedirs("data_metropolis", exist_ok=True)

    args = [
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 1),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 2),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 3),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 4),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 5),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 6),
    ]
    
    n_proc = min(len(args), os.cpu_count())

    with Pool(processes=n_proc) as pool:
        pool.starmap(Metropolis, args)
