import pandas as pd
from multiprocessing import Pool
from food_manual import get_manual
from send_email import send_email

#load excel food table
xl = pd.ExcelFile('food_data.xlsx')
sheets = xl.sheet_names
df = xl.parse(sheets[0])

#多线程update 菜谱 & 步骤
# pool = Pool(processes = 7) # or some number of your choice
# df['tmp'] = pool.map(get_manual,  df['菜名']) #== df['菜名'].apply(get_manual)
# pool.terminate()
# 
# df['材料'] = df['tmp'].apply(lambda x : x[0])
# df['步骤'] = df['tmp'].apply(lambda x : x[1])
# df.drop(columns='tmp', axis=1, inplace=True)

#写入excel
writer = pd.ExcelWriter('food_data.xlsx')
df.to_excel(writer,'Sheet0')
writer.save()

#random 选择7天的菜谱
week_foods = df.sample(7)
week_food_names = '\n'.join(week_foods['菜名'].tolist())
week_ings = week_foods['材料'].sum()


#email 自己一周需要的食材
message = '你好，道菲。 这周为您精心(randomly) 挑选的菜单是：\n'
message = message + week_food_names
message = message + '\n\n 需要的食材是：\n'
message = message + week_ings
message = message + '\n\n请在DaoFei的 Program文件夹的food_data.xlsx 中添加菜名' 
+ '\n\n非常感谢您的参与'

send_email(message)
