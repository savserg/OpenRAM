#!/usr/bin/env python3
"""
Run a regression test on various srams
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class timing_setup_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.spice_name="ngspice"
        OPTS.analytical_delay = False

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import setup_hold
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)
        
        import sram
        import tech
        slews = [tech.spice["rise_time"]*2]
        
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        sh = setup_hold(corner)
        data = sh.analyze(slews,slews)
        #print data
        if OPTS.tech_name == "freepdk45":
            golden_data = {'hold_times_HL': [-0.01586914],
                           'hold_times_LH': [-0.01586914],
                           'setup_times_HL': [0.02685547],
                           'setup_times_LH': [0.03295898]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'hold_times_HL': [-0.08911132999999999],
                            'hold_times_LH': [-0.0769043],
                            'setup_times_HL': [0.1184082],
                            'setup_times_LH': [0.1672363]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))

        self.assertTrue(self.check_golden_data(data,golden_data,0.25))
        
        reload(characterizer)
        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
