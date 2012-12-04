import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab
import simulation_parameters
import sys
from scipy.optimize import leastsq
import os

# load simulation parameters
network_params = simulation_parameters.parameter_storage()  # network_params class containing the simulation parameters
params = network_params.load_params()                       # params stores cell numbers, etc as a dictionary

if (len(sys.argv) < 2):
    sim_cnt = 0
    fn = params['conn_list_ee_fn_base'] + '%d.dat' % sim_cnt
    output_fn = params['weight_and_delay_fig']
    if not os.path.exists(fn):
        tmp_fn = 'delme_tmp_%d' % (np.random.randint(0, 1e7))
        cat = 'cat %s* > %s' % (params['conn_list_ee_fn_base'], tmp_fn)
        sort = 'sort -gk 2 -gk 1 %s > %s' % (tmp_fn, fn)
        del_tmp_fn = 'rm %s' % (tmp_fn)
        print cat
        os.system(cat)
        print sort
        os.system(sort)
        print del_tmp_fn
        os.system(del_tmp_fn)

else:
    fn = sys.argv[1]
    output_fn = fn.rsplit('.dat')[0] + '.png'

d = np.loadtxt(fn)

weights = d[:, 2]
delays = d[:, 3]
w_mean, w_std = weights.mean(), weights.std()
d_mean, d_std = delays.mean(), delays.std()
n_weights = weights.size
n_possible = params['n_exc']**2

n_bins = 30
n_w, bins_w = np.histogram(weights, bins=n_bins, normed=True)
#n_w = n_w / float(n_w.sum())

print "bins_w", bins_w, '\nn_w', n_w
n_d, bins_d = np.histogram(delays, bins=n_bins, normed=True)
#n_d = n_d / float(n_d.sum())
print "bins_d", bins_d, '\nn_d', n_d

def residuals_exp_dist(p, y, x):
    return y - eval_exp_dist(x, p)

def eval_exp_dist(x, p):
    return p[0] * np.exp(- x * p[0])
#    return p[0] * np.exp(- x / p[1])

def residuals_delay_dist(p, y, x):
    return y - eval_delay_dist(x, p)

def eval_delay_dist(x, p):
    return x * p[1] * np.exp(- x / p[0])


print "Fitting function to weight distribution"
guess_params = (5e-2) # (w[0], w_tau)
#guess_params = (0.5, 5e-4) # (w[0], w_tau)
opt_params = leastsq(residuals_exp_dist, guess_params, args=(n_w, bins_w[:-1]), maxfev=1000)
#opt_w0 = opt_params[0][0]
#print "Optimal parameters: w_0 %.2e w_tau %.2e" % (opt_w0, opt_wtau)
opt_wtau= opt_params[0]#[0]

p_ee = float(n_weights) / n_possible
print 'P_ee: %.3e' % p_ee
print 'w_min: %.2e w_max %.2e w_mean: %.2e  w_std: %.2e' % (weights.min(), weights.max(), weights.mean(), weights.std())
print 'd_min: %.2e d_max %.2e d_mean: %.2e  d_std: %.2e' % (delays.min(), delays.max(), delays.mean(), delays.std())
print "Optimal parameters: w_lambda %.5e" % (opt_wtau)

print "Fitting function to delay distribution"
guess_params = (5., 10.)
opt_params_delay = leastsq(residuals_delay_dist, guess_params, args=(n_d, bins_d[:-1]), maxfev=1000)
print 'Opt delay params:', opt_params_delay
opt_d0 = opt_params_delay[0][0]
opt_d1 = opt_params_delay[0][1]

print "Plotting ..."
fig = pylab.figure()
ax1 = fig.add_subplot(211)
bin_width = bins_w[1] - bins_w[0]
ax1.bar(bins_w[:-1]-.5*bin_width, n_w, width=bin_width, label='$w_{mean} = %.2e \pm %.2e$' % (w_mean, w_std))
ax1.plot(bins_w[:-1], eval_exp_dist(bins_w[:-1], opt_params), 'r--', label='Fit: $(%.2e) * exp(-(%.2e) \cdot w)$' % (opt_wtau, opt_wtau))
#ax1.plot(bins_w[:-1], eval_exp_dist(bins_w[:-1], opt_params[0]), 'r--', label='Fit: $(%.1e) * exp(-w / (%.1e))$' % (opt_w0, opt_wtau))
ax1.set_xlabel('Weights')
ax1.set_ylabel('Count')
title = 'Weight profile $\sigma_{X(V)} = %.1f (%.1f)$' % (params['w_sigma_x'], params['w_sigma_v'])
ax1.set_title(fn)
ax1.legend()

ax2 = fig.add_subplot(212)
bin_width = bins_d[1] - bins_d[0]
ax2.bar(bins_d[:-1]-.5*bin_width, n_d, width=bin_width, label='$\delta_{mean} = %.1e \pm %.1e$' % (d_mean, d_std))
ax2.plot(bins_d[:-1], eval_delay_dist(bins_d[:-1], (opt_d0, opt_d1)), 'r--', label='Fit: $\delta \cdot exp(-\delta / (%.1e))$' % (opt_d0))
ax2.set_xlabel('Delays')
ax2.set_ylabel('Count')
ax2.legend()

print "Saving to:", output_fn
pylab.savefig(output_fn)
#pylab.show()

