#coding:utf-8

import json

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

with open ('/home/lzhenn/workspace/mercurius/config_files/basic_info.json','r') as f:
    tgt_json=json.load(f)

# define const for PATH
const.MERC_ROOT=tgt_json['MERC_ROOT']
const.UTILS_PATH=const.MERC_ROOT+'/src/utils'
const.CFG_TARGET_FILE=const.MERC_ROOT+'/config_files/config_targets.json'
const.CFG_PORTFOLIO_FILE=const.MERC_ROOT+'/config_files/daily_portfolio_routine.json'


# define const for the MARKET
const.NO_RISK_RETURN=tgt_json['NO_RISK_RETURN']
const.US_AVG_DIV=tgt_json['US_AVG_DIV']
const.TRAD_DAYS_PER_YEAR=tgt_json['TRAD_DAYS_PER_YEAR']
