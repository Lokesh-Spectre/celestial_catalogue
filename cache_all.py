import pandas as pd
import time
import pickle
start = time.time()
df = pd.read_csv('data/hygdata.csv')
mainDB = {}
# all, HIPPACARAS, HD, HR, glice
# mainDB
for _, i in df.iterrows():
    mainDB[i[0]] = dict(zip(df.keys(), i.tolist()))
mainDB_file = open('DB/mainDB', 'wb')
pickle.dump(mainDB, mainDB_file)
mainDB_file.close()
print('mainDB -- check!!', time.time()-start)
# HIPPACARAS satellite catalogue
hip = {}
for _, i in df.iterrows():
    if i[1] == i[1]:
        hip[i[1]] = i[0]
    else:
        continue
hip_file = open('DB/hip', 'wb')
pickle.dump(hip, hip_file)
hip_file.close()
print('hip -- check!!', time.time()-start)
# Henry Draper catalogue
n = 2
hd_data = {}
for _, i in df.iterrows():
    if i[n] == i[n]:
        hd_data[i[n]] = i[0]
    else:
        continue
hd_file = open('DB/hd', 'wb')
pickle.dump(hd_data, hd_file)
hd_file.close()
print('HD -- check!!', time.time()-start)
# hertzsprung russell catalogue
n = 3
hr_data = {}
for _, i in df.iterrows():
    if i[n] == i[n]:
        hr_data[i[n]] = i[0]
    else:
        continue
hr_file = open('DB/hr', 'wb')
pickle.dump(hr_data, hr_file)
hr_file.close()
print('HR -- check!!', time.time()-start)

# Gliese catalaogue
n = 4
gl_data = {}
for _, i in df.iterrows():
    if i[n] == i[n]:
        gl_data[i[n]] = i[0]
    else:
        continue
gl_file = open('DB/gl', 'wb')
pickle.dump(gl_data, gl_file)
gl_file.close()
print('Gliese -- check!!', time.time()-start)

# search caches
print('\nSearch cache !!', time.time()-start)
# luminosity
lum_data = []
for _, i in df.iterrows():
    lum_data.append((i[16], i[0]))
lum_data = tuple(sorted(lum_data))
lum_file = open('DB/lum_sch', 'wb')
pickle.dump(lum_data, lum_file)
lum_file.close()
print('luminosity -- check!!', time.time()-start)

# Distance
dist_data = []
for _, i in df.iterrows():
    dist_data.append((i[7], i[0]))
dist_data = tuple(sorted(dist_data))
dist_file = open('DB/dist_sch', 'wb')
pickle.dump(dist_data, dist_file)
dist_file.close()
print('Distance -- check!!', time.time()-start)

# magnitude
mag_data = []
for _, i in df.iterrows():
    mag_data.append((i[8], i[0]))
mag_data = tuple(sorted(mag_data))
mag_file = open('DB/mag_sch', 'wb')
pickle.dump(mag_data, mag_file)
mag_file.close()
print('Magnitude -- check!!', time.time()-start)
with open('DB/mainDB', 'rb') as file:
    mainDB = pickle.load(file)
df = pd.read_csv('data/stars_alpha-names.csv')
ch_data = {}
for _, i in df.iterrows():
    if 'HR' in i[1]:
        HR = int(i[1][2:])
        for j in mainDB.values():
            if HR==j['hr']:
                break
        ch_data[i[0].lower()] = j['id']
ch_file = open('DB/names', 'wb')
pickle.dump(ch_data, ch_file)
ch_file.close()
print('names -- check!!', time.time()-start)
