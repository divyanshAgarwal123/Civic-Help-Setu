import datetime,json,os,pathlib,subprocess,sys
out=pathlib.Path(__file__).parent;root=out.parents[1];which=sys.argv[1];cwd=root/('civic1263-parent'if which=='parent'else'civic1263');env=dict(os.environ)
for key in ['GOOGLE_APPLICATION_CREDENTIALS','FIREBASE_SERVICE_ACCOUNT','FIREBASE_SERVICE_ACCOUNT_JSON']:env.pop(key,None)
results={'target':which,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=cwd,text=True).strip(),'checks':[]};prefix=['npm','exec','--yes','--package=node@22.23.5','--','npm','run']
checks=[('lint',[]),('test',['--','--maxWorkers=2','--reporter=json','--outputFile='+str(out/('civic-'+which+'-tests.json'))]),('build',[]),('lint:security',[])]
for name,extra in checks:
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();log=out/('civic-'+which+'-'+name.replace(':','-')+'.log')
 with log.open('w')as f:
  p=subprocess.run(prefix+[name]+extra,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 results['checks'].append({'name':name,'exitCode':p.returncode,'startedAt':started,'finishedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':log.name});(out/('civic-'+which+'-checks.json')).write_text(json.dumps(results,indent=2)+'\n');print(which,name,p.returncode,flush=True)
