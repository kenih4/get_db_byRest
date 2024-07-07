# -*- coding: utf-8 -*-
"""
python get_db_byRest.py config_setting_LLRF.xlsx config_sig_LLRF_Pickup_INJECTOR.xlsx
python get_db_byRest.py config_setting_LLRF.xlsx config_sig_LLRF_Pickup_MAINLINAC.xlsx
python get_db_byRest.py config_setting_LLRF_SCSS.xlsx config_sig_LLRF_Pickup_SCSS.xlsx

デバッグ用
python get_db_byRest.py config_setting_LLRF.xlsx config_sig_TEST.xlsx

"""

import time
import sys
import math

import numpy as np
import pandas as pd
import pandas.tseries.offsets as offsets
from mdaq import pymdaq_web

import matplotlib as mpl
import matplotlib.pyplot as plt

print(pd.__version__)
print(mpl.__version__)

class ShiftLog:

    def __init__(self, x_or_s):
#        print("x_or_s = ",x_or_s)
        rest_api_host = 'srweb-dmz-03' if x_or_s =='xfel' else 'xfweb-dmz-03'
        self.db = pymdaq_web.db(rest_api_host, port=8888, debug=0)
        
    def __del__(self):
        self.db.close()
        
    def get_data(self, signame, from_dt, to_dt):
        db = self.db        
        res = db.get_data(signame,from_dt,to_dt)
        
        if db.status()!=pymdaq_web.DB_OK:
            print('Error: %d: %s' % (db.status(),db.err_msg()))
            return

        data = res
        nd = db.conv_pointdata_to_ndarray(data, split=False, use_mdates=False)  #時系列ログデータから取得した点データをNumPyのndarrayに変換 http://srweb-dmz-03.spring8.or.jp:8888/static/docs/mdaq_web_api/mdaq.html
        df = pd.DataFrame(nd, columns=['date', 'value'])
        df.sort_values('date', inplace=True)
        return df

    
    def record(self, begin_dt, end_dt, sig):
        #print(begin_dt)
        #print(sig)
        from_dt = begin_dt
        to_dt   = end_dt
        df = self.get_data(sig, from_dt, to_dt)    
        return df
    
    
    
    
    
"""
#箱ひげ図を表示するための関数を定義
def get_box(input_df):
  print("箱ひげ図を表示するための関数を定義")
  #入力のコピーを作成
  output_df=input_df.copy()
  #表示する図のサイズを指定
  fig = plt.figure(figsize=(20,20))
  #箱ひげ図で表示するデータの列を指定
  num_list=["value"]
  #指定した列分繰り返す
  for i in range(len(num_list)):
    #1出力に複数の図を表示できるように設定
    plt.subplot(len(num_list), 4, i+1)
    #箱ひげ図の表示
    output_df[num_list[i]].plot(kind="box")
  return output_df
"""

if __name__ == '__main__':


    print("arg len:",len(sys.argv))
    print("argv:",sys.argv)
    print("arg1:" + sys.argv[1])
    if len(sys.argv) <= 2:
        print("Need arg")
        sys.exit()

    conf_set = sys.argv[1]
    conf_sig = sys.argv[2]
    
    df_set = pd.read_excel(conf_set, sheet_name="setting", header=None, index_col=0)
    print(df_set)
    df_sig = pd.read_excel(conf_sig, sheet_name="sig")
    print(df_sig)




    begin_dt = '2024/06/27 02:51:00'
    end_dt = '2024/06/27 02:52:00'

    begin_dt = '2024/07/4 17:35:00'
    end_dt = '2024/07/4 17:45:00'
    
    log = ShiftLog(str(df_set.loc['x_or_s']).replace("1","").strip().splitlines()[0])
    print("figsize = ",plt.rcParams["figure.figsize"])  # default [6.4, 4.8]
    print("dpi = ",plt.rcParams["figure.dpi"])      # defalut 100.0      #ディスプレイ上に描画される図のサイズ デフォルト値は、ピクセル単位で640x480

#    print("len(df_sig) = ",len(df_sig))
    ax = [] * len(df_sig)
#    fig, (ax) = plt.subplots(nrows=len(df_sig), figsize=(5, 1 * 100))    #figsize で指定した(横幅, 縦幅) と dpi を掛け合わせると、生成される図のピクセル数が (横幅*dpi) × (縦幅*dpi) と求まる
#    fig, (ax) = plt.subplots(nrows=len(df_sig), figsize=(5, 1 * len(df_sig)))    #figsize で指定した(横幅, 縦幅) と dpi を掛け合わせると、生成される図のピクセル数が (横幅*dpi) × (縦幅*dpi) と求まる
    fig, (ax) = plt.subplots(nrows=len(df_sig), ncols=2, figsize=(5, 1 * len(df_sig)),   gridspec_kw=dict(width_ratios=[7,1], wspace=0.01, hspace=0.01))    #figsize で指定した(横幅, 縦幅) と dpi を掛け合わせると、生成される図のピクセル数が (横幅*dpi) × (縦幅*dpi) と求まる
    fig.patch.set_facecolor(str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0])
    fig.canvas.manager.set_window_title(str(df_set.loc['title']).replace("1","").strip())    

#    bx = [] * len(df_sig)
#    fig_b, (bx) = plt.subplots(nrows=len(df_sig), figsize=(1, 1 * len(df_sig)))    #figsize で指定した(横幅, 縦幅) と dpi を掛け合わせると、生成される図のピクセル数が (横幅*dpi) × (縦幅*dpi) と求まる
    
    for index, row in df_sig.iterrows():
        print (index,row["sname"], row["width"])
#        if index > 1:
#            continue
        df = pd.DataFrame()
        df = log.record(begin_dt, end_dt, row["sname"])   
        if df is None:
            print("df is None ~~~~~~~~~~~~~~~~~")
            continue

        print("ANS:",df.iloc[-1]['date'], " VAL:", df.iloc[-1]['value'])
#        print("ANS:",df.iloc[-2]['date'], " VAL:", df.iloc[-2]['value'])
#        print("MEAN:",df.value.mean())
#        print("STD:",df.value.std())

        latest = df.value.mean()    #(df.iloc[-1]['value']+df.iloc[-2]['value'])/2      # df.iloc[-1]['value']
        width  = df.value.std() * 3
        ax[index,0].plot(df['date'], df['value'], markersize=1, label=row["sname"], color=row['color'],linewidth=row["linewidth"])   #, clip_on=False)
        ax[index,0].set_ylim(latest - row["width"], latest + row["width"])   #固定幅
        ax[index,0].set_ylim(latest - width, latest + width)
        ax[index,0].patch.set_facecolor('gray')
        ax[index,0].grid(axis="x", linestyle=':', color='snow')
        ax[index,0].legend(loc='upper left', borderaxespad=0, fontsize="3") #, fontsize="100"

        ax[index,1].boxplot(df['value'])


#    plt.show()
#    sys.exit()
    
    plt.xticks(rotation=70)
    plt.savefig(str(df_set.loc['title']).replace("1","").strip().splitlines()[0]+'.png', dpi=300) # dip デフォルトは100


    
    
    
#    sys.exit()
#    raise SystemExit()
