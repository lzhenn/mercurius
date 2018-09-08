#coding:utf-8

class _const:
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("cannot change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercases' % name)
        self.__dict__[name]=value

const=_const() 

# define const
const.MERC_ROOT='/home/lzhenn/workspace/mercurius'
const.UTILS_PATH=const.MERC_ROOT+'/src/utils'


