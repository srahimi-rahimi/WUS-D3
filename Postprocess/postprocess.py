import sys
sys.path.insert(0,'/glade/work/leihuang/postprocess/')
import postprocess_wus_lib as plib
import argparse


def main(model, file_type, year, domain, varname, in_dir, out_dir, leap_flag, bc_flag):
    noleap = False
    if leap_flag == 0: 
        noleap = True
    nobc = False
    if bc_flag == 0: 
        nobc = True
    plib.process(model, file_type, year, domain, varname, in_dir, out_dir, noleap, nobc)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=str)
    parser.add_argument("file_type", type=str)
    parser.add_argument("year", type=int)
    parser.add_argument("domain", type=str)
    parser.add_argument("varname", type=str)
    parser.add_argument("in_dir", type=str)
    parser.add_argument("out_dir", type=str)
    parser.add_argument("leap_flag", type=int)
    parser.add_argument("bc_flag", type=int)
    parsed = parser.parse_args()
    main(parsed.model,parsed.file_type,parsed.year,parsed.domain,parsed.varname,parsed.in_dir,parsed.out_dir,parsed.leap_flag,parsed.bc_flag)    