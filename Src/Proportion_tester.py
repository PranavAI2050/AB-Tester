
##AB testing proportions

import scipy.stats as stats
from dataclasses import dataclass
import math
import numpy as np

@dataclass
class estimation_metrics_prop:
    n:int
    x:float
    p:float
    def __repr__(self):
        return f"sample_params(n={self.n}, x={self.x}, p={self.p:.3f})"
     
def c_v_data(data, groups_col , control_group, test_group, conversion):
    control_data =  data[data[groups_col] == control_group][conversion]
    variation_data =  data[data[groups_col] == test_group][conversion]
    return control_data, variation_data

def compute_proportion_metrics(data):
    metrics = estimation_metrics_prop( 
        n=len(data),
        x=data.sum(),
        p=data.mean()
    )
    
    return metrics

def pooled_proportion(control_metrics, variation_metrics):
    
    x1, n1 = control_metrics.x, control_metrics.n
    x2, n2 = variation_metrics.x, variation_metrics.n
    
    pp = (x1 + x2)/(n1 + n2)
    return pp
def z_statistic_diff_proportions(control_metrics, variation_metrics):
    
    pp = pooled_proportion(control_metrics, variation_metrics)
    
    n1, p1 = control_metrics.n, control_metrics.p
    n2, p2 = variation_metrics.n, variation_metrics.p
    
    z = (p1 - p2)/np.sqrt(pp*(1 - pp)*(1/n1 + 1/n2))
    
    return z

def reject_nh_z_statistic(data, groups_col , control_group, test_group, conversion,alpha=0.05):
    control_data ,var_data= c_v_data(data, groups_col , control_group, test_group, conversion)

    control_metrics = compute_proportion_metrics(control_data)
    variation_metrics = compute_proportion_metrics(var_data)
    
    z_statistic = z_statistic_diff_proportions(control_metrics, variation_metrics)
     
    reject = False
    p_value = 2*(1 - stats.norm.cdf(np.abs(z_statistic)))
    
    if p_value < alpha:
        reject = True
    return reject