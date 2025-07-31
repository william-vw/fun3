import os, subprocess, re, multiprocess
from datetime import datetime
import pandas as pd

def run(cmd):    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = [ b.decode('UTF-8') for b in process.communicate() ]
    
    if error.strip() != "":
        print(error)

    print(out)

def __do_runNSave(cmd, out_path, ret_times, get_times_eye=True):
     # result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = [ b.decode('UTF-8') for b in process.communicate() ]
    out = out.rstrip()
    # print("out:", out)
    # print("error:", error)
        
    with open(out_path, 'w') as fh:
        fh.write(out)
    
    if "** ERROR **" in error:
        print("ERROR:", error)
    
    elif get_times_eye:
        netw_time = int(re.search("networking \d+ \[msec cputime\] (\d+) \[msec walltime\]", error).group(1))
        reas_time = int(re.search("reasoning \d+ \[msec cputime\] (\d+) \[msec walltime\]", error).group(1))
        ret_times.append(netw_time); ret_times.append(reas_time)
        # return netw_time, reas_time

def runNSave_timed(cmd, out_path, max_time, get_times_eye=True):
    mngr = multiprocess.Manager()
    ret_times = mngr.list()
    
    p = multiprocess.Process(target=__do_runNSave, args=(cmd, out_path, ret_times, get_times_eye))
    p.start()
    
    p.join(max_time)
    if p.is_alive():
        p.kill()
        return (-1, -1)
    else:
        return ret_times
        
def runNSave(cmd, out_path, get_times_eye=True):
   ret_times = []
   __do_runNSave(cmd, out_path, ret_times, get_times_eye)
   
   return ret_times

def get_times_file(path, system):
    times_file = os.path.join(path, f"times_{system}.csv")
    exists = os.path.exists(times_file)
    times_fh = open(times_file, 'a')
    if not exists:
        header = "run,query,data,netw_time,reas_time"
        if system == "fun3":
            header += ",gen_time,exec_time"
        header += "\n"
        times_fh.write(header)
        
    return times_fh

def record_eye(times_file, run, query, data, netw_time, reas_time):
    times_file.write(f"{run},{query},{data},{netw_time},{reas_time}\n")
    
def record_fun3(times_file, run, query, data, netw_time, reas_time, gen_time, exec_time):
    times_file.write(f"{run},{query},{data},{netw_time},{reas_time},{gen_time},{exec_time}\n")
    
    
def __load_n3_time(path):
    df_n3 = pd.read_csv(path)

    # drop all times for query with at least 1 failed phase
    df_n3['id'] = df_n3.apply(lambda x: f"{x['query']},{x['type']}", axis=1)
    df_n3_failed = df_n3[df_n3['reas_time'] == -1]['id']
    df_n3_filt = df_n3[~df_n3['id'].isin(df_n3_failed)]

    return df_n3_filt


def load_n3_times(path, pt=None, q=None):
    df_n3 = pd.read_csv(path)
    if pt is not None:
        df_n3 = df_n3[df_n3['data'].str.contains(pt)]
    if q is not None:
        df_n3 = df_n3[df_n3['query'].str.contains(q)]
    
    df_n3['total_time'] = df_n3['netw_time'] + df_n3['reas_time']

    return df_n3

def load_n3_agg(path, pt=None,q=None):
    df_n3 = load_n3_times(path, pt=pt, q=q)
    cols = ['netw_time', 'reas_time', 'total_time']
    if "fun3" in path:
        cols.append("gen_time")
    df_n3_agg = df_n3.groupby(['query', 'data'])[cols].mean().reset_index()

    df_n3_agg['query_id'] = df_n3_agg['query'].str.slice(len("rules_red"), -len(".n3")).astype(int)
    df_n3_agg['data_id'] = df_n3_agg['data'].str.slice(
        len("gen"), -len("_ptx.n3")).astype(int)
    df_n3_agg = df_n3_agg.sort_values(by=['query_id', 'data_id'])

    return df_n3_agg