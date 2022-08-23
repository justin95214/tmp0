import pandas as pd
import numpy as np
import DB


#네이버/쿠팡/지마켓/이마트
def filter(naver, coupang, gmarket, emart):


	naver_df = pd.DataFrame()  
	coupang_df = pd.DataFrame()
	gmarket_df = pd.DataFrame()
	emart_df = pd.DataFrame()

	try:	
		TABLE_NAME = 'gmarket'
		ENGINE_URL = 'mysql+pymysql://root:qwer1234@localhost:3306/kurly?charset=utf8mb4'
		# engineUrl = 'mysql+pymysql://root:root@localhost:3306/kurly?charset=utf8mb4'

		db = DB(TABLE_NAME, ENGINE_URL)
		conn = db.get_conn()

		conn.execute('SET NAMES utf8;')
		conn.execute('SET CHARACTER SET utf8;')
		conn.execute('SET character_set_connection=utf8;')

	except:
		print(f'아직 DB 구현이 안됨')

	## 합칠 데이터프레임
	total_df = pd.DataFrame()

	if naver == True:
		naver_df = pd.read_csv("./naver.csv", encoding='utf8')	
		naver_df['unit_price'] = naver_df['price'].copy()
		naver_df['price'] = naver_df['unit_price']* naver_df['weight']
		naver_df.fillna(np.NaN)
		naver_df['weight'].dropna()
		total_df = pd.concat([total_df, naver_df],  ignore_index=True)

	if coupang == True:
		coupang_df = pd.read_csv("./coupang.csv", encoding='utf8')
		coupang_df['unit_price'] = coupang_df['price'].copy()
		coupang_df['unit_price'] = coupang_df['unit_price'].round()
		coupang_df['price'] = coupang_df['unit_price']* coupang_df['weight']
		#coupang_df['unit_price'] = coupang_df['unit_price']
		total_df = pd.concat([total_df, coupang_df],  ignore_index=True)
		

	if gmarket == True:
		gmarket_df = pd.read_csv("./gmarket.csv", encoding='utf8')

		gmarket_df['weight'].replace('None',np.NaN)

		gmarket_df['weight'].dropna()
		
		gmarket_df['unit_price'] = gmarket_df['price']/gmarket['weight']
		#gmarket_df['unit_price'] = gmarket_df['unit_price']
		gmarket_df = pd.concat([total_df, gmarket_df],  ignore_index=True)

	#if emart == True:
	#	emart_df = pd.read_csv("./emart.csv", encoding='utf8')
	#	total_df = pd.concat([emart_df, emart_df],  ignore_index=True)
	
	return total_df



## 특정 위치의 배경색 바꾸기
def draw_color_cell(x,color):
	color = f'background-color:{color}'
	return color 


def make_pivot(df):
	
	df.style.applymap(draw_color_cell,color='#ff9090',subset=pd.IndexSlice[2:5,'kind':'site'])
	df.to_csv("result_temp.csv", encoding='cp949')
	df0 = pd.pivot_table(df, index='location', columns = 'unit_price', values='price', aggfunc='count')
	df0 = df0.fillna("")
	print(df0.columns)
	df0.style.applymap(draw_color_cell,color='#ff9090',subset=pd.IndexSlice[2:5,'1333':'1490'])
	return df0



result = filter(True, True, False, True)
table = make_pivot(result)
table.to_excel("result.xlsx", encoding='cp949', engine='openpyxl')
print(table)


