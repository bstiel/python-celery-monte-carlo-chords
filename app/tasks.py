import scipy
import scipy.stats

from worker import app


def black_scholes_call(S, strike, T, rf, sigma):
    """
       Objective: Black-Schole-Merton option model
       Format   : bs_call(S,X,T,r,sigma)
               S: current stock price
               X: exercise price
               T: maturity date in years
              rf: risk-free rate (continusouly compounded)
           sigma: volatiity of underlying security 
       Example 1:  
         >>>bs_call(40,40,1,0.1,0.2)
         5.3078706338643578
    """    
    d1 = (scipy.log(S/strike) + (rf+sigma*sigma/2.)*T) / (sigma*scipy.sqrt(T))
    d2 = d1 - sigma * scipy.sqrt(T)
    return S*scipy.stats.norm.cdf(d1) - strike*scipy.exp(-rf*T) * scipy.stats.norm.cdf(d2)


@app.task(bind=True, name='up_and_out_call')
def up_and_out_call(self, s0, strike, T, r, sigma, barrier, n_simulation, n_steps = 100.):
    dt = T / n_steps
    total = 0
    for j in range(0, n_simulation):
        sT = s0
        out = False
        for i in range(0, int(n_steps)):
            e = scipy.random.normal()
            sT *= scipy.exp((r - 0.5 * sigma * sigma) * dt + sigma * e * scipy.sqrt(dt))
            if sT > barrier:
                out = True
                break
        if out == False:
            total += bs_call(s0, strike, T, r, sigma)
    return total / n_simulation


@app.task(bind=True, name='mean')
def mean(self, args):
    return sum(args) / len(args)
