import json
from .hermes_skill_fault_gym import run
from .hermes_skill_fault_gym.metadata import DESCRIPTION
ERROR={'fr':'Entrée invalide pour le laboratoire local.','en':'Invalid input for the local laboratory.','es':'Entrada inválida para el laboratorio local.'}
def handle(args,**kwargs):
 lang=args.get('lang','en')if isinstance(args,dict)else'en'
 if lang not in ERROR:lang='en'
 try:
  if not isinstance(args,dict)or not isinstance(args.get('payload'),dict):raise ValueError('payload')
  result=run(args['payload']);return json.dumps({'language':lang,'summary':DESCRIPTION[lang],'result':result},ensure_ascii=False,allow_nan=False)
 except Exception:return json.dumps({'code':'invalid_input','message':ERROR[lang]},ensure_ascii=False)
def register(ctx):
 name='hermes_skill_fault_gym'
 schema={'name':name,'description':DESCRIPTION['fr']+' / '+DESCRIPTION['en']+' / '+DESCRIPTION['es'],'parameters':{'type':'object','properties':{'payload':{'type':'object','description':'Entrée JSON du laboratoire / Laboratory JSON input / Entrada JSON del laboratorio'},'lang':{'type':'string','enum':['fr','en','es']}},'required':['payload']}}
 ctx.register_tool(name=name,toolset=name,schema=schema,handler=handle)
