from common import connect_to_mongodb, connect_to_maindb


client = connect_to_mongodb()
db = client['fetcher']
collection = db['collected_url']

main_client = connect_to_maindb()
maindb = main_client['zeno_db']
maincollection = maindb['articles_app_article']

# doc = collection.find_one({"url": "http://businessmirror.com.ph/2025/08/21/chinese-marine-scientists-eye-collaboration-with-filipinos-to-protect-south-china-sea-ecosystem"})
# print(doc)

# for document in collection.find():
#     url = document['url']
#     doc = maincollection.find_one({'article_url':'http://businessmirror.com.ph/2025/08/21/chinese-marine-scientists-eye-collaboration-with-filipinos-to-protect-south-china-sea-ecosystem'})
#     if doc:
#         print(doc)
#     else:
#         print('error')

doc = maincollection.find_one({
    "article_clean_url":{"$regex":"businessmirror.com.ph"},
    "article_clean_url":{"$regex":"chinese-marine-scientists-eye-collaboration-with-filipinos-to-protect-south-china-sea-ecosystem"}
    })
print(doc)
