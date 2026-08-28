from flask import Flask, render_template, request, jsonify
from math import floor
app=Flask(__name__)
state={'low':90000.0,'high':110000.0,'grids':10,'capital':10000000.0,'fee':0.0025,'running':False,'paper':True,'price':100000.0,'cash':10000000.0,'usdt':0.0,'trades':[]}

def levels():
    n=max(2,int(state['grids'])); lo=state['low']; hi=state['high']; step=(hi-lo)/(n-1)
    return [round(lo+i*step,2) for i in range(n)]
@app.route('/')
def index(): return render_template('index.html', s=state, levels=levels())
@app.post('/api/config')
def config():
    d=request.json
    for k in ('low','high','grids','capital','fee'):
        if k in d: state[k]=float(d[k]) if k!='grids' else int(d[k])
    state['cash']=state['capital']; state['usdt']=0; state['trades']=[]
    return jsonify(ok=True,levels=levels())
@app.post('/api/toggle')
def toggle(): state['running']=not state['running']; return jsonify(running=state['running'])
@app.post('/api/price')
def price():
    state['price']=float(request.json['price']); return jsonify(ok=True,price=state['price'])
@app.post('/api/simulate')
def simulate():
    p=float(request.json['price']); old=state['price']; state['price']=p
    lv=levels(); action=None
    # Simple grid crossing simulator: one trade per request, alternating based on cash/USDT
    if state['running']:
        if p<=max([x for x in lv if x<=p], default=lv[0]) and state['cash']>0:
            amount=min(state['capital']/state['grids'],state['cash']); qty=(amount*(1-state['fee']))/p
            state['cash']-=amount; state['usdt']+=qty; action='BUY'
            state['trades'].append({'side':'BUY','price':p,'amount':amount,'qty':qty})
        elif p>=min([x for x in lv if x>=p], default=lv[-1]) and state['usdt']>0:
            qty=state['usdt']/max(1,1); proceeds=qty*p*(1-state['fee']); state['usdt']=0; state['cash']+=proceeds; action='SELL'
            state['trades'].append({'side':'SELL','price':p,'amount':proceeds,'qty':qty})
    equity=state['cash']+state['usdt']*p
    return jsonify(price=p,action=action,cash=state['cash'],usdt=state['usdt'],equity=equity,trades=state['trades'][-20:])
@app.get('/api/state')
def api_state(): return jsonify(state=state,levels=levels(),equity=state['cash']+state['usdt']*state['price'])
if __name__=='__main__': app.run(host='0.0.0.0',port=8000)
