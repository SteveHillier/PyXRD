# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

from pyxrd.generic.mathtext_support import mt_range
from pyxrd.generic.io import storables

from pyxrd.mvc import PropIntel

from .base_models import _AbstractProbability

@storables.register()
class R3G2Model(_AbstractProbability):
    """
	Reichweite = 3 / Components = 2
	Restrictions:
	2/3 <= W0 <= 1.0
	P11 = 0
	P101 = 0
	
	independent variables = 2
	W0
	P0000 (W0<3/4) of P1001 (W0>3/4)
        
        W1 = 1 – W0
        
        P0000 given (W0 < 3/4):
            W100/W000 = W1 / (W0 - 2*W1) 
            P0001 = 1-P0000
            P1000 = P0001 * W100/W000
            P1001 = 1 - P1000
        P1001 given (W0 >= 3/4):
            W000/W100 = (W0 - 2*W1) / W1
            P1000 = 1-P1001
            P0000 = 1 - P1000 * W100/W000
            P0001 = 1 - P0000
            
        P0010 = 1
        P0011 = 0
        
        P0100 = 1
        P0101 = 0
        
        since P11=0 and P101=0:
        P1100 = P1101 = P1010 = P1011 = P1110 = P1111 = P0110 = P0111 = 0
	
	indexes are NOT zero-based in external property names!
	"""

    # MODEL METADATA:
    class Meta(_AbstractProbability.Meta):
        store_id = "R3G2Model"
        independent_label_map = [
            ("W1", r"$W_1$", [2.0 / 3.0, 1.0]),
            ("P1111_or_P2112",
             r"$P_{1111} %s$ or $\newline P_{2112} %s$" % (
                mt_range(2.0 / 3.0, "W_1", 3.0 / 4.0),
                mt_range(3.0 / 4.0, "W_1", 1.0)
             ), [0.0, 1.0]),
        ]
        properties = [
            PropIntel(
                name=prop, label=label,
                minimum=rng[0], maximum=rng[1],
                data_type=float,
                refinable=True, storable=True, has_widget=True
            ) for prop, label, rng in independent_label_map
        ]


    # PROPERTIES:
    _W0 = 0.0
    def get_W1(self): return self._W0
    def set_W1(self, value): self._clamp_set_and_update("_W0", value)

    _P0000_P1001 = 0.0
    def get_P1111_or_P2112(self): return self._P0000_P1001
    def set_P1111_or_P2112(self, value): self._clamp_set_and_update("_P0000_P1001", value)

    # ------------------------------------------------------------
    #      Initialisation and other internals
    # ------------------------------------------------------------
    def setup(self, W1=0.85, P1111_or_P2112=0.75, **kwargs):
        _AbstractProbability.setup(self, R=3)
        self.W1 = W1
        self.P1111_or_P2112 = P1111_or_P2112

    # ------------------------------------------------------------
    #      Methods & Functions
    # ------------------------------------------------------------
    def update(self):
        with self.data_changed.hold_and_emit():
            self.mW[0] = self.W1
            self.mW[1] = 1.0 - self.W1

            # TODO add some boundary checks (e.g. P0000 = 1.0 or 0.0)
            # These make the calculations a lot simpler
            # Now some calcs return NaNs!!
            if self.mW[0] <= 0.75: # 0,0,0,0 is given
                self.mP[0, 0, 0, 0] = self.P1111_or_P2112
                self.mP[0, 0, 0, 1] = 1.0 - self.mP[0, 0, 0, 0]
                self.mP[1, 0, 0, 0] = self.mP[0, 0, 0, 1] * (self.mW[0] - 2 * self.mW[1]) / self.mW[1]
                self.mP[1, 0, 0, 1] = 1.0 - self.mP[1, 0, 0, 0]
            else: # 1,0,0,1 is given
                self.mP[1, 0, 0, 1] = self.P1111_or_P2112
                self.mP[1, 0, 0, 0] = 1.0 - self.mP[1, 0, 0, 1]
                self.mP[0, 0, 0, 0] = 1.0 - self.mP[1, 0, 0, 0] * self.mW[1] / (self.mW[0] - 2 * self.mW[1])
                self.mP[0, 0, 0, 1] = 1.0 - self.mP[0, 0, 0, 0]

            self.mP[0, 0, 1, 0] = 1.0
            self.mP[0, 1, 0, 0] = 1.0

            self.mP[0, 0, 1, 1] = 0.0
            self.mP[0, 1, 0, 1] = 0.0
            self.mP[0, 1, 1, 0] = 0.0
            self.mP[0, 1, 1, 1] = 0.0
            self.mP[1, 0, 1, 0] = 0.0
            self.mP[1, 0, 1, 1] = 0.0
            self.mP[1, 1, 0, 0] = 0.0
            self.mP[1, 1, 0, 1] = 0.0
            self.mP[1, 1, 1, 0] = 0.0
            self.mP[1, 1, 1, 1] = 0.0

            # since P11=0 and P101=0:
            self.mW[1, 0, 1] = self.mW[1, 1, 0] = self.mW[1, 1, 1] = 0.0

            t = (1 + 2 * self.mP[0, 0, 0, 1] / self.mP[1, 0, 0, 0])
            self.mW[0, 0, 0] = self.mW[0] / t
            self.mW[1, 0, 0] = self.mW[0, 1, 0] = self.mW[0, 0, 1] = 0.5 * (self.mW[0] - self.mW[0, 0, 0])
            self.mW[0, 1, 1] = self.mW[1] - self.mW[0, 0, 1]

            self.solve()
            self.validate()

    pass # end of class