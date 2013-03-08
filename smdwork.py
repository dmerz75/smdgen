import shutil,os,itertools,re
#_______DICTIONARY_____________________________________________________________
zdictn ={'da':13.0,'rda':33.0,'le':33.0,
         'ee':4.0,'empty':5.3,'empty':5.7}
configf=['job.sh','go.py','smd.namd','smd.tcl','expavg.py']
confign={'1':{'gpu':'nodes=1:ppn=1:gpus=1:TESLA','cpu':'nodes=1:ppn=1'},
         '2':{'gpu':'nodes=1:ppn=2:gpus=1:TESLA','cpu':'nodes=1:ppn=2'},
         '3':{'gpu':'nodes=1:ppn=3:gpus=1:TESLA','cpu':'nodes=1:ppn=3'},
         '4':{'gpu':'nodes=1:ppn=4:gpus=1:TESLA','cpu':'nodes=1:ppn=4'},
         '5':{'gpu':'nodes=1:ppn=5:gpus=1:TESLA','cpu':'nodes=1:ppn=5'},
         '6':{'gpu':'nodes=1:ppn=6:gpus=1:TESLA','cpu':'nodes=1:ppn=6'},
         '7':{'gpu':'nodes=1:ppn=7:gpus=1:TESLA','cpu':'nodes=1:ppn=7'},
         '8':{'gpu':'nodes=1:ppn=8:gpus=1:TESLA','cpu':'nodes=1:ppn=8'},
       '16':{'gpu':'nodes=1:ppn=16:gpus=1:TESLA','cpu':'nodes=1:ppn=16'}}
configw={'swt':'walltime=72:00:00','mwt':'walltime=368:00:00',
         'lwt':'walltime=720:00:00'}
configq={'short':'tg_short','workq':'tg_workq','standby':'standby',
         'standby-8':'standby-8'}
confige={'1':'v1000','2':'v100','3':'v10','4':'v1','5':'vp1'}
strdir ={'01.vac':'00.struc-equil.v','02.imp':'00.struc-equil.i',
         '03.exp':'00.struc-equil.e'}
dictpf ={'1':1,'2':1,'3':50,'4':100,'5':500}
setup  ={'1':{'vel':0.002,'steps':1000,'dcd':100,'howmany':50,'freq':50},
      '2':{'vel':0.0002,'steps':1000,'dcd':1000,'howmany':50,'freq':50},
      '3':{'vel':0.00002,'steps':1000,'dcd':10000,'howmany':5,'freq':50},
      '4':{'vel':0.000002,'steps':1000,'dcd':100000,'howmany':1,'freq':50},
      '5':{'vel':0.0000002,'steps':1000,'dcd':1000000,'howmany':1,'freq':50}}
#__________global_____use______________________________________________________
def cp_file(f_dir,f,d_dir,d):
    shutil.copy(os.path.join(f_dir,f),os.path.join(d_dir,d))
def cp_tree(f_dir,f,d_dir,d):
    shutil.copytree(os.path.join(f_dir,f),os.path.join(d_dir,d))
def reg_ex(script,subout,subin):
    o=open(script,'r+')
    text=o.read()
    text=re.sub(subout,subin,text)
    o.close()
    o=open(script,'w+')
    o.write(text)
    o.close()
#______________________________________________________________________________
class make_JobDirSmd:
    def __init__(self,ngn,mol,zc,workdir,jobdir):
        self.ngn  = ngn
        self.mol  = mol
        self.zc   = zc
        self.workdir = workdir
        self.jobdir = jobdir
        self.jdir = os.path.join(self.workdir,self.jobdir)
    def makeJobDir(self):
        if not os.path.exists(self.jdir):os.makedirs(self.jdir)
        texdir=os.path.join(self.jobdir,'tex_%s' % self.jdir.split('/')[-1])
        if not os.path.exists(texdir): os.makedirs(texdir)
        cp_file(self.workdir,'gen.py',self.jobdir,'.gen_%s.py' % \
                  self.jdir.split('/')[-1])
        cp_file(self.workdir,'04.scripts/run.py',self.jobdir,'run.py')
        cp_file(self.workdir,'04.scripts/exprun.py',self.jobdir,'exprun.py')
        cp_file(self.workdir,'04.scripts/tm.tex',texdir,'tm.tex')
        cp_file(self.workdir,'04.scripts/pdflatex.sh',texdir,'pdflatex.sh')
        cp_file(self.workdir,'04.scripts/del.py',self.jobdir,'del.py')
        if self.ngn=='namd':
            cp_tree(self.workdir,'04.toppar',self.jobdir,'toppar')
        if self.ngn=='gro':
            cp_tree(self.workdir,'04.topol',self.jobdir,'topol')
        cp_tree(self.workdir,'04.scripts',self.jobdir,'04.scripts')
        return texdir
    def reg_exp(self,subdir):
        for root, dirnames, filenames in os.walk(subdir):
            for f in filenames:
                script=os.path.join(root,f)
                if f=='tm.tex':
                    plotname=self.mol+self.ngn+'vacv1000'+str(self.zc)
                    reg_ex(script,'xxplotnamexx',plotname)
class Struc_Dirs:
    def __init__(self,ngn,mol,env,workdir,jobdir):
        self.ngn  = ngn
        self.mol  = mol
        self.env  = env
        self.workdir = workdir
        self.jobdir = jobdir
        self.jdir = os.path.join(self.workdir,self.jobdir)
    def makeStrucDir(self):
        cp_tree(os.path.join(self.workdir,'01.struc-equil.'+self.ngn, \
                self.mol,self.env),'',self.jdir,strdir[self.env])
class Smd_Method:
    def __init__(self,ngn,mol,env,vel,ts,zc,lD,sf,workdir,jobdir,gate,cn,comp,\
                wallt,queue,direct):
        self.ngn  = ngn
        self.mol  = mol
        self.env  = env
        self.e    = self.env.split('.')[1]
        self.vel  = str(int(vel))
        self.ts   = ts
        self.zc   = zc
        self.lD   = lD
        self.sf   = sf
        self.workdir = workdir
        self.jobdir = jobdir
        self.gate = gate
        self.cn   = cn
        self.comp = comp
        self.wt   = wallt
        self.q    = queue
        self.jdir = os.path.join(self.workdir,self.jobdir)
        self.edir = os.path.join(self.jdir,self.env)
        vdirname = str(self.vel).zfill(2)
        self.vdir = os.path.join(self.edir,vdirname)
        # self.vel 2  / self.ts 2 fs/ts  / self.zc 13 / self.direct 1
        # ALSO located in STEERING section
        self.v_ats  = setup[self.vel]['vel']*direct
        self.tsteps = 1000*(10**int(vel))*sf
        self.distA  = self.v_ats*self.tsteps
        self.spos   = zc
        self.epos   = self.spos+self.distA
        self.t_ps   = (self.tsteps*self.ts)/1000
        self.t_ns   = (self.tsteps*self.ts)/(10**6)
        self.v_aps  = self.distA/self.t_ps
        self.v_ans  = self.distA/self.t_ns
        self.dt     = setup[self.vel]['freq']*ts/1000
        '''
        print 'v_ats',self.v_ats,type(self.v_ats)
        print 'tsteps',self.tsteps,type(self.tsteps)
        print 'distA',self.distA,type(self.distA)
        print 'spos',self.spos,type(self.spos)
        print 'epos',self.epos,type(self.epos)
        print 't_ps',self.t_ps,type(self.t_ps)
        print 't_ns',self.t_ns,type(self.t_ns)
        print 'v_aps',self.v_aps,type(self.v_aps)
        print 'v_ans',self.v_ans,type(self.v_ans)
        print 'dt',self.dt,type(self.dt)
        '''
    def makeEnvDir(self):
        if not os.path.exists(self.edir):os.makedirs(self.edir)
    def makeSubDirCopies(self,x=3):
        for i in range(x):
            sdirname = str(self.vel).zfill(2)+'.'+str(i).zfill(2)
            cp_tree(self.vdir,'',self.edir,sdirname)
        shutil.rmtree(self.vdir)
#_____________________________________________________________________________
    def reg_exp(self,subdir):
        def call_smd(script):
            reg_ex(script,'xxnumxx',str(self.vel).zfill(2))
            reg_ex(script,'xxstepsxx',str(int(self.tsteps)))
            reg_ex(script,'xxdcdxx',str(setup[self.vel]['dcd']))
            if self.ngn=='amb':
                reg_ex(script,'xxtsxx',str(self.ts/1000))
            elif self.ngn=='namd':
                reg_ex(script,'xxtsxx',str(self.ts))
            reg_ex(script,'xxlDxx',self.lD)
            reg_ex(script,'xxfreqxx',str(setup[self.vel]['freq']))
        def call_expavg(script):
            reg_ex(script,'xxtefdirxx','0'+self.vel+'.*/*-tef.dat*')
            reg_ex(script,'xxnumxx',str(self.vel).zfill(2))
            reg_ex(script,'xxvvxx',self.vel)
            reg_ex(script,'xxvelapsxx',str(self.v_aps))
            reg_ex(script,'xxvelansxx',str(self.v_ans))
            reg_ex(script,'xxpfxx',str(dictpf[self.vel]))
            plotname=self.mol+self.ngn+self.e+str(confige[self.vel])+str(self.zc)
            reg_ex(script,'xxplotnamexx',plotname)
            reg_ex(script,'xxstartconstraintxx',str(self.spos))
            reg_ex(script,'xxendconstraintxx',str(self.epos))
            reg_ex(script,'xxmoleculexx',self.mol)
            reg_ex(script,'xxdtxx',str(self.dt))
            reg_ex(script,'xxenvironxx',self.e)
        for root, dirnames, filenames in os.walk(subdir):
            for f in filenames:
                if len(f.split('-'))==1:
                    idn=f
                elif len(f.split('-'))==2:
                    idn=f.split('-')[1]
                script=os.path.join(root,f)
                if idn=='job.sh':
                    bashjobname=self.mol+'.'+self.ngn+'.'+str(self.v_ans)+self.e
                    reg_ex(script,'xxjobnamexx',bashjobname)
                    reg_ex(script,'xxqueuexx',configq[self.q])
                    reg_ex(script,'xxnodesxx',confign[self.cn][self.comp])
                    reg_ex(script,'xxwalltimexx',configw[self.wt])
                elif idn=='go.py':
                    reg_ex(script,'xxnumxx',str(self.vel).zfill(2))
                    reg_ex(script,'xxhowmanyxx',str(setup[self.vel]['howmany']))
                    reg_ex(script,'xxnodecountxx',self.cn)
                    reg_ex(script,'xxstartconstraintxx',str(self.zc))
                    reg_ex(script,'xxendconstraintxx',str(self.epos))
                    reg_ex(script,'xxstrucequilxx',str(strdir[self.env]))
                elif idn=='smd.namd':
                    call_smd(script)
                elif idn=='smd.in':
                    call_smd(script)
                elif idn=='smd.tcl':
                    reg_ex(script,'xxnumxx',str(self.vel).zfill(2))
                    reg_ex(script,'xxvelocityxx',str(self.v_ats))
                    reg_ex(script,'xxzcoordxx',str(self.zc))
                    reg_ex(script,'xxtsxx',self.ts)
                    reg_ex(script,'xxfreqxx',str(setup[self.vel]['freq']))
                elif idn=='dist.RST':
                    call_expavg(script)
                elif idn=='expavg.py':
                    call_expavg(script)
                elif idn=='tm.tex':
                    call_expavg(script)
                elif idn=='dualplot.py':
                    call_expavg(script)
                elif idn=='npy.py':
                    call_expavg(script)
                elif idn=='hb.py':
                    reg_ex(script,'xxenvironxx',strdir[self.env])
                elif idn=='allhb.py':
                    call_expavg(script)
                elif idn=='allwp.py':
                    call_expavg(script)
                elif idn=='ihbond.py':
                    call_expavg(script)
#_____________________________________________________________________________
    def makeSubDir(self):
        mdir='00.maindir.'+self.ngn
        pre=os.path.join(self.workdir,mdir)
        os.makedirs(self.vdir)
        if self.ngn=='namd':
            cp_file(os.path.join(pre,self.mol,self.env),'smd.namd',self.vdir,\
                    'smd.namd')
            cp_file(os.path.join(pre,'VDIR'),'job-'+self.gate+'.sh', \
                    self.vdir,'job.sh')
            cp_file(os.path.join(pre,'VDIR'),'go-'+self.gate+'.py',self.vdir, \
                    'go.py')
        if self.ngn=='amb':
            cp_file(os.path.join(pre,self.mol,self.env),'smd.in',self.vdir,\
                    'smd.in')
            cp_file(os.path.join(pre,'VDIR'),'job-'+self.gate+'.sh', \
                    self.vdir,'job.sh')
            cp_file(os.path.join(pre,'VDIR'),'go-'+self.gate+'.py',self.vdir, \
                    'go.py')
        if self.ngn=='gro':
            cp_file(os.path.join(pre,self.mol,self.env),'smd.mdp',self.vdir,\
                    'smd.mdp')
            cp_file(os.path.join(pre,self.mol),'groups.txt',self.vdir, \
                    'groups.txt')
            cp_file(os.path.join(pre,'VDIR'),'job-'+self.gate+'.sh', \
                    self.vdir,'job.sh')
            cp_file(os.path.join(pre,'VDIR'),'go-'+self.gate+'.py',self.vdir, \
                    'go.py')
        return self.vdir
    def makeEvalDir(self):
        source=os.path.join(self.workdir,'00.maindir.'+self.ngn,'EVAL')
        for root, dirnames, filenames in os.walk(source):
            for f in filenames:
                fi=os.path.join(root,f)
                d=str(self.vel).zfill(2)+'-'+f
                dest=os.path.join(self.edir,str((self.vel).zfill(2))+'.eval')
                di=os.path.join(dest,d)
                if not os.path.exists(dest):os.makedirs(dest)
                shutil.copy(fi,di)
        return dest
#_____Steering_Class__________________________________________________________
class Smd_Steering:
    def __init__(self,ngn,mol,env,vel,ts,zc,lD,sf,workdir,jobdir,gate,cn,comp,\
                wallt,queue,direct):
        self.ngn  = ngn
        self.mol  = mol
        self.env  = env
        self.e    = self.env.split('.')[1]
        self.vel  = str(int(vel))
        self.ts   = ts
        self.zc   = zc
        self.lD   = lD
        self.sf   = sf
        self.workdir = workdir
        self.jobdir = jobdir
        self.gate = gate
        self.cn   = cn
        self.comp = comp
        self.wt   = wallt
        self.q    = queue
        self.jdir = os.path.join(self.workdir,self.jobdir)
        self.edir = os.path.join(self.jdir,self.env)
        vdirname = str(self.vel).zfill(2)
        self.vdir = os.path.join(self.edir,vdirname)
        # STEERING
        self.v_ats  = setup[self.vel]['vel']*direct
        self.tsteps = 1000*(10**int(vel))*sf
        self.distA  = self.v_ats*self.tsteps
        self.spos   = zc
        self.epos   = self.spos+self.distA
        self.t_ps   = (self.tsteps*self.ts)/1000
        self.t_ns   = (self.tsteps*self.ts)/(10**6)
        self.v_aps  = self.distA/self.t_ps
        self.v_ans  = self.distA/self.t_ns
        self.dt     = setup[self.vel]['freq']*ts/1000
    def reg_exp(self,subdir):
        # end function_____________________________________
        for root, dirnames, filenames in os.walk(subdir):
            for f in filenames:
                if len(f.split('-'))==1:
                    idn=f
                elif len(f.split('-'))==2:
                    idn=f.split('-')[1]
                script=os.path.join(root,f)
                if idn=='smd.tcl':
                    reg_ex(script,'xxvelocityxx',str(self.v_ats))
                    reg_ex(script,'xxzcoordxx',str(self.spos))
                    reg_ex(script,'xxtsxx',str(self.ts))
                    reg_ex(script,'xxfreqxx',str(setup[self.vel]['freq']))
                elif idn=='dist.RST':
                    reg_ex(script,'xxtefdirxx','0'+self.vel+'.*/*-tef.dat*')
                    reg_ex(script,'xxnumxx','0'+self.vel)
                    reg_ex(script,'xxvvxx',self.vel)
                    reg_ex(script,'xxvelapsxx',str(self.v_aps))
                    reg_ex(script,'xxvelansxx',str(self.v_ans))
                    reg_ex(script,'xxpfxx',str(dictpf[self.vel]))
                    plotname=self.mol+self.ngn+self.e+ \
                          str(confige[self.vel])+str(self.spos)
                    reg_ex(script,'xxplotnamexx',plotname)
                    reg_ex(script,'xxstartconstraintxx',str(self.spos))
                    reg_ex(script,'xxendconstraintxx',str(self.epos))
                    reg_ex(script,'xxmoleculexx',self.mol)
                    reg_ex(script,'xxenvironxx',self.e)
                    reg_ex(script,'xxdtxx',str(self.dt))
                elif idn=='hb.py':
                    reg_ex(script,'xxenvironxx',strdir[self.env])
    def place_steering_control(self):
        cp_file(os.path.join(self.workdir,'00.maindir.'+self.ngn,'VDIR'), \
                'hb.py',self.edir,'0'+self.vel+'-hb.py')
        if self.ngn=='namd':
            cp_file(os.path.join(self.workdir,'00.maindir.'+self.ngn,self.mol),\
                    'smd.tcl',self.edir,str(self.vel).zfill(2)+'-smd.tcl')
        elif self.ngn=='amb':
            cp_file(os.path.join(self.workdir,'00.maindir.'+self.ngn,self.mol),\
                    'dist.RST',self.edir,str(self.vel).zfill(2)+'-dist.RST')
        return self.edir
