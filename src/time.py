from lib import np,pd,plt,warnings,datetime
import scipy.stats
from scipy.optimize import curve_fit
from lib import os,glob,join,basename,dirname,sys

def to_log(data):
    return np.log10(data+1)

def skew_normal(x,m,a,s,n):
    t = (x-m)/s
    output = 2 / s * scipy.stats.norm.pdf(t) * scipy.stats.norm.cdf(a*t)
    return n*output


if __name__ == '__main__':
    root = sys.argv[1]
    
    data = pd.read_csv(join(root,"Time.csv"),index_col=0)
    data.index = pd.to_datetime(data.index)
    
    '''
    date - 날짜
    time - 발표시간
    test - 누적 검사 수
    negative - 누적 음성 결과 수
    confirmed - 누적 양성 결과 수 (확진)
    released - 누적 격리 해제 수
    deceased - 누적 사망 수
    '''

    plt.figure(figsize=(12,4))
    plt.plot(to_log(data['test']), '-o', label='test', color='k')
    plt.plot(to_log(data['negative']), '-o', label='negative', color='gray')
    plt.plot(to_log(data['confirmed']), '-o', label='confirmed', color='r')
    plt.plot(to_log(data['released']), '-o', label='released', color='b')
    plt.plot(to_log(data['deceased']), '-o', label='deceased', color='g')
    plt.legend()
    plt.grid()
    plt.title('Number of people(Log(1+N)) by date')
    plt.ylabel('Log(1+N)')
    plt.xlabel('Date')
    plt.ylim(bottom=0)
    plt.xlim(data.index[0], data.index[-1])
    plt.xticks(rotation=30)
    plt.show()

    
    one_day = pd.DataFrame(data=data.iloc[1:].values 
                            - data.iloc[:-1].values
                            ,columns= data.columns)
    one_day.index = data.index[1:]
    print(one_day.head())
    plt.figure(figsize=(16, 4))
    plt.subplot(121)
    plt.plot(one_day['test'], '-o', label='test', color='k')
    plt.plot(one_day['negative'], '-o', label='negative', color='gray')
    plt.legend()
    plt.grid()
    plt.title('Number of people by date',fontsize=20)
    plt.ylabel('Number')
    plt.xlabel('Date')
    plt.ylim(bottom=0)
    plt.xlim(data.index[0], data.index[-1])
    plt.xticks(rotation=30)

    plt.subplot(122)
    plt.plot(one_day['confirmed'], '-o', label='confirmed', color='r')
    plt.plot(one_day['released'], '-o', label='released', color='b')
    plt.plot(one_day['deceased'], '-o', label='deceased', color='g')
    plt.legend()
    plt.grid()
    plt.title('Number of people by date',fontsize=20)
    plt.ylabel('Number')
    plt.xlabel('Date')
    plt.ylim(bottom=0)
    plt.xlim(data.index[0], data.index[-1])
    plt.xticks(rotation=30)
    plt.show()

    one_day['ratio'] = 100 * one_day['confirmed'] / one_day['test']
    
    plt.figure(figsize=(8, 4))
    plt.plot(one_day['ratio'], '-o', label='test', color='k')
    plt.ylabel('Number')
    plt.xlabel('Date')
    plt.ylim(bottom=0)
    plt.title('Confirmation rate',fontsize=20)
    plt.grid()
    plt.xlim(data.index[0], data.index[-1])
    plt.xticks(rotation=30)
    plt.show()
    print(one_day.head())
    print('확진율 (%) (확진자 수/검사 수 X 100)')
    print('전체\t: %.4f %%'%(one_day['ratio'].mean()))
    print('최근 2주\t: %.4f %%'%(one_day['ratio'].iloc[14:].mean()))

    data['x'] = data['confirmed'] - data['released'] - data['deceased'] # x = 확진자 - 격리해제자 - 사망자

    plt.figure(figsize= (8,4))
    plt.plot(data['x'],'-o',label='test',color='k')
    plt.ylabel('Number')
    plt.xlabel('Date')
    plt.title('Net number of confirmed persons',fontsize=20)
    plt.grid()
    plt.ylim(bottom=0)
    plt.xlim(data.index[0],data.index[-1])
    plt.xticks(rotation=30)
    plt.show()

    xdata = list(range(0, len(data)))
    ydata = data['x']
    popt, _ = curve_fit(skew_normal, xdata, ydata, bounds=([40, 3, 20, 200000], [45, 5, 25, 300000]))

    prediction = pd.DataFrame(index=pd.date_range(data.index[0], '2020-5-30'))
    prediction.index.name = 'date'
    prediction['data'] = np.NaN
    prediction['data'].loc[data['x'].index] = data['x']
    prediction['idx'] = list(range(0, len(prediction+1)))
    prediction['pred'] = prediction['idx'].apply(lambda x: skew_normal(x, popt[0], popt[1], popt[2], popt[3]))

    plt.plot(prediction['data'], '-o', label='data', color='k')
    plt.plot(prediction['pred'], '--', label='fit', color='r')
    plt.legend()
    plt.title('Prediction',fontsize=20)
    plt.grid()
    plt.ylabel('Number')
    plt.xlabel('Date')
    plt.ylim(bottom=0)
    plt.xlim(prediction.index[0], prediction.index[-1])
    plt.xticks(rotation=30)
    plt.show()

    