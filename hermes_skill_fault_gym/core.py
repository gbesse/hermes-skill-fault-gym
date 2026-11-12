from .common import integer
FAULTS=['none','before_write','after_write','duplicate_delivery','stale_snapshot']
def run(data):
 stock=integer(data['stock'],1,1000000);quantity=integer(data['quantity'],1,stock);faults=data.get('faults',FAULTS)
 if not isinstance(faults,list)or len(faults)>100 or any(f not in FAULTS for f in faults):raise ValueError('faults')
 output=[]
 for fault in faults:
  for strategy in ['blind_retry','reconcile']:
   available=stock;effects=[];version=1;observed=1;attempts=0;status='ready'
   if fault=='stale_snapshot':version=2;available-=1
   deliveries=2 if fault in ['after_write','duplicate_delivery','before_write']else 1
   for attempt in range(deliveries):
    attempts+=1
    if strategy=='reconcile'and effects:status='confirmed_existing';break
    if strategy=='reconcile'and version!=observed:status='stale_blocked';break
    if fault=='before_write'and attempt==0:continue
    if available<quantity:status='insufficient';break
    available-=quantity;effects.append('reservation');status='written'
    if fault=='after_write'and attempt==0:status='uncertain';continue
    if fault not in ['duplicate_delivery']:break
   output.append({'fault':fault,'strategy':strategy,'effects':len(effects),'available':available,'attempts':attempts,'status':status,'at_most_one_effect':len(effects)<=1,'stale_action_blocked':status=='stale_blocked'})
 return {'scenarios':output,'actual_hermes_skill_executed':False,'unseen_fault_robustness_proven':False,'repair_generated':False}
