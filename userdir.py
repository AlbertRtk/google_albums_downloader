import os


def check_user_dir(func):
    def check(cls_inst):
        user_dir = os.path.join(os.getcwd(), 'user')
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return func(cls_inst, user_dir=user_dir)
    return check
