def Metropolis(names, step, chain_i):
    from imports import PARAMS, DC1, DFN, pd, np, pybamm
    
    data = np.loadtxt("data1C.data")
    
    params = PARAMS.paramsDFN
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
    a1 = 1 / 20
    a2 = 1 / 0.02
    t_rmse = 3000.0
    accept_th = 2.5


    rng = np.random.default_rng(np.random.SeedSequence(12345 + chain_i))
    t_end_exp = data[:,0][-1]
    t_run = np.linspace(0, 1.3 * t_end_exp, 1000)
    mask_rmse = data[:,0] <= t_rmse


    def evaluate(theta):
        run_inputs = dict(inputs, **{k: 10 ** t for k, t in zip(names, theta)})
        try:
            sol = model.run(inputs=run_inputs, t_eval=t_run, sens=False)
        except Exception as e:
            return None
        t_end = sol.t[-1]
        time_error = abs(t_end - t_end_exp)
        if t_end < t_rmse:
            return None
        v = np.interp(data[:,0][mask_rmse], sol.t, sol["voltage"].entries)
        rmse = np.sqrt(np.mean((v - data[:,1][mask_rmse]) ** 2))
        return a1 * time_error + a2 * rmse


    theta = np.log10([inputs[k] for k in names])
    state = evaluate(theta)
    
    theta0 = np.log10([inputs[k] for k in names])

    chain = [theta.copy()]
    history = [state]
    n_acc = 1

    for i in range(n_steps):
        prop = theta + step * rng.standard_normal(len(names))
        out = evaluate(prop)

        if out is not None and out < accept_th:
            theta, state = prop, out
            n_acc += 1

        chain.append(prop.copy())
        history.append(out)
        
        print(f"CHAIN: {chain_i} -- Step {i} of {n_steps}, accepted percentage: {n_acc / (i + 2) * 100:.2f}%")
        
    chain = np.array(chain)
    history = np.array(history)
    history[history == None] = np.nan

    np.savetxt(f"data_metropolis/chain{chain_i}.data", np.column_stack((chain, history, history < accept_th)), fmt="%.5e",
        header=f"log10 {names[0]}, log10 {names[1]}, log10 {names[2]}, log10 {names[3]}, a1 * RMSE + a2 * time error, accepted\n"
        "model : DFN, Chen2020\n"
        f"a1 = {a1}, a2 = {a2}, accept_th = {accept_th}\n"
        f"theta0 = {theta0}\n"
        f"accepted percentage = {n_acc / n_steps * 100:.2f}%"
    )
    
    
if __name__ == "__main__":
    from multiprocessing import Pool
    import numpy as np

    args = [
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 1),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 2),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 3),
        (("Fk_cathode", "D_s_cathode", "Fk_anode", "D_s_anode"), np.array([0.1, 0.1, 0.1, 0.1]), 4),
    ]

    with Pool(processes=4) as pool:
        pool.starmap(Metropolis, args)