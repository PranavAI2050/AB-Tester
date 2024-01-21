##ABtester numeric
import scipy.stats as stats
from dataclasses import dataclass
import math
import numpy as np
@dataclass
class estimation_metrics_cont:
    n:int
    xbar:float
    s:float
    def __repr__(self):
        return f"sample_params(n={self.n}, xbar={self.xbar:.3f}, s={self.s:.3f})"
     
def c_v_data(data, groups_col , control_group, test_group, activity):
    control_data =  data[data[groups_col] == control_group][activity]
    variation_data =  data[data[groups_col] == test_group][activity]
    return control_data, variation_data

def compute_continuous_metrics(data):

    metrics = estimation_metrics_cont( 
        n=len(data),
        xbar=np.mean(data),
        s=np.std(data, ddof=1)
    ) 
    
    return metrics

def degrees_of_freedom(control_metrics, variation_metrics):
     
    n1, s1 = control_metrics.n, control_metrics.s
    n2, s2 = variation_metrics.n, variation_metrics.s
    
    
    dof = np.square(s1**2/n1 + s2**2/n2) / ((s1**2/n1)**2/(n1 - 1) + (s2**2/n2)**2/(n2 - 1))
    return dof
def t_statistic_diff_means(control_metrics, variation_metrics):
    
    
    n1, xbar1, s1 = control_metrics.n, control_metrics.xbar, control_metrics.s
    n2, xbar2, s2 = variation_metrics.n, variation_metrics.xbar, variation_metrics.s
    
    t = (xbar1 - xbar2) / np.sqrt(s1**2/n1 + s2**2/n2)
    
    return t

def reject_nh_t_statistic(data, groups_col , control_group, test_group, activity,alpha=0.05):
    contol_data, var_data = c_v_data(data, groups_col , control_group, test_group, activity)
    
    control_metrics = compute_continuous_metrics(contol_data)
    variation_metrics = compute_continuous_metrics(var_data)
    
    dof = degrees_of_freedom(control_metrics,variation_metrics )
    t_statistic = t_statistic_diff_means(control_metrics,variation_metrics)
    
    reject = False
    p_value = 2*(1 - stats.t.cdf(abs(t_statistic), df=dof))
    
    if p_value < alpha:
        reject = True     
    return reject
 