import debug
import design
import math
from tech import drc
import contact
from pinv import pinv
from vector import vector
from globals import OPTS
from pnand2 import pnand2
from pnand3 import pnand3


class hierarchical_predecode(design.design):
    """
    Pre 2x4 and 3x8 decoder shared code.
    """
    def __init__(self, input_number):
        self.number_of_inputs = input_number
        self.number_of_outputs = int(math.pow(2, self.number_of_inputs))
        design.design.__init__(self, name="pre{0}x{1}".format(self.number_of_inputs,self.number_of_outputs))

        from importlib import reload
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
    
    def add_pins(self):
        for k in range(self.number_of_inputs):
            self.add_pin("in[{0}]".format(k))
        for i in range(self.number_of_outputs):
            self.add_pin("out[{0}]".format(i))
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_modules(self):
        """ Create the INV and NAND gate """
        
        self.inv = pinv()
        self.add_mod(self.inv)
        
        self.add_nand(self.number_of_inputs)
        self.add_mod(self.nand)

    def add_nand(self,inputs):
        """ Create the NAND for the predecode input stage """
        if inputs==2:
            self.nand = pnand2()
        elif inputs==3:
            self.nand = pnand3()
        else:
            debug.error("Invalid number of predecode inputs: {}".format(inputs),-1)
            
    def setup_layout_constraints(self):

        self.height = self.number_of_outputs * self.nand.height

        # x offset for input inverters
        self.x_off_inv_1 = self.number_of_inputs*self.m2_pitch 

        # x offset to NAND decoder includes the left rails, mid rails and inverters, plus two extra m2 pitches
        self.x_off_nand = self.x_off_inv_1 + self.inv.width + (2*self.number_of_inputs + 2) * self.m2_pitch

        # x offset to output inverters
        self.x_off_inv_2 = self.x_off_nand + self.nand.width

        # Height width are computed 
        self.width = self.x_off_inv_2 + self.inv.width

    def route_rails(self):
        """ Create all of the rails for the inputs and vdd/gnd/inputs_bar/inputs """
        input_names = ["in[{}]".format(x) for x in range(self.number_of_inputs)]
        offset = vector(0.5*self.m2_width,2*self.m1_width)
        self.input_rails = self.create_vertical_pin_bus(layer="metal2",
                                                        pitch=self.m2_pitch,
                                                        offset=offset,
                                                        names=input_names,
                                                        length=self.height - 2*self.m1_width)

        invert_names = ["Abar[{}]".format(x) for x in range(self.number_of_inputs)]
        non_invert_names = ["A[{}]".format(x) for x in range(self.number_of_inputs)]
        decode_names = invert_names + non_invert_names
        offset = vector(self.x_off_inv_1 + self.inv.width + 2*self.m2_pitch, 2*self.m1_width)
        self.decode_rails = self.create_vertical_bus(layer="metal2",
                                                     pitch=self.m2_pitch,
                                                     offset=offset,
                                                     names=decode_names,
                                                     length=self.height - 2*self.m1_width)

        
    def create_input_inverters(self):
        """ Create the input inverters to invert input signals for the decode stage. """
        self.in_inst = []
        for inv_num in range(self.number_of_inputs):
            name = "Xpre_inv[{0}]".format(inv_num)
            self.in_inst.append(self.add_inst(name=name,
                                              mod=self.inv))
            self.connect_inst(["in[{0}]".format(inv_num),
                               "inbar[{0}]".format(inv_num),
                               "vdd", "gnd"])

    def place_input_inverters(self):
        """ Place the input inverters to invert input signals for the decode stage. """
        for inv_num in range(self.number_of_inputs):
            if (inv_num % 2 == 0):
                y_off = inv_num * (self.inv.height)
                mirror = "R0"
            else:
                y_off = (inv_num + 1) * (self.inv.height)
                mirror="MX"
            offset = vector(self.x_off_inv_1, y_off)
            self.in_inst[inv_num].place(offset=offset,
                                        mirror=mirror)
            
    def create_output_inverters(self):
        """ Create inverters for the inverted output decode signals. """
        self.inv_inst = []
        for inv_num in range(self.number_of_outputs):
            name = "Xpre_nand_inv[{}]".format(inv_num)
            self.inv_inst.append(self.add_inst(name=name,
                                               mod=self.inv))
            self.connect_inst(["Z[{}]".format(inv_num),
                               "out[{}]".format(inv_num),
                               "vdd", "gnd"])


    def place_output_inverters(self):
        """ Place inverters for the inverted output decode signals. """
        for inv_num in range(self.number_of_outputs):
            if (inv_num % 2 == 0):
                y_off = inv_num * self.inv.height
                mirror = "R0"
            else:
                y_off =(inv_num + 1)*self.inv.height
                mirror = "MX"
            offset = vector(self.x_off_inv_2, y_off)   
            self.inv_inst[inv_num].place(offset=offset,
                                         mirror=mirror)

    def create_nand_array(self,connections):
        """ Create the NAND stage for the decodes """
        self.nand_inst = []        
        for nand_input in range(self.number_of_outputs):
            inout = str(self.number_of_inputs)+"x"+str(self.number_of_outputs)
            name = "Xpre{0}_nand[{1}]".format(inout,nand_input)
            self.nand_inst.append(self.add_inst(name=name,
                                                mod=self.nand))
            self.connect_inst(connections[nand_input])


    def place_nand_array(self):
        """ Place the NAND stage for the decodes """
        for nand_input in range(self.number_of_outputs):
            inout = str(self.number_of_inputs)+"x"+str(self.number_of_outputs)
            if (nand_input % 2 == 0):
                y_off = nand_input * self.inv.height
                mirror = "R0"
            else:
                y_off = (nand_input + 1) * self.inv.height
                mirror = "MX"
            offset = vector(self.x_off_nand, y_off)
            self.nand_inst[nand_input].place(offset=offset,
                                             mirror=mirror)
            

    def route(self):
        self.route_input_inverters()
        self.route_inputs_to_rails()
        self.route_nand_to_rails()
        self.route_output_inverters()        
        self.route_vdd_gnd()

    def route_inputs_to_rails(self):
        """ Route the uninverted inputs to the second set of rails """
        for num in range(self.number_of_inputs):
            # route one signal next to each vdd/gnd rail since this is
            # typically where the p/n devices are and there are no
            # pins in the nand gates. 
            y_offset = (num+self.number_of_inputs) * self.inv.height + contact.m1m2.width + self.m1_space
            in_pin = "in[{}]".format(num)            
            a_pin = "A[{}]".format(num)
            in_pos = vector(self.input_rails[in_pin].x,y_offset)
            a_pos = vector(self.decode_rails[a_pin].x,y_offset)            
            self.add_path("metal1",[in_pos, a_pos])
            self.add_via_center(layers = ("metal1", "via1", "metal2"),
                                offset=[self.input_rails[in_pin].x, y_offset],
                                rotate=90)
            self.add_via_center(layers = ("metal1", "via1", "metal2"),
                                offset=[self.decode_rails[a_pin].x, y_offset],
                                rotate=90)

    def route_output_inverters(self):
        """
        Route all conections of the outputs inverters 
        """
        for num in range(self.number_of_outputs):

            # route nand output to output inv input
            zr_pos = self.nand_inst[num].get_pin("Z").rc()
            al_pos = self.inv_inst[num].get_pin("A").lc()
            # ensure the bend is in the middle 
            mid1_pos = vector(0.5*(zr_pos.x+al_pos.x), zr_pos.y)
            mid2_pos = vector(0.5*(zr_pos.x+al_pos.x), al_pos.y)
            self.add_path("metal1", [zr_pos, mid1_pos, mid2_pos, al_pos])

            z_pin = self.inv_inst[num].get_pin("Z")
            self.add_layout_pin(text="out[{}]".format(num),
                                layer="metal1",
                                offset=z_pin.ll(),
                                height=z_pin.height(),
                                width=z_pin.width())

    
    def route_input_inverters(self):
        """
        Route all conections of the inputs inverters [Inputs, outputs, vdd, gnd] 
        """
        for inv_num in range(self.number_of_inputs):
            out_pin = "Abar[{}]".format(inv_num)
            in_pin = "in[{}]".format(inv_num)
            
            #add output so that it is just below the vdd or gnd rail
            # since this is where the p/n devices are and there are no
            # pins in the nand gates.
            y_offset = (inv_num+1) * self.inv.height - 3*self.m1_space
            inv_out_pos = self.in_inst[inv_num].get_pin("Z").rc()
            right_pos = inv_out_pos + vector(self.inv.width - self.inv.get_pin("Z").lx(),0)
            rail_pos = vector(self.decode_rails[out_pin].x,y_offset)
            self.add_path("metal1", [inv_out_pos, right_pos, vector(right_pos.x, y_offset), rail_pos])
            self.add_via_center(layers = ("metal1", "via1", "metal2"),
                                offset=rail_pos,
                                rotate=90)

            
            #route input
            inv_in_pos = self.in_inst[inv_num].get_pin("A").lc()
            in_pos = vector(self.input_rails[in_pin].x,inv_in_pos.y)
            self.add_path("metal1", [in_pos, inv_in_pos])
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=in_pos,
                                rotate=90)
            

    def route_nand_to_rails(self):
        # This 2D array defines the connection mapping 
        nand_input_line_combination = self.get_nand_input_line_combination()
        for k in range(self.number_of_outputs):
            # create x offset list         
            index_lst= nand_input_line_combination[k]

            if self.number_of_inputs == 2:
                gate_lst = ["A","B"]
            else:
                gate_lst = ["A","B","C"]

            # this will connect pins A,B or A,B,C
            for rail_pin,gate_pin in zip(index_lst,gate_lst):
                pin_pos = self.nand_inst[k].get_pin(gate_pin).lc()
                rail_pos = vector(self.decode_rails[rail_pin].x, pin_pos.y)
                self.add_path("metal1", [rail_pos, pin_pos])
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=rail_pos,
                                    rotate=90)



    def route_vdd_gnd(self):
        """ Add a pin for each row of vdd/gnd which are must-connects next level up. """

        # Find the x offsets for where the vias/pins should be placed
        in_xoffset = self.in_inst[0].rx()
        out_xoffset = self.inv_inst[0].lx()
        for num in range(0,self.number_of_outputs):
            # this will result in duplicate polygons for rails, but who cares
            
            # Route both supplies
            for n in ["vdd", "gnd"]:
                nand_pin = self.nand_inst[num].get_pin(n)
                supply_offset = nand_pin.ll().scale(0,1)
                self.add_rect(layer="metal1",
                              offset=supply_offset,
                              width=self.inv_inst[num].rx())

                # Add pins in two locations
                for xoffset in [in_xoffset, out_xoffset]:
                    pin_pos = vector(xoffset, nand_pin.cy())
                    self.add_via_center(layers=("metal1", "via1", "metal2"),
                                        offset=pin_pos,
                                        rotate=90)
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=pin_pos,
                                        rotate=90)
                    self.add_layout_pin_rect_center(text=n,
                                                    layer="metal3",
                                                    offset=pin_pos)
            


