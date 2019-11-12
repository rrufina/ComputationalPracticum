"""
Differential Equations. Computational Practicum
Student: Rufina Sirgalina
"""
import matplotlib
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
from solution import *
matplotlib.use('TkAgg')

root = tk.Tk()
root.title("Differential Equations. Computational Practicum")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

x_0 = tk.DoubleVar()
y_0 = tk.DoubleVar()
x_f = tk.DoubleVar()
n = tk.IntVar()
n_0 = tk.IntVar()
n_f = tk.IntVar()

label = tk.Label(mainframe, text="Variant 20" \
                 "\n y' = (2-y^2)/(2yx^2) ")
label.grid(columnspan=2, pady=10)

x0_label = tk.Label(mainframe, text='x0')
x0_label.grid(row=2)
x0_entry = tk.Entry(mainframe, textvariable=x_0)
x0_entry.grid(row=2, column=1)

y0_label = tk.Label(mainframe, text='y0')
y0_label.grid(row=3)
y0_entry = tk.Entry(mainframe, textvariable=y_0)
y0_entry.grid(row=3, column=1)

xf_label = tk.Label(mainframe, text='X')
xf_label.grid(row=4)
xf_entry = tk.Entry(mainframe, textvariable=x_f)
xf_entry.grid(row=4, column=1)

n_label = tk.Label(mainframe, text='N')
n_label.grid(row=5)
n_entry = tk.Entry(mainframe, textvariable=n)
n_entry.grid(row=5, column=1)

n0_label = tk.Label(mainframe, text='N min')
n0_label.grid(row=6)
n0_entry = tk.Entry(mainframe, textvariable=n_0)
n0_entry.grid(row=6, column=1)

nf_label = tk.Label(mainframe, text='N max')
nf_label.grid(row=7)
nf_entry = tk.Entry(mainframe, textvariable=n_f)
nf_entry.grid(row=7, column=1)

def plotGraphs(x_0, y_0, x_f, n, n_0, n_f):

    ex = ExactSolution(x_0, y_0, x_f, n)
    em = EulerMethod(x_0, y_0, x_f, n)
    iem = ImprovedEulerMethod(x_0, y_0, x_f, n)
    rkm = RungeKuttaMethod(x_0, y_0, x_f, n)

    ex_x, ex_y = ex.solve()
    em_x, em_y = em.solve()
    iem_x, iem_y = iem.solve()
    rkm_x, rkm_y = rkm.solve()

    plt.figure()

    plt.subplot(1, 3, 1)
    plt.plot(ex_x, ex_y, label='Exact Solution')
    plt.plot(em_x, em_y, label='Euler Method')
    plt.plot(iem_x, iem_y, label='Improved Euler Method')
    plt.plot(rkm_x, rkm_y, label='Runge Kutta Method')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Solutions')
    plt.grid()
    plt.legend(loc='best')

    em_er_y = em.error(ex_y)
    iem_er_y = iem.error(ex_y)
    rkm_er_y = rkm.error(ex_y)

    plt.subplot(1, 3, 2)
    plt.plot(em_x, em_er_y, label='Euler Method')
    plt.plot(iem_x, iem_er_y, label='Improved Euler Method')
    plt.plot(rkm_x, rkm_er_y, label='Runge Kutta Method')
    plt.xlabel('x')
    plt.ylabel('Error')
    plt.title('Local Errors')
    plt.grid()
    plt.legend(loc='best')

    if n_0 and n_f:

        total_err = TotalError(n_0, n_f)
        te_x = total_err.X
        em_te_y, iem_te_y, rkm_te_y = total_err.calculate(x_0, y_0, x_f)

        plt.subplot(1, 3, 3)
        plt.plot(te_x, em_te_y, label='Euler Method')
        plt.plot(te_x, iem_te_y, label='Improved Euler Method')
        plt.plot(te_x, rkm_te_y, label='Runge Kutta Method')
        plt.xlabel('N')
        plt.ylabel('Error')
        plt.title('Total Errors')
        plt.grid()
        plt.legend(loc='best')

    plt.show()


ttk.Button(mainframe,
           text='Plot',
           command=lambda: plotGraphs(x_0.get(),
                                      y_0.get(),
                                      x_f.get(),
                                      n.get(),
                                      n_0.get(),
                                      n_f.get())).grid(columnspan=2, row=9, pady=10)

root.mainloop()
