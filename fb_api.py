#!/usr/bin/env python2
import facebook
import config
import pprint
import json
import requests

"""
https://graph.facebook.com/oauth/authorize?client_id=669315863177903&app_id=669315863177903&redirect_uri=http://fb-parser.int&type=client_cred&display=page&scope=publish_actions,publish_pages,user_photos,publish_stream,read_stream,user_likes
https://graph.facebook.com/oauth/authorize?client_id=".$app_id."&redirect_uri=".urlencode($canvas_page_url)."&type=client_cred&display=page&scope=user_photos,publish_stream,read_stream,user_likes"
"""


class FbParser(object):

    username = 'softproposal'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # code='AQClMjoXlFTLq_WjjDHOq04qCPERDlDHrFOks4GpRCF4R7ED9889leLdVbUEVV6zZUzssJsY8009KTwpgMuvmqs2KBsOtoPhNNt6-tFXQZ9JkKSRRFVmPX--iS6-O8RKHfH9On2I-KaGS-tYeyqd3tmFxrR9ayGQhzsY8XvbyB6pxV8a5xOfYHOemaK8X-T2UyIy4QBsm87sTgKXvJ2Iygv-KgY4xKSTdFjqGhkf9gUWhjn7dARwu9P4Emjjpq6Whs2g5BTGlZppgekoe1fZqwwtRshJUvi4XKF3d-1uE97Kd7Nk-8ddH1qS7DZHr9t6-TAxoceKHHP6c7NmqDC1XVS6#_=_'
        # self.token = facebook.get_access_token_from_code(code, 'http://fb-parser.int/', config.config['id'], config.config['secret'])

        self.token = facebook.get_app_access_token(config.app_config['id'], config.app_config['secret'])
        pprint.pprint(self.token)
        self.graph = facebook.GraphAPI(self.token)
        self.profile = self.graph.get_object(self.username)

    def get_data(self, index=0, link=False, method=False, object_id=False):

        obj_id = object_id if object_id else self.profile['id']

        if not link:
            if not method:
                return False
            data = self.graph.get_connections(obj_id, method, summary=True, limit=100)
            get_from = method + ' from ' + self.username
        else:
            r = requests.get(link)
            data = json.loads(r.content.decode("utf-8"))
            get_from = method + ' from ' + self.username

        if 'data' not in data:
            return False

        if method == 'likes':
            if data['summary']['total_count'] == 0:
                return False
            elif data['summary']['total_count'] < 26:
                print('get ' + str(len(data['data'])) + ' objects ' + get_from)
                return data['data']
            else:
                data = self.graph.get_connections(obj_id, method, summary=True, limit=data['summary']['total_count'])
                print('get ' + str(len(data['data'])) + ' objects ' + get_from)
                return data['data']

        index += len(data['data'])
        string = 'get %d ' % len(data['data'])
        print(string + get_from)
        print('all objects ' + str(index))

        next_data = False

        if 'paging' in data:
            if 'next' in data['paging']:
                next_data = self.get_data(index, data['paging']['next'], method)

        if next_data:
            data['data'].extend(next_data)

        return data['data']
        pass

    def get_posts(self):
        return self.get_data(method='posts')

    def get_feed(self):
        return self.get_data(method='feed')

    def get_photos(self):
        return self.get_data(method='photos')

    def get_likes(self):
        return self.get_data(method='likes')

    def get_likes_object(self, object_id=False):

        if not object_id:
            return False

        return self.get_data(method='likes', object_id=object_id)




fb = FbParser(username='freelanceuidesignerdeveloper')
list_ids = []
posts = fb.get_feed()

pprint.pprint(posts)
# for id in posts:
#     pprint.pprint(id)

users_dict = {}
permission_posts = []
for key, id in enumerate(list_ids):

    print(str(key+1) + ' in ' + str(len(list_ids)))

    try:
        likes_dict = fb.get_likes_object(id)
    except:
        permission_posts.append(id)
        continue

    if not likes_dict:
        continue


    for u in likes_dict:
        users_dict[u['id']] = u['name']
f = open('user_list.json', 'w')
data_json = json.dumps(posts)
data_json = data_json.replace(', "', ',\n\t"')
# data_json = data_json.replace('"}', '"\n}')
# data_json = data_json.replace('{"', '{\n\t"')

f.write(data_json)
f.close()
print(len(users_dict))


# code = 'AQC6d0Vbl0dEfeh65sidypbugzNkl3xwT4zrZwZ3yeUUGBblBiW2-ee8231ej22CbSdTAUOaM1bAbjyIXfEURBRjryFgFLsq-tq3Lqzv8TUizRcrHUSYBtJiFGkcKoEYSN996MAAi3bon_vH9CUUVsRV6Eebjf-ldQWwP_1YUvTaL0XCN90sCze1PXwebw8WuQCzxC1C4SP7quOQFGisXy6LDp29Fwitt8VlD-w0GHUZBxr05rWfXcJog71zZp1GBogE30y_hRUXCzxqHDNNKfQBxN7VIinNeTdeRpvC8ASljSQI0F_kPo3ryltgx97VbdSh3-xgG4wxAip1-uxPsiXG#_=_'