
class ChoiceTypes:
    '''
    base class for choice types
    '''
    @classmethod
    def get_name(cls, _id):
        '''
        returns string name for the given _id
        '''
        name = _id
        for choice in cls.CHOICES:
            if choice[0] == _id:
                name = choice[1]
        return name
