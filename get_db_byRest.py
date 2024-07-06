# -*- coding: utf-8 -*-
"""
python get_db_byRest.py
"""

import numpy as np
import pandas as pd
import pandas.tseries.offsets as offsets
from mdaq import pymdaq_web

import matplotlib as mpl
import matplotlib.pyplot as plt

print(pd.__version__)
print(mpl.__version__)

class ShiftLog:

    def __init__(self):
        # REST-API
        rest_api_host = 'srweb-dmz-03'
        self.db = pymdaq_web.db(rest_api_host, port=8888, debug=0)
        
    def __del__(self):
        self.db.close()
        
    def get_data(self, signame, from_dt, to_dt):
        db = self.db
        
        res = db.get_data(signame,from_dt,to_dt)
        
        if db.status()!=pymdaq_web.DB_OK:
            print('Error: %d: %s' % (db.status(),db.err_msg()))
            raise SystemExit()
        data = res
        nd = db.conv_pointdata_to_ndarray(data, split=False, use_mdates=False)  #時系列ログデータから取得した点データをNumPyのndarrayに変換 http://srweb-dmz-03.spring8.or.jp:8888/static/docs/mdaq_web_api/mdaq.html
        df = pd.DataFrame(nd, columns=['date', 'value'])
        df.sort_values('date', inplace=True)
        
        
        
        return df

        # Get first value of next shift
        """
        c = pd.to_datetime(to_dt) + offsets.Minute()
        corr_to_dt = c.strftime('%Y/%m/%d %H:%M:%S')
        res = db.get_data(signame,to_dt,corr_to_dt)
        if db.status()!=pymdaq_web.DB_OK:
            print('Error: %d: %s' % (db.status(),db.err_msg()))
            raise SystemExit()
        data = res
        nd = db.conv_pointdata_to_ndarray(data, split=False, use_mdates=False)
        df2 = pd.DataFrame(nd, columns=['date', 'value'])
        df2.sort_values('date', inplace=True)
        print("C    DEBUG~~~~~~~~~~~~~~~~~~@get_data")
        return df._append(df2[:1], ignore_index=True)
        """
    
        
    def record(self, begin_dt, end_dt, siglist):        

        
        print(begin_dt)

        from_dt = begin_dt
        to_dt   = end_dt
        
        print("siglist[0]=",siglist[0])

        df = self.get_data(siglist[0], from_dt, to_dt)
        
        print(df)
        
        
        """
        # Find the time in the RUN state
        start = pd.Timestamp
        end = pd.Timestamp
        running = False
        prevRun = False
    
        print("FFFF    DEBUG~~~~~~~~~~~~~~~~~~")
        rec = pd.DataFrame()
        for i,item in df.iterrows():
            run = bool(int(item['value']) & 0x2) # isRunning
            if run == prevRun: continue
            prevRun = run;
            if run:
                print('started on', item['date'])
                start = item['date']
                running = True
            else:
                print('stopped on', item['date'])
                end = item['date']
                rec = rec.append({'begin': start, 'end': end}, ignore_index=True)
                running = False

        print("GGGF    DEBUG~~~~~~~~~~~~~~~~~~")
    
        if running:
            if start != df.iloc[-1]['date']:
                end = df.iloc[-1]['date']
                rec = rec.append({'begin': start, 'end': end}, ignore_index=True)

        print(rec)
        

        energy_list = []
        current_list = []
        charge_list = []
    
        for i,item in rec.iterrows():
            from_dt = item['begin'].strftime('%Y/%m/%d %X.%f')
            to_dt = item['end'].strftime('%Y/%m/%d %X.%f')

            energy = []
            for signame in energy_signame:
                df = self.get_data(signame, from_dt, to_dt)
                energy.append(df['value'].max())
#                print(signame, '=', '{:.4f}'.format(df['value'].max()), 'GeV')

            print('Max. of energy =', '{:.4f}'.format(max(energy)), 'GeV')
            energy_list.append(max(energy))
    
            df = self.get_data(current_signame, from_dt, to_dt)
            current = df['value'].max()
            print('Max. of current =', '{:.4f}'.format(current), 'nC/s')
            current_list.append(current)
    
            df = self.get_data(charge_signame, from_dt, to_dt)
            df['diff'] = df['value'].diff()
            charge = 0.
            for i,item in df.iterrows():
                if (np.isnan(item['diff']) or item['diff'] < 0): continue
                charge += item['diff']
            print('Charge =', '{:.1f}'.format(charge), 'nC')
            charge_list.append(charge)

        rec['energy'] = energy_list
        rec['current'] = current_list
        rec['charge'] = charge_list
        """
#        print(rec)
        return df
    

if __name__ == '__main__':
    
    begin_dt = '2021/06/18 01:00'
    end_dt = '2021/06/18 09:00'
    
    log = ShiftLog()
#    df = log.record(begin_dt, end_dt, 'xsbt')
#    df = log.record('2024/06/18 01:00', '2024/06/18 02:00', 'xsbt')

    l = []

    l.append('xfel_llrf_cb01_1_iq/amplitude')

    df = log.record('2024/06/18 01:00', '2024/06/18 01:01', l)



    print(df)
    print("print(df.dtypes) = ")
    print(df.dtypes)

    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(df['date'], df['value'])
    plt.show()

#    plt.figure()
#    df.plot()
#    plt.savefig('test.png')
#    plt.close('all')

#fig, (ax) = plt.subplots(nrows=len(df_sig), sharex="row", figsize=(float(x_size), float(y_size)))
#fig.patch.set_facecolor(str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0])
#fig.canvas.set_window_title(str(df_set.loc['title']).replace("1","").strip())
#ax[n].plot(keys, s.rave, linestyle="solid", marker=str(df_sig.loc[n]['marker']).replace("1","").strip().splitlines()[0], markersize=df_sig.loc[n]['linewidth'], color=df_sig.loc[n]['color'], label=df_sig.loc[n]['label'], clip_on=False)
    
    