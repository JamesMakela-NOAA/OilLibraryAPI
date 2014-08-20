""" Cornice services.
"""
from cornice import Service
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.orm.exc import NoResultFound

from ..common.views import cors_policy, obj_id_from_url
from ..models import DBSession
from oil_library.models import Oil

oil_api = Service(name='oil', path='/oil*obj_id',
                  description="List All Oils",  cors_policy=cors_policy)


@oil_api.get()
def get_oils(request):
    '''Returns all oils in JSON format'''
    obj_id = obj_id_from_url(request)

    if not obj_id:
        oils = DBSession.query(Oil)
        return [{'name': o.name,
                 'adios_oil_id': o.adios_oil_id,
                 'api': o.api,
                 'location': o.location,
                 'field_name': o.field_name,
                 'product_type': o.product_type,
                 'oil_class': o.oil_class,
                 'categories': get_category_paths(o)}
                for o in oils]
    else:
        try:
            oil = (DBSession.query(Oil)
                   .filter(Oil.adios_oil_id == obj_id).one())
            return oil.tojson()
        except NoResultFound:
            raise HTTPNotFound()


def get_category_paths(oil, sep='-'):
    return [sep.join([c.name for c in get_category_ancestors(cat)])
            for cat in oil.categories]


def get_category_ancestors(category):
    '''
        Here we take a category, which is assumed to be a node
        in a tree structure, and determine the parents of the category
        all the way up to the apex.
    '''
    cat_list = []
    cat_list.append(category)

    while category.parent != None:
        cat_list.append(category.parent)
        category = category.parent

    cat_list.reverse()
    return cat_list
