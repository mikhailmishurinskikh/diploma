import pybamm

def paramsDFN():
    return pybamm.ParameterValues({
        # Geometry
        "L_sep": 12e-6,
        "L_anode": 85.2e-6,
        "L_cathode": 75.6e-6,

        # Butler-Folmer anode, negative (C)
        "Fk_anode": 6.48e-7,
        "C_max_anode": 33133,
        "U_anode": lambda x: (
            1.9793 * pybamm.exp(-39.3631 * x) + 0.2482
            - 0.0909 * pybamm.tanh(29.8538 * (x - 0.1234))
            - 0.04478 * pybamm.tanh(14.9159 * (x - 0.2769))
            - 0.0205 * pybamm.tanh(30.4444 * (x - 0.6103))
        ),

        # Butler-Folmer cathode, positive (NMC)
        "Fk_cathode": 3.42e-6,
        "C_max_cathode": 63104,
        "U_cathode": lambda x: (
            -0.8090 * x + 4.4875
            - 0.0428 * pybamm.tanh(18.5138 * (x - 0.5542))
            - 17.7326 * pybamm.tanh(15.7890 * (x - 0.3117))
            + 17.5842 * pybamm.tanh(15.9308 * (x - 0.3120))
        ),

        # Electrolyte
        "D_e": lambda c: 8.794e-11 * (c/1000) ** 2 - 3.972e-10 * (c/1000) + 4.862e-10,
        "kappa_e": lambda c: 0.1297 * (c/1000) ** 3 - 2.51 * (c/1000) ** 1.5 + 3.329 * (c/1000),
        "t_plus": 0.2594,
        "eps_sep": 0.47,
        "tau_sep": 0.47 / 0.47**1.5,
        "tau_anode": 0.25 / 0.25**1.5,
        "tau_cathode": 0.335 / 0.335**1.5,

        # Solid anode
        "eps_s_anode": 0.75,
        "kappa_s_anode": 215,
        "R_p_anode": 5.86e-6,
        "D_s_anode": 3.3e-14,

        # Solid cathode
        "eps_s_cathode": 0.665,
        "kappa_s_cathode": 0.18,
        "R_p_cathode": 5.22e-6,
        "D_s_cathode": 4e-15,

        # General
        "T": 298.15,

        # Initial
        "C_e_0": 1000,
        "C_s_0_anode": 0.9014 * 33133,
        "C_s_0_cathode": 0.27 * 63104,

        # Cutoff
        "u_min" : 2.5,
        "u_max" : 4.4,
    })

def paramsDC1():
    return pybamm.ParameterValues({
        # Geometry
        "L_sep": 12e-6,
        "L_anode": 85.2e-6,
        "L_cathode": 75.6e-6,

        # Butler-Folmer anode, negative (C)
        "Fk_anode": 6.48e-7,
        "C_max_anode": 33133,
        "U_anode": lambda x: (
            1.9793 * pybamm.exp(-39.3631 * x) + 0.2482
            - 0.0909 * pybamm.tanh(29.8538 * (x - 0.1234))
            - 0.04478 * pybamm.tanh(14.9159 * (x - 0.2769))
            - 0.0205 * pybamm.tanh(30.4444 * (x - 0.6103))
        ),

        # Butler-Folmer cathode, positive (NMC)
        "Fk_cathode": 3.42e-6,
        "C_max_cathode": 63104,
        "U_cathode": lambda x: (
            -0.8090 * x + 4.4875
            - 0.0428 * pybamm.tanh(18.5138 * (x - 0.5542))
            - 17.7326 * pybamm.tanh(15.7890 * (x - 0.3117))
            + 17.5842 * pybamm.tanh(15.9308 * (x - 0.3120))
        ),

        # Electrolyte
        "D_e": lambda c: 8.794e-11 * (c/1000) ** 2 - 3.972e-10 * (c/1000) + 4.862e-10,
        "kappa_e": lambda c: 0.1297 * (c/1000) ** 3 - 2.51 * (c/1000) ** 1.5 + 3.329 * (c/1000),
        "t_plus": 0.2594,
        "eps_sep": 0.47,
        "tau_sep": 0.47 / 0.47**1.5,
        "tau_anode": 0.25 / 0.25**1.5,
        "tau_cathode": 0.335 / 0.335**1.5,

        # Solid anode
        "eps_s_anode": 0.75,
        "kappa_s_anode": 215,
        "a_anode": 383959.0,
        "s_anode": -368.1,

        # Solid cathode
        "eps_s_cathode": 0.665,
        "kappa_s_cathode": 0.18,
        "a_cathode": 382183.9,
        "s_cathode": -2705.1,

        # General
        "T": 298.15,

        # Initial
        "C_e_0": 1000,
        "C_s_0_anode": 0.9014 * 33133,
        "C_s_0_cathode": 0.27 * 63104,

        # Cutoff
        "u_min" : 2.5,
        "u_max" : 4.4,
    })

def paramsDFN_template():
    return pybamm.ParameterValues({
        # Geometry
        "L_sep": "[input]",
        "L_anode": "[input]",
        "L_cathode": "[input]",

        # Butler-Folmer anode, negative (C)
        "Fk_anode": "[input]",
        "C_max_anode": "[input]",
        "U_anode": lambda x: (
            1.9793 * pybamm.exp(-39.3631 * x) + 0.2482
            - 0.0909 * pybamm.tanh(29.8538 * (x - 0.1234))
            - 0.04478 * pybamm.tanh(14.9159 * (x - 0.2769))
            - 0.0205 * pybamm.tanh(30.4444 * (x - 0.6103))
        ),

        # Butler-Folmer cathode, positive (NMC)
        "Fk_cathode": "[input]",
        "C_max_cathode": "[input]",
        "U_cathode": lambda x: (
            -0.8090 * x + 4.4875
            - 0.0428 * pybamm.tanh(18.5138 * (x - 0.5542))
            - 17.7326 * pybamm.tanh(15.7890 * (x - 0.3117))
            + 17.5842 * pybamm.tanh(15.9308 * (x - 0.3120))
        ),

        # Electrolyte
        "D_e": lambda c: 8.794e-11 * (c/1000) ** 2 - 3.972e-10 * (c/1000) + 4.862e-10,
        "kappa_e": lambda c: 0.1297 * (c/1000) ** 3 - 2.51 * (c/1000) ** 1.5 + 3.329 * (c/1000),
        "t_plus": "[input]",
        "eps_sep": "[input]",
        "tau_sep": "[input]",
        "tau_anode": "[input]",
        "tau_cathode": "[input]",

        # Solid anode
        "eps_s_anode": "[input]",
        "kappa_s_anode": "[input]",
        "R_p_anode": 5.86e-6,
        "D_s_anode": "[input]",

        # Solid cathode
        "eps_s_cathode": "[input]",
        "kappa_s_cathode": "[input]",
        "R_p_cathode": 5.22e-6,
        "D_s_cathode": "[input]",

        # General
        "T": 298.15,

        # Initial
        "C_e_0": "[input]",
        "C_s_0_anode": "[input]",
        "C_s_0_cathode": "[input]",

        # Cutoff
        "u_min" : 2.5,
        "u_max" : 4.4,
    })

def paramsDC1_template():
    return pybamm.ParameterValues({
        # Geometry
        "L_sep": "[input]",
        "L_anode": "[input]",
        "L_cathode": "[input]",

        # Butler-Folmer anode, negative (C)
        "Fk_anode": "[input]",
        "C_max_anode": "[input]",
        "U_anode": lambda x: (
            1.9793 * pybamm.exp(-39.3631 * x) + 0.2482
            - 0.0909 * pybamm.tanh(29.8538 * (x - 0.1234))
            - 0.04478 * pybamm.tanh(14.9159 * (x - 0.2769))
            - 0.0205 * pybamm.tanh(30.4444 * (x - 0.6103))
        ),

        # Butler-Folmer cathode, positive (NMC)
        "Fk_cathode": "[input]",
        "C_max_cathode": "[input]",
        "U_cathode": lambda x: (
            -0.8090 * x + 4.4875
            - 0.0428 * pybamm.tanh(18.5138 * (x - 0.5542))
            - 17.7326 * pybamm.tanh(15.7890 * (x - 0.3117))
            + 17.5842 * pybamm.tanh(15.9308 * (x - 0.3120))
        ),

        # Electrolyte
        "D_e": lambda c: 8.794e-11 * (c/1000) ** 2 - 3.972e-10 * (c/1000) + 4.862e-10,
        "kappa_e": lambda c: 0.1297 * (c/1000) ** 3 - 2.51 * (c/1000) ** 1.5 + 3.329 * (c/1000),
        "t_plus": "[input]",
        "eps_sep": "[input]",
        "tau_sep": "[input]",
        "tau_anode": "[input]",
        "tau_cathode": "[input]",

        # Solid anode
        "eps_s_anode": "[input]",
        "kappa_s_anode": "[input]",
        "a_anode": "[input]",
        "s_anode": "[input]",

        # Solid cathode
        "eps_s_cathode": "[input]",
        "kappa_s_cathode": "[input]",
        "a_cathode": "[input]",
        "s_cathode": "[input]",

        # General
        "T": 298.15,

        # Initial
        "C_e_0": "[input]",
        "C_s_0_anode": "[input]",
        "C_s_0_cathode": "[input]",

        # Cutoff
        "u_min" : 2.5,
        "u_max" : 4.4,
    })