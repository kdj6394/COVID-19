from lib import os,join,basename,dirname
from lib import pd,np,plt,warnings
from lib import sns,folium
warnings.filterwarnings(action='ignore')
plt.rc('font',family='Malgun Gothic') #한글폰트설정 안하니깐 깨짐

def barplot_h(data, y:str, x:str, str_color:str):
    print('Head',data.head(),sep='\n')
    print('Info',data.info(),sep='\n')
    print('Shape',data.shape)
    plt.barh(data[y],data[x]
    ,label = x,align='center',linewidth = 10)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid()
    plt.legend()
    plt.title(x+"별"+y)
    for i,v in enumerate(data[y]):
        str_val = data[x][i]
        plt.text(data[x][i],v,str_val,fontsize=9,color=str_color,
        horizontalalignment = 'left',verticalalignment = 'center',fontweight = 'bold')
    plt.show()

def sns_lineplot(data, y:str, x:str,hue,title:str):
    if hue == 0:
        print('Head',data.head(),sep='\n')
        print('Info',data.info(),sep='\n')
        print('Shape',data.shape)
        plt.figure(figsize=(14,7))
        plt.xticks(rotation=90)
        plt.title(title,fontsize=20)
        plt.xlabel(x,fontsize=15)
        plt.ylabel(y,fontsize=15)
        sns.lineplot(data=data,x=x,y=y)
        plt.show()
    else:
        print('Head',data.head(),sep='\n')
        print('Info',data.info(),sep='\n')
        print('Shape',data.shape)
        plt.figure(figsize=(14,7))
        plt.xticks(rotation=60)
        plt.title(title,fontsize=20)
        plt.xlabel(x,fontsize=15)
        plt.ylabel(y,fontsize=15)
        sns.lineplot(data=data,x=x,y=y,hue=hue)
        plt.show()

def sns_barplot(data,y:str,x:str,title:str):
    print('Head',data.head(),sep='\n')
    print('Info',data.info(),sep='\n')
    print('Shape',data.shape)
    plt.figure(figsize=(15,7))
    plt.title(title,fontsize=30)
    plt.xlabel(x, fontsize=20)
    plt.ylabel(y, fontsize=20)
    sns.barplot(data=data, x=x, y=y)
    plt.show()

def folium_polyline_coords(data,x:str,y:str,a:str,b:str,c:str,savepath,savename:str,color):
    lists = []
    for n in data.index:
        points = (data.loc[n,x],data.loc[n,y])
        lists.append(points)

    draw_map = folium.Map(location=[data[x].mean(), data[y].mean()], zoom_start=11)

    for n in data.index:
        folium.Marker(location=[data.loc[n, x], data.loc[n, y]],popup=data.loc[n, a]+" : "+
                    data.loc[n, b]+","+data.loc[n, c]).add_to(draw_map)
    lists = []
    for n in data.index:
        points = (data.loc[n, x], data.loc[n, y])
        lists.append(points)
        
    folium.PolyLine(lists,color=color).add_to(draw_map)
    draw_map.save(join(savepath,savename+'.html'))

if __name__ == '__main__':
    root = r'C:\Users\82104\Documents\Data\Corona\coronavirusdataset_20200328'
    map_save_path = r'C:\Users\82104\Documents\Data\Corona_vis'
    # root = r'D:\coronavirusdataset_20200328'

    region = pd.read_csv(join(root,"Region.csv"))
    timeprovince = pd.read_csv(join(root,"TimeProvince.csv"))
    timegender = pd.read_csv(join(root,"TimeGender.csv"))
    timeage = pd.read_csv(join(root,"TimeAge.csv"))
    time = pd.read_csv(join(root,"Time.csv"))
    patientinfo = pd.read_csv(join(root,"PatientInfo.csv"))
    patientroute = pd.read_csv(join(root,"PatientRoute.csv"))
    case = pd.read_csv(join(root,"Case.csv"))
    weather = pd.read_csv(join(root,"Weather.csv"))


    case.columns = ['환자번호','시도','구군','집단감염여부','집단감염장소','확진자누적수','위도','경도']
    
    df_location = pd.DataFrame(case.groupby(['집단감염장소'])['확진자누적수'].max())
    df_location = df_location.sort_values(by=['집단감염장소'], ascending = True).reset_index()
    barplot_h(df_location,'집단감염장소','확진자누적수','Red')


    time.columns = ['날짜','시간','검사자누적숫자','음성누적숫자','양성누적숫자','완치누적숫자','사망누적숫자']
    df_test = time.pivot_table(index='날짜',values='검사자누적숫자',aggfunc=np.sum).reset_index()
    sns_lineplot(df_test,'검사자누적숫자','날짜',0,'날짜별 검사자 누적수')
    
    df_neg = time.groupby(['날짜'])['음성누적숫자'].max().reset_index()
    sns_lineplot(df_neg,'음성누적숫자','날짜',0,'날짜별 음성 누적수')
    
    df_pos = time.groupby(['날짜'])['양성누적숫자'].max().reset_index()
    sns_lineplot(df_pos,'양성누적숫자','날짜',0,'날짜별 양성 누적수')

    df_rel = time.groupby(['날짜'])['완치누적숫자'].max().reset_index()
    sns_lineplot(df_rel,'완치누적숫자','날짜',0,'날짜별 완치 누적수')

    df_dec = time.groupby(['날짜'])['사망누적숫자'].max().reset_index()
    sns_lineplot(df_dec,'사망누적숫자','날짜',0,'날짜별 사망 누적수')

    plt.figure(figsize=(15,7))
    plt.plot(time['날짜'], time['양성누적숫자'], color='red')
    plt.plot(time['날짜'], time['완치누적숫자'], color='green')
    plt.plot(time['날짜'], time['사망누적숫자'], color='black')
    plt.xticks(rotation=90, size=10)
    plt.yticks(size=13)
    plt.xlabel('날짜', fontsize=20)
    plt.ylabel('누적숫자', fontsize=20)
    plt.legend(['양성','완치','사망자'], loc='best', fontsize=20)
    plt.title('Corona_Virus 진단별 누적 숫자 추이', size=30)
    plt.show()



    timeage = timeage.drop(['time'],axis=1)
    timeage.columns = ['날짜','연령대','확진자누적수','사망자누적수']

    timeage['날짜'] = pd.to_datetime(timeage['날짜'])
    timeage.loc[timeage['연령대'] == '0s', '연령대'] = '0세이상 10세미만'
    timeage.loc[timeage['연령대'] == '10s', '연령대'] = '10세이상 20세미만'
    timeage.loc[timeage['연령대'] == '20s', '연령대'] = '20세이상 30세미만'
    timeage.loc[timeage['연령대'] == '30s', '연령대'] = '30세이상 40세미만'
    timeage.loc[timeage['연령대'] == '40s', '연령대'] = '40세이상 50세미만'
    timeage.loc[timeage['연령대'] == '50s', '연령대'] = '50세이상 60세미만'
    timeage.loc[timeage['연령대'] == '60s', '연령대'] = '60세이상 70세미만'
    timeage.loc[timeage['연령대'] == '70s', '연령대'] = '70세이상 80세미만'
    timeage.loc[timeage['연령대'] == '80s', '연령대'] = '80세이상'


    timeage['날짜'] = timeage['날짜'].astype(str)
    age_max = timeage.loc[timeage['날짜'] == '2020-03-20'].reset_index(drop=True)

    barplot_h(age_max,'연령대','확진자누적수','red')
    barplot_h(age_max,'연령대','사망자누적수','red')

    timegender.columns = ['날짜','시간','성별','확진자누적수','사망자누적수']
    sns_lineplot(timegender,'확진자누적수','날짜','성별','성별에따른 날짜별 확진자 누적수')
    sns_lineplot(timegender,'사망자누적수','날짜','성별','성별에따른 날짜별 사망자 누적수')


    data = patientinfo.copy()
    data['contact_number'] = data['contact_number'].fillna(0)

    df_infection = data.loc[data['contact_number'] >= 16].reset_index(drop=True)
    columns = ['sex','age','country','province','city','infection_case','contact_number','confirmed_date','released_date']
    df_infection = df_infection.loc[:,columns]
    df_infection.columns = ['성별','연령','국적','시도','구군','감염장소','접촉자수','확진날짜','퇴원날짜']

    df_infection['연령'] = df_infection['연령'].fillna('unknown')
    df_infection.loc[df_infection['연령'] == 'unknown']
    df_infection = df_infection.loc[df_infection['연령'].str.contains('10s|20s|30s|40s|50s|60s|70s')]

    df_infection.loc[df_infection['연령'] == '10s', '연령'] = '10세이상 20세미만'
    df_infection.loc[df_infection['연령'] == '20s', '연령'] = '20세이상 30세미만'
    df_infection.loc[df_infection['연령'] == '30s', '연령'] = '30세이상 40세미만'
    df_infection.loc[df_infection['연령'] == '40s', '연령'] = '40세이상 50세미만'
    df_infection.loc[df_infection['연령'] == '50s', '연령'] = '50세이상 60세미만'
    df_infection.loc[df_infection['연령'] == '60s', '연령'] = '60세이상 70세미만'
    df_infection.loc[df_infection['연령'] == '70s', '연령'] = '70세이상 80세미만'
    df_infection.loc[df_infection['연령'] == '80s', '연령'] = '80세이상'
    
    sns_barplot(df_infection,'접촉자수','연령','연령별접촉자수')

    df_route = patientroute.copy()
    df_route.columns = ['환자번호','global_num','날짜','시도','구군','위도','경도']
    df_route['환자번호'] = df_route['환자번호'].astype(str)

    '''
    가장 많이 돌아다닌 확진자 상위 4명 환자번호 id 
    1000000013    29
    2000000003    18
    2000000006    15
    1000000014    11
    '''


    df_route_many = df_route.loc[df_route['환자번호'].str.contains('1000000013|2000000003|2000000006|1000000014')]
    
    df_route_max = df_route_many.loc[df_route_many['환자번호'] == '1000000013']
    df_route_max = df_route_max.reset_index(drop=True)
    geo_df_1st = df_route_max
    folium_polyline_coords(geo_df_1st,'위도','경도','날짜','시도','구군',map_save_path,'1st','red')
    
    df_route_2nd = df_route_many.loc[df_route_many['환자번호'] == '2000000003']
    df_route_2nd = df_route_2nd.reset_index(drop=True)
    geo_df_2nd = df_route_2nd
    folium_polyline_coords(geo_df_2nd,'위도','경도','날짜','시도','구군',map_save_path,'2nd','red')

    df_route_3rd = df_route_many.loc[df_route_many['환자번호'] == '2000000006']
    df_route_3rd = df_route_3rd.reset_index(drop=True)
    geo_df_3rd = df_route_3rd
    folium_polyline_coords(geo_df_3rd,'위도','경도','날짜','시도','구군',map_save_path,'3rd','red')

    df_route_4th = df_route_many.loc[df_route_many['환자번호'] == '1000000014']
    df_route_4th = df_route_4th.reset_index(drop=True)
    geo_df_4th = df_route_4th
    folium_polyline_coords(geo_df_4th,'위도','경도','날짜','시도','구군',map_save_path,'4th','red')

    

    geo_df = df_route_many
    map_all = folium.Map(location=[geo_df['위도'].mean(), geo_df['경도'].mean()], zoom_start=8)

    for n in geo_df.index:
        # 1위:파란색, 2위:빨간색, 3위:초록색, 4위:오렌지색
        if geo_df.loc[n, '환자번호'] == '1000000013':
            icon_color = 'blue'
        elif geo_df.loc[n, '환자번호'] == '2000000003':
            icon_color = 'red'
        elif geo_df.loc[n, '환자번호'] == '2000000006':
            icon_color = 'green'
        else:
            icon_color = 'orange'
        
        folium.CircleMarker(location=[geo_df.loc[n, '위도'], geo_df.loc[n, '경도']],
                    popup="환자번호 :"+geo_df.loc[n, '환자번호']+" - 날짜:"+geo_df.loc[n, '날짜']+' 시도 :'+geo_df.loc[n, '시도']+
                            " 구군 :"+geo_df.loc[n, '구군'], color=icon_color, fill_color=icon_color, fill=True,
                        radius=9).add_to(map_all)

    lists1 = []
    for n in df_route_max.index:
        points = (df_route_max.loc[n, '위도'], df_route_max.loc[n, '경도'])
        lists1.append(points)
    folium.PolyLine(lists1, color='blue').add_to(map_all)

    lists2 = []
    for n in df_route_2nd.index:
        points = (df_route_2nd.loc[n, '위도'], df_route_2nd.loc[n, '경도'])
        lists2.append(points)
        
    folium.PolyLine(lists2, color='red').add_to(map_all)

    lists3 = []
    for n in df_route_3rd.index:
        points = (df_route_3rd.loc[n, '위도'], df_route_3rd.loc[n, '경도'])
        lists3.append(points)

    folium.PolyLine(lists3, color='green').add_to(map_all)

    lists4 = []
    for n in df_route_4th.index:
        points = (df_route_4th.loc[n, '위도'], df_route_4th.loc[n, '경도'])
        lists4.append(points)

    folium.PolyLine(lists4, color='orange').add_to(map_all)

    map_all.save(join(map_save_path,'all.html'))