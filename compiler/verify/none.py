"""
This is a DRC/LVS/PEX interface file the case with no DRC/LVS tools.

"""
import debug

# Only print the warning once.
drc_warned = False
lvs_warned = False
pex_warned = False

def run_drc(cell_name, gds_name, extract=False):
    global drc_warned
    if not drc_warned:
        debug.warning("DRC unable to run.")
        drc_warned=True
    # Since we warned, return a failing test.        
    return 1
    
def run_lvs(cell_name, gds_name, sp_name, final_verification=False):
    global lvs_warned
    if not lvs_warned:
        debug.warning("LVS unable to run.")
        lvs_warned=True
    # Since we warned, return a failing test.
    return 1

def run_pex(name, gds_name, sp_name, output=None):
    global pex_warned    
    if not pex_warned:
        debug.warning("PEX unable to run.")
        pex_warned=True
    # Since we warned, return a failing test.        
    return 1

def print_drc_stats():
    pass
def print_lvs_stats():
    pass
def print_pex_stats():
    pass
