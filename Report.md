# Report
## Time
### 누적그래프
* test,negative,confirmed,released,deceased 의 전체 양상 비교를 위해 숫자에 +1 이후 로그를 취한값을 비교하였다.
``` python 
def to_log(data):
    return np.log10(data+1)
 ㅜㅜㅜㅜㅜㅜ
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
```   


* ![이미지](https://github.com/kdj6394/COVID-19/blob/master/src/time_image/%EB%82%A0%EC%A7%9C%EB%B3%84%EC%9D%B8%EC%9B%90%EC%88%98(Log(1+N)).png?raw=true)


* 위의 그래프의 특정적인 지점은 __2020-02-18 부터 확진자 및 사망가 급증__, __누적격리수의 경우 2020-03-05 부터 소량 증가__ 함이 보인다.

### 일별그래프
* 누적결과로부터 일별검사,음성결과,양성결과,격리해재,사망수치를 구함.
```python 
one_day = pd.DataFrame(data=data.iloc[1:].values 
                            - data.iloc[:-1].values
                            ,columns= data.columns)
    one_day.index = data.index[1:]
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
```

* ![이미지](https://github.com/kdj6394/COVID-19/blob/master/src/time_image/%EB%82%A0%EC%A7%9C%EB%B3%84%EC%9D%B8%EC%9B%90%EC%88%98.png?raw=true)

### 테스트당 확진 비율 (확진율)
* 확진율 = 확진자 수/ 검사수 X 100
```python
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
```
* ![이미지](https://github.com/kdj6394/COVID-19/blob/master/src/time_image/%EB%82%A0%EC%A7%9C%EB%B3%84%ED%99%95%EC%A7%84%EC%9C%A8.png?raw=true)


* 전체    : 2.5645 %
* 최근 2주        : 2.1224 %

### 순수 확진자수
1. 순수확진자수는 누적확진자수에서 격리해제수와 사망자수를 제한한값
2. 순수확진자수 = 확진자수 - 격리해제수 - 사망자수
```python 
data['x'] = data['confirmed'] - data['released'] - data['deceased']

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
```
* ![이미지](https://github.com/kdj6394/COVID-19/blob/master/src/time_image/%EB%82%A0%EC%A7%9C%EB%B3%84%EC%88%9C%EC%88%98%ED%99%95%EC%A7%84%EC%9E%90%EC%88%98.png?raw=true)


### 순수 확진자수 예측
* 순수확진자수의 추세를 알아보기위해 Skew normal distribution 을 이용
```python
def skew_normal(x,m,a,s,n):
    t = (x-m)/s
    output = 2 / s * scipy.stats.norm.pdf(t) * scipy.stats.norm.cdf(a*t)
    return n*output

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
```
* ![이미지](https://github.com/kdj6394/COVID-19/blob/master/src/time_image/%EC%98%88%EC%B8%A1.png?raw=true)


### 결론
* 2020-02-18 부터 확진자가 급증
* 순수확진자수는 감소추세
* Skew normal distribution 을 가정, 2020-04-20 이후 순수확진자수가 1000명 이하로 예상


## Vis
### 2020-01-01 이후를 기준으로 검색추이 그래프생성
```python
Search=search_trend['date']
Search1Year=Search[1385:]
SearchC=search_trend['cold']
SearchCold=SearchC[1385:]
SearchF=search_trend['flu']
SearchFlu=SearchF[1385:]
SearchP=search_trend['pneumonia']
SearchPneumonia=SearchP[1385:]
SearchCorona=search_trend['coronavirus']
SearchCoronavirus=SearchCorona[1385:]

plt.figure(figsize=(15,8))
plt.plot(Search1Year,SearchCold)
plt.plot(Search1Year,SearchFlu)
plt.plot(Search1Year,SearchPneumonia)
plt.plot(Search1Year,SearchCoronavirus,'-o')
plt.title('검색추이')
plt.grid()
plt.xlabel('날짜')
plt.ylabel('검색량')
plt.xticks(fontsize=8,rotation=45)
plt.legend(['감기','발열','폐렴','코로나바이러스'],fontsize=8)
plt.show()
```
* ![이미지](검색추이) + vis부분 추가하기
