
class LM5060:
    ISENSE = 16e-6
    VOFFSET = 0
    UVLOTH = 1.6
    UVLOBIAS = 5.5e-6
    OVPTH = 2.0

    @classmethod
    def getRs(cls, idsth: float, rdson: float) -> float:
        return ((idsth * rdson) + LM5060.VOFFSET) / LM5060.ISENSE

    @classmethod
    def getIdsth(cls, rs: float, rdson: float) -> float:
        return ((rs * LM5060.ISENSE) - LM5060.VOFFSET) / rdson

    @classmethod
    def getUVLORh(cls, vinmin: float, rl: float) -> float:
        """Get UVLO high-side resistor value

        Args:
            vinmin (float): UVLO cutoff voltage
            rl (float): low side resistor value. recommended value: <100k

        Returns:
            float: high side resistor value
        """
        return (vinmin - LM5060.UVLOTH) / (LM5060.UVLOBIAS + LM5060.UVLOTH / rl)

    @classmethod
    def getVinmin(cls, rh, rl):
        return (LM5060.UVLOBIAS + LM5060.UVLOTH / rl) * rh + LM5060.UVLOTH

    @classmethod
    def getOVPRh(cls, vinmax, rl):
        return rl * (vinmax - LM5060.OVPTH) / LM5060.OVPTH

    @classmethod
    def getVinmax(cls, rh, rl):
        return LM5060.OVPTH + rh * LM5060.OVPTH / rl


class DMTH8003SPS:
    RDSON = 6e-3  # ohm, Vgs=6V


if __name__ == '__main__':
    EIA_E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7,
               3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

    # Calculate sense resistor value for given Idsth
    Idsth = 100
    Rs = LM5060.getRs(idsth=Idsth, rdson=DMTH8003SPS.RDSON)
    print("Idsth = {:.3f} -> Rs = {:.3f} kOhm".format(Idsth, Rs / 1000))

    # List Idsth you can get with E24 resistors
    print("Calculate sense pin resistor value")
    for r in EIA_E24:
        rs = r * 10e3
        idsth = LM5060.getIdsth(rs=rs, rdson=DMTH8003SPS.RDSON)
        print("R = {} kOhm, Idsth = {:.1f} A".format(rs/1000, idsth))

    # List high side resistor value for a given UVLO and E24 low side resistor value
    vinmin = 12
    print(f"Calculate UVLO resistor value for {vinmin} V")
    for r in EIA_E24:
        rl = r * 10e3
        rh = LM5060.getUVLORh(vinmin=12, rl=rl)
        print("Rl = {} kOhm, Rh = {:.3f} kOhm".format(rl/1000, rh/1000))

    # List high side resistor value for a given OVP and E24 low side resistor value
    vinmax = 24
    print(f"Calculate OVP resistor value for {vinmax} V")
    for r in EIA_E24:
        rl = r * 10e3
        rh = LM5060.getOVPRh(vinmax=vinmax, rl=rl)
        print("Rl = {} kOhm, Rh = {:.3f} kOhm".format(rl/1000, rh/1000))
