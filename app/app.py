import os
import logging
from flask import Flask, Response, request, jsonify
from tasks import up_and_out_call, mean
from celery import chord


app = Flask(__name__)
app.config['DEBUG'] = True
logger = logging.getLogger(__name__)


@app.route('/', methods=['POST'])
def index():
    simulations = 100000
    per_worker = 1000
    n = int(simulations / per_worker)

    # s0, x, T, r, sigma, barrier, n_simulation
    s0 = 100
    strike = 120
    T = 0.5
    r = 0.01
    sigma = 0.1
    barrier = 150

    #  s0, strike, T, r, sigma, barrier, n_simulation

    logger.info(f'Create chord, n={n}')

    task = chord([up_and_out_call.s(
        s0=s0,
        strike=strike,
        T=T,
        r=r,
        sigma=sigma,
        barrier=barrier,
        n_simulation=per_worker) for i in range(0, n)], mean.s())()
    return jsonify({'id': str(task.id), 'status': task.status}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)