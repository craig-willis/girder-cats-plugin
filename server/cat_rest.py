from girder.api.rest import Resource
from girder.api import access
from girder.api.rest import Resource, filtermodel, RestException
from girder.api.describe import Description, autoDescribeRoute
from girder.constants import SortDir, AccessType
from .models.cat import Cat as CatModel

class Cat(Resource):
    def __init__(self):
        super(Cat, self).__init__()
        self.resourceName = 'cat'
        self._model = CatModel()
        self.route('GET', (), self.listCats)
        self.route('GET', (':id',), self.getCat)
        self.route('POST', (), self.createCat)
        #self.route('PUT', (':id',), self.updateCat)
        self.route('DELETE', (':id',), self.deleteCat)
        
    @access.public
    @filtermodel(model='cat', plugin='cats')
    @autoDescribeRoute(
        Description('Return all the cats accessible to the user')
        .param('userId', "The ID of the cats's creator.", required=False)
        .param('text', ('Perform a full text search for cat with matching '
                        'name or description.'), required=False)
        .pagingParams(defaultSort='lowerName',
                      defaultSortDir=SortDir.DESCENDING)
    )
    def listCats(self, userId, text, limit, offset, sort, params):
        currentUser = self.getCurrentUser()
        if userId:
            user = self.model('user').load(userId, force=True, exc=True)
        else:
            user = None
            
        return list(self._model.list(
                user=user, currentUser=currentUser,
                offset=offset, limit=limit, sort=sort))
                
    @access.public
    @filtermodel(model='cat', plugin='cats')
    @autoDescribeRoute(
        Description('Get a cat by ID.')
        .modelParam('id', model='cat', plugin='cats', force=True)
        .errorResponse('ID was invalid.')
        .errorResponse('Read access was denied for the cat', 403)
    )
    def getCat(self, cat, params):
        return cat                


    @access.user
    @autoDescribeRoute(
        Description('Create a new cat.')
        .jsonParam('cat', 'Name and qualities of the cat.', paramType='body')
        .responseClass('cat')
        .errorResponse('You are not authorized to create cats.', 403)
    )
    def createCat(self, cat):
        user = self.getCurrentUser()

        return self._model.createCat(
            cat, creator=user, save=True)

    @access.user
    @autoDescribeRoute(
        Description('Delete an existing cat.')
        .modelParam('id', 'The ID of the cat.',  model='cat', plugin='cats', level=AccessType.ADMIN)
        .errorResponse('ID was invalid.')
        .errorResponse('Admin access was denied for the cat.', 403)
    )
    def deleteCat(self, cat):
        self.model('cat', 'cats').remove(cat)