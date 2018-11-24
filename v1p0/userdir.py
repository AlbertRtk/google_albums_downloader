"""
AR, 2018-10-25
"""

import os


def user_dir(func):
    """
    Decorator to set directory of user local library

    :param func:
    :return:
    """
    def set_dir(cls_inst):
        u_dir = os.path.join(os.getcwd(), 'user')
        if not os.path.exists(u_dir):
            os.makedirs(u_dir)
        return func(cls_inst, user_dir=u_dir)
    return set_dir
