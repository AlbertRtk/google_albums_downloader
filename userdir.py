import os


def user_dir(func):
    def set_dir(cls_inst):
        u_dir = os.path.join(os.getcwd(), 'user')
        if not os.path.exists(u_dir):
            os.makedirs(u_dir)
        return func(cls_inst, user_dir=u_dir)
    return set_dir
