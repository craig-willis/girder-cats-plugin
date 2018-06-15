from . import cat_rest


def load(info):
    info['apiRoot'].cat = cat_rest.Cat()
    
    