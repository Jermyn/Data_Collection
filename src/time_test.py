# def in_between(now, start, end):
#     if start <= end:
#         return start <= now < end
#     else: # over midnight e.g., 23:30-04:15
#         return start <= now or now < end

# from datetime import datetime, time

# print("in between" if in_between(time(21), time(20), time(2)) else "not in between")   
# from datetime import datetime

# datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')   
# print (datetime_object)  

# from elasticsearch import Elasticsearch
# es = Elasticsearch(['http://137.132.165.139/api/devices'])  # use default of localhost, port 9200
# # es.index(index='posts', doc_type='blog', id=1, body={
# #     'author': 'Santa Clause',
# #     'blog': 'Slave Based Shippers of the North',
# #     'title': 'Using Celery for distributing gift dispatch',
# #     'topics': ['slave labor', 'elves', 'python',
# #                'celery', 'antigravity reindeer'],
# #     'awesomeness': 0.2
# # })
# 
# print (es.get())