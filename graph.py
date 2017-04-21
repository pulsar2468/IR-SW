import time

import sys
import tweepy
from tweepy.streaming import StreamListener



def get_user_information(get_name_account):
    '''
    matches = api.lookup_users(user_ids=identificativo)

    if len(matches) != 1:
        print('sorry the name not exist')
        exit()

'''
    while True:
        try:
            user = api.get_user(get_name_account)
            d = {'name': user.name,
                 'screen_name': user.screen_name,
                 'id': user.id,
                 'friends_count': user.friends_count,
                 'followers_count': user.followers_count,
                 'followers_ids': user.followers_ids()}
            return d['id']
        except tweepy.TweepError as e:
            if ('88' in e.reason):
                print('Wait: 15 min\n')
                time.sleep(60 * 15)
            else:
                print('Name not exist! You try with another name\n')
                exit()


# I get all following of the node considered
def get_following(node):
    while True:
        try:
            users = tweepy.Cursor(api.friends_ids, id=node, count=n_node).pages(1)
            l = list()
            for i in users:
                for user in i:
                    l.append(user)
            return l


        except tweepy.TweepError as e:
            if ('88' in e.reason):
                print('Wait: 15 min\n')
                time.sleep(60 * 15)
            else:
                print('I cannot to get data from one account\nTweet are protected\n')
                return l


def get_follower(node):
    users = tweepy.Cursor(api.friends_ids, id=node, count=200)
    l = list()
    for i in users.pages():
        for user in i:
            l.append(user)
    return l


def create_abstraction_file_test(name, first_l, second_l, thirt_l, forth_l):
    try:
        with open(name, 'w') as f:

            for item in first_l:
                f.write(get_name_account + ':' + "%s\n" % item)

            i = 0
            for item in second_l:
                f.write(str(first_l[0][i]) + ':' + "%s\n" % item)
                i += 1
            i = 0

            j_index = 0
            for j in range(0, len(second_l)):
                for i in range(0, len(second_l[j])):
                    f.write(str(second_l[j][i]) + ':' + "%s\n" % thirt_l[j_index])
                    j_index += 1

            j_index = 0
            for j in range(0, len(thirt_l)):
                for i in range(0, len(thirt_l[j])):
                    f.write(str(thirt_l[j][i]) + ':' + "%s\n" % forth_l[j_index])
                    j_index += 1

            f.close()

    except IOError:
        print('File not found!')
        exit('Exit')


'''
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)
'''

# Error Control
# ****************************************************
if (len(sys.argv) != 3):
    print('Error Missing parameters\n')
    exit()

else:
    try:
        if int(sys.argv[1]) > 5:
            print('Remember  that it is set on the fourth depth level, please insert this variable wisely!\n')
            exit()
    except Exception as e:
        print('Input error! You must insert a number\n')
        exit()


# enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'NM4xHHBwm7fiBQjf0X4QfdN8X'  # keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'u6pnGad8o11sNhLiY77voEbAUawHejgGiVgxKBwPFVKLyLyRbD'  # keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '251060755-lUeE2kxqXjMfL5hLqzmo4EuyuWo4wYmqcihTEU0o'  # keep the quotes, replace this with your access token
ACCESS_SECRET = 'sUCSFY1PkPkVxVD5P96EixYzCjJnUapeXmzyJ8HQ1UW2s'  # keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

# get data from terminal -_> argv[1],argv[2] --> following for each account and name of the account
n_node = int(sys.argv[1])
get_name_account = str(get_user_information(sys.argv[2]))

'''
# l = StdOutListener()
# stream = Stream(auth, l)
# stream.filter(track='trump', languages=['en'])
'''

first_level = []
second_level = []
thirt_level = []
fourth_level = []

first_level.append(get_following(get_name_account))  # i'm your father

start = time.time()

for i in range(0, len(first_level)):
    for j in range(0, len(first_level[i])):
        second_level.append(get_following(first_level[i][j]))  # following dei miei following, rappresenta il secondo livello di astrazione
        # create_abstraction_file('/home/nataraja/Scrivania/data_set/second_level/'+get_user_information(first_level[i][j])+'.text', second_level[len(second_level)-1])

for i in range(0, len(second_level)):
    for j in range(0, len(second_level[i])):
        thirt_level.append(get_following(second_level[i][j]))
        # create_abstraction_file('/home/nataraja/Scrivania/data_set/thirt_level/'+get_user_information(second_level[i][0][j])+'.text', thirt_level[len(thirt_level)-1])

for i in range(0, len(thirt_level)):
    for j in range(0, len(thirt_level[i])):
        fourth_level.append(get_following(thirt_level[i][j]))

end = time.time()
print('Time:', end - start)

print('First abstraction level', first_level)
print('Second abstraction level', second_level)
print('Thirt abstraction level', thirt_level)
print('Fourth abstraction level', fourth_level)

create_abstraction_file_test('data_set/graph_format_text/'+sys.argv[2]+'.text', first_level, second_level, thirt_level,fourth_level)
