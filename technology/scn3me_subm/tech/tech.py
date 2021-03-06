import os

"""
File containing the process technology parameters for SCMOS 3me, subm, 180nm.
"""

info={}
info["name"]="scn3me_subm"
info["body_tie_down"] = 0
info["has_pwell"] = True
info["has_nwell"] = True

#GDS file info
GDS={}
# gds units
GDS["unit"]=(0.001,1e-6)  
# default label zoom
GDS["zoom"] = 0.5


###################################################
##GDS Layer Map
###################################################

# create the GDS layer map
layer={} 
layer["vtg"]            = -1 
layer["vth"]            = -1 
layer["contact"]        = 47 
layer["pwell"]          = 41 
layer["nwell"]          = 42 
layer["active"]         = 43 
layer["pimplant"]       = 44
layer["nimplant"]       = 45
layer["poly"]           = 46 
layer["active_contact"] = 48
layer["metal1"]         = 49 
layer["via1"]           = 50 
layer["metal2"]         = 51 
layer["via2"]           = 61 
layer["metal3"]         = 62 
layer["text"]           = 63 
layer["boundary"]       = 63 
layer["blockage"]       = 83

###################################################
##END GDS Layer Map
###################################################

###################################################
##DRC/LVS Rules Setup
###################################################
_lambda_ = 0.3

#technology parameter
parameter={}
parameter["min_tx_size"] = 4*_lambda_
parameter["beta"] = 2 

drclvs_home=os.environ.get("DRCLVS_HOME")

drc={}
#grid size is 1/2 a lambda
drc["grid"]=0.5*_lambda_
#DRC/LVS test set_up
drc["drc_rules"]=drclvs_home+"/calibreDRC_scn3me_subm.rul"
drc["lvs_rules"]=drclvs_home+"/calibreLVS_scn3me_subm.rul"
drc["layer_map"]=os.environ.get("OPENRAM_TECH")+"/scn3me_subm/layers.map"

        	      					
# minwidth_tx with contact (no dog bone transistors)
drc["minwidth_tx"] = 4*_lambda_
drc["minlength_channel"] = 2*_lambda_

# 1.3 Minimum spacing between wells of same type (if both are drawn) 
drc["well_to_well"] = 6*_lambda_
# 1.4 Minimum spacing between wells of different type (if both are drawn) 
drc["pwell_to_nwell"] = 0
# 1.1 Minimum width 
drc["minwidth_well"] = 12*_lambda_

# 3.1 Minimum width 
drc["minwidth_poly"] = 2*_lambda_
# 3.2 Minimum spacing over active
drc["poly_to_poly"] = 3*_lambda_
# 3.3 Minimum gate extension of active 
drc["poly_extend_active"] = 2*_lambda_
# 5.5.b Minimum spacing between poly contact and other poly (alternative rules)
drc["poly_to_polycontact"] = 4*_lambda_
# ??
drc["active_enclosure_gate"] = 0.0
# 3.5 Minimum field poly to active 
drc["poly_to_active"] = _lambda_
# 3.2.a Minimum spacing over field poly
drc["poly_to_field_poly"] = 3*_lambda_
# Not a rule
drc["minarea_poly"] = 0.0

# ??
drc["active_to_body_active"] = 4*_lambda_  # Fix me
# 2.1 Minimum width 
drc["minwidth_active"] = 3*_lambda_
# 2.2 Minimum spacing
drc["active_to_active"] = 3*_lambda_
# 2.3 Source/drain active to well edge 
drc["well_enclosure_active"] = 6*_lambda_
# Reserved for asymmetric enclosures
drc["well_extend_active"] = 6*_lambda_
# Not a rule
drc["minarea_active"] = 0.0

# 4.1 Minimum select spacing to channel of transistor to ensure adequate source/drain width 
drc["implant_to_channel"] = 3*_lambda_
# 4.2 Minimum select overlap of active
drc["implant_enclosure_active"] = 2*_lambda_
# 4.3 Minimum select overlap of contact  
drc["implant_enclosure_contact"] = _lambda_
# Not a rule
drc["implant_to_contact"] = 0
# Not a rule
drc["implant_to_implant"] = 0
# Not a rule
drc["minwidth_implant"] = 0

# 6.1 Exact contact size
drc["minwidth_contact"] = 2*_lambda_
# 5.3 Minimum contact spacing
drc["contact_to_contact"] = 3*_lambda_               
# 6.2.b Minimum active overlap 
drc["active_enclosure_contact"] = _lambda_
# Reserved for asymmetric enclosure
drc["active_extend_contact"] = _lambda_
# 5.2.b Minimum poly overlap 
drc["poly_enclosure_contact"] = _lambda_
# Reserved for asymmetric enclosures
drc["poly_extend_contact"] = _lambda_
# Reserved for other technologies
drc["contact_to_gate"] = 2*_lambda_
# 5.4 Minimum spacing to gate of transistor
drc["contact_to_poly"] = 2*_lambda_
        
# 7.1 Minimum width 
drc["minwidth_metal1"] = 3*_lambda_
# 7.2 Minimum spacing 
drc["metal1_to_metal1"] = 3*_lambda_
# 7.3 Minimum overlap of any contact 
drc["metal1_enclosure_contact"] = _lambda_
# Reserved for asymmetric enclosure
drc["metal1_extend_contact"] = _lambda_
# 8.3 Minimum overlap by metal1 
drc["metal1_enclosure_via1"] = _lambda_           
# Reserve for asymmetric enclosures
drc["metal1_extend_via1"] = _lambda_
# Not a rule
drc["minarea_metal1"] = 0

# 8.1 Exact size 
drc["minwidth_via1"] = 2*_lambda_
# 8.2 Minimum via1 spacing 
drc["via1_to_via1"] = 3*_lambda_

# 9.1 Minimum width
drc["minwidth_metal2"] = 3*_lambda_
# 9.2 Minimum spacing 
drc["metal2_to_metal2"] = 3*_lambda_
# 9.3 Minimum overlap of via1 
drc["metal2_extend_via1"] = _lambda_
# Reserved for asymmetric enclosures
drc["metal2_enclosure_via1"] = _lambda_
# 14.3 Minimum overlap by metal2
drc["metal2_extend_via2"] = _lambda_
# Reserved for asymmetric enclosures
drc["metal2_enclosure_via2"] = _lambda_
# Not a rule
drc["minarea_metal2"] = 0

# 14.1 Exact size
drc["minwidth_via2"] = 2*_lambda_
# 14.2 Minimum spacing
drc["via2_to_via2"] = 3*_lambda_

# 15.1 Minimum width
drc["minwidth_metal3"] = 5*_lambda_
# 15.2 Minimum spacing to metal3
drc["metal3_to_metal3"] = 3*_lambda_
# 15.3 Minimum overlap of via 2
drc["metal3_extend_via2"] = 2*_lambda_
# Reserved for asymmetric enclosures
drc["metal3_enclosure_via2"] = 2*_lambda_
# Not a rule
drc["minarea_metal3"] = 0

###################################################
##END DRC/LVS Rules
###################################################

###################################################
##Spice Simulation Parameters
###################################################

# spice model info
spice={}
spice["nmos"]="n"
spice["pmos"]="p"
# This is a map of corners to model files
SPICE_MODEL_DIR=os.environ.get("SPICE_MODEL_DIR")
# FIXME: Uncomment when we have the new spice models
#spice["fet_models"] = { "TT" : [SPICE_MODEL_DIR+"/nom/pmos.sp",SPICE_MODEL_DIR+"/nom/nmos.sp"] }
spice["fet_models"] = { "TT" : [SPICE_MODEL_DIR+"/nom/pmos.sp",SPICE_MODEL_DIR+"/nom/nmos.sp"],
                        "FF" : [SPICE_MODEL_DIR+"/ff/pmos.sp",SPICE_MODEL_DIR+"/ff/nmos.sp"],
                        "FS" : [SPICE_MODEL_DIR+"/ff/pmos.sp",SPICE_MODEL_DIR+"/ss/nmos.sp"],
                        "SF" : [SPICE_MODEL_DIR+"/ss/pmos.sp",SPICE_MODEL_DIR+"/ff/nmos.sp"],                        
                        "SS" : [SPICE_MODEL_DIR+"/ss/pmos.sp",SPICE_MODEL_DIR+"/ss/nmos.sp"] }
                        

#spice stimulus related variables
spice["feasible_period"] = 5         # estimated feasible period in ns
spice["supply_voltages"] = [4.5, 5.0, 5.5]  # Supply voltage corners in [Volts]
spice["nom_supply_voltage"] = 5.0    # Nominal supply voltage in [Volts]
spice["rise_time"] = 0.05            # rise time in [Nano-seconds]
spice["fall_time"] = 0.05            # fall time in [Nano-seconds]
spice["temperatures"] = [0, 25, 100]  # Temperature corners (celcius)
spice["nom_temperature"] = 25        # Nominal temperature (celcius)

#sram signal names
#FIXME: We don't use these everywhere...
spice["vdd_name"] = "vdd"
spice["gnd_name"] = "gnd"
spice["control_signals"] = ["CSB", "WEB"]
spice["data_name"] = "DATA"
spice["addr_name"] = "ADDR"
spice["minwidth_tx"] = drc["minwidth_tx"]
spice["channel"] = drc["minlength_channel"]
spice["clk"] = "clk"

# analytical delay parameters
# FIXME: These need to be updated for SCMOS, they are copied from FreePDK45.
spice["wire_unit_r"] = 0.075    # Unit wire resistance in ohms/square
spice["wire_unit_c"] = 0.64     # Unit wire capacitance ff/um^2
spice["min_tx_r"] = 9250.0      # Minimum transistor on resistance in ohms
spice["min_tx_drain_c"] = 0.7   # Minimum transistor drain capacitance in ff
spice["min_tx_gate_c"] = 0.1    # Minimum transistor gate capacitance in ff
spice["msflop_setup"] = 9        # DFF setup time in ps
spice["msflop_hold"] = 1         # DFF hold time in ps
spice["msflop_delay"] = 20.5     # DFF Clk-to-q delay in ps
spice["msflop_slew"] = 13.1      # DFF output slew in ps w/ no load
spice["msflop_in_cap"] = 9.8242  # Input capacitance of ms_flop (Din) [Femto-farad]
spice["dff_setup"] = 9        # DFF setup time in ps
spice["dff_hold"] = 1         # DFF hold time in ps
spice["dff_delay"] = 20.5     # DFF Clk-to-q delay in ps
spice["dff_slew"] = 13.1      # DFF output slew in ps w/ no load
spice["dff_in_cap"] = 9.8242  # Input capacitance of ms_flop (Din) [Femto-farad]

# analytical power parameters, many values are temporary
spice["bitcell_leakage"] = 1     # Leakage power of a single bitcell in nW
spice["inv_leakage"] = 1         # Leakage power of inverter in nW
spice["nand2_leakage"] = 1       # Leakage power of 2-input nand in nW
spice["nand3_leakage"] = 1       # Leakage power of 3-input nand in nW
spice["nor2_leakage"] = 1        # Leakage power of 2-input nor in nW
spice["msflop_leakage"] = 1      # Leakage power of flop in nW
spice["flop_para_cap"] = 2       # Parasitic Output capacitance in fF

spice["default_event_rate"] = 100         # Default event activity of every gate. MHz
spice["flop_transition_prob"] = .5        # Transition probability of inverter.
spice["inv_transition_prob"] = .5         # Transition probability of inverter.
spice["nand2_transition_prob"] = .1875    # Transition probability of 2-input nand.
spice["nand3_transition_prob"] = .1094    # Transition probability of 3-input nand.
spice["nor2_transition_prob"] = .1875     # Transition probability of 2-input nor.
###################################################
##END Spice Simulation Parameters
###################################################
