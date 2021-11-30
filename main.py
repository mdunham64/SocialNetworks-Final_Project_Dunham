from TikTokApi import TikTokApi

verifyFp_Cookie = "verify_khr3jabg_V7ucdslq_Vrw9_4KPb_AJ1b_Ks706M8zIJTq"


def starting_user(search_term):
    api = TikTokApi.get_instance()

    users = api.search_for_users(search_term=search_term, count=1)

    if users is None:
        print('Uh ohh. No user found...')
        return

    for user in users:
        user_obj = user['user']
        user_id = user_obj['id']
        user_username = user_obj['uniqueId']
        user_nickname = user_obj['nickname']
        print("user's account name: ", user_username)
        print("user's nickname: ", user_nickname)
        print("user's id: ", user_id)



def get_suggested_videos(starting_id, count=10):
    api = TikTokApi.get_instance(custom_verifyFp=verifyFp_Cookie)

    tiktoks = api.get_suggested_users_by_id_crawler(startingId=starting_id)
    for tiktok in tiktoks:
        print(tiktok)

if __name__ == '__main__':
    starting_user("mizkif")
    get_suggested_videos(6753412046878753797)
