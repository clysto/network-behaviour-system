import random
import csv
import datetime

# Define the groups
groups = ['大一', '大二', '大三', '大四']

# Define the IP address range
ip_range = ['192.168.' + str(i) + '.' + str(j) for i in range(256) for j in range(256)]

# Define the URL prefix
url_prefix = ['http://www.', 'https://www.', 'http://', 'https://']

# Define the URL suffix
url_suffix = ['.com', '.org', '.net', '.cn']

# Define the start ID
start_id = 1000000

# Define the start time
start_time = datetime.datetime(2023, 4, 21, 16, 0, 0)

# Define the end time
end_time = datetime.datetime(2023, 4, 21, 19, 0, 0)

# Generate the data
data = []
for i in range(10000):
    group = random.choice(groups)
    ip = random.choice(ip_range)
    url = random.choice(url_prefix) + str(random.randint(1, 100)) + random.choice(url_suffix)
    time = start_time + datetime.timedelta(seconds=random.randint(0, int((end_time - start_time).total_seconds())))
    data.append([start_id + i, ip, 'xiaojiawei@qq.com', group, i+1, random.randint(10000, 65535), round(random.uniform(0, 1), 4), random.choice(ip_range), time.strftime('%Y/%m/%d %H:%M'), url, 700])

# Append the data to the CSV file
with open('data.csv', 'a', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(data)
