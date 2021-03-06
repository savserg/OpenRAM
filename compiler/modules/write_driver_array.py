from math import log
import design
from tech import drc
import debug
from vector import vector
from globals import OPTS

class write_driver_array(design.design):
    """
    Array of tristate drivers to write to the bitlines through the column mux.
    Dynamically generated write driver array of all bitlines.
    """

    def __init__(self, columns, word_size):
        design.design.__init__(self, "write_driver_array")
        debug.info(1, "Creating {0}".format(self.name))

        self.columns = columns
        self.word_size = word_size
        self.words_per_row = int(columns / word_size)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()


    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_write_array()
        
    def create_layout(self):
    
        if self.bitcell.width > self.driver.width:
            self.width = self.columns * self.bitcell.width
        else:
            self.width = self.columns * self.driver.width
        
        self.height = self.driver.height
        
        self.place_write_array()
        self.add_layout_pins()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.word_size):
            self.add_pin("data[{0}]".format(i))
        for i in range(self.word_size):            
            self.add_pin("bl[{0}]".format(i))
            self.add_pin("br[{0}]".format(i))
        self.add_pin("en")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):
        from importlib import reload
        c = reload(__import__(OPTS.write_driver))
        self.mod_write_driver = getattr(c, OPTS.write_driver)
        self.driver = self.mod_write_driver("write_driver")
        self.add_mod(self.driver)

        # This is just used for measurements,
        # so don't add the module
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()

    def create_write_array(self):
        self.driver_insts = {}
        for i in range(0,self.columns,self.words_per_row):
            name = "Xwrite_driver{}".format(i)
            index = int(i/self.words_per_row)
            self.driver_insts[index]=self.add_inst(name=name,
                                                   mod=self.driver)

            self.connect_inst(["data[{0}]".format(index),
                               "bl[{0}]".format(index),
                               "br[{0}]".format(index),
                               "en", "vdd", "gnd"])


    def place_write_array(self):
        if self.bitcell.width > self.driver.width:
            driver_spacing = self.bitcell.width
        else:
            driver_spacing = self.driver.width
    
        for i in range(0,self.columns,self.words_per_row):
            index = int(i/self.words_per_row)            
            base = vector(i * driver_spacing,0)
            self.driver_insts[index].place(base)

            
    def add_layout_pins(self):
        for i in range(self.word_size):
            din_pin = self.driver_insts[i].get_pin("din")
            self.add_layout_pin(text="data[{0}]".format(i),
                                layer="metal2",
                                offset=din_pin.ll(),
                                width=din_pin.width(),
                                height=din_pin.height())
            bl_pin = self.driver_insts[i].get_pin("bl")            
            self.add_layout_pin(text="bl[{0}]".format(i),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=bl_pin.height())
                           
            br_pin = self.driver_insts[i].get_pin("br")
            self.add_layout_pin(text="br[{0}]".format(i),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=br_pin.height())

            for n in ["vdd", "gnd"]:
                pin_list = self.driver_insts[i].get_pins(n)
                for pin in pin_list:
                    pin_pos = pin.center()
                    # Add the M2->M3 stack 
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=pin_pos)
                    self.add_layout_pin_rect_center(text=n,
                                                    layer="metal3",
                                                    offset=pin_pos)



        self.add_layout_pin(text="en",
                            layer="metal1",
                            offset=self.driver_insts[0].get_pin("en").ll().scale(0,1),
                            width=self.width,
                            height=drc['minwidth_metal1'])
                       
                       

