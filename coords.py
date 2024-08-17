import datetime


class Coords():
    def __init__(self, x, y, Deg=True):
        self.x = x
        self.y = y
        self.Deg = Deg

    # # enables addition and subtraction of instances
    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coords(self.x - other.x, self.y - other.y)

    def t(self):
        return (self.x, self.y)

    def hrs(self):
        if self.Deg:
            self.x = self.x / 15
            self.y = self.y / 15
            self.Deg = False
        return self

    def deg(self):
        if not self.Deg:
            self.x = self.x * 15
            self.y = self.y * 15
            self.Deg = True
        return self

    def is_visible(self, star):  # returns True and angle of star if the star is within range of 4 hours
        self.hrs()
        if self.x - 4 <= star.x <= self.x + 4 and self.y - 4 <= star.y <= self.y + 4:
            star = star - self.hrs()
            star.Deg = False
            return True, star.deg().t()
        else:
            star = star - self.hrs()
            star.Deg = False
            return False, star.deg().t()

# The Finding reference point of celestial coordinate system w.r.t GCS (i.e. longitudes and latitudes)
def Rcc(at_time=datetime.datetime.now()):
    ref_eqnx_cord = Coords(145.404, 0)  # place of march equinox of 2021
    ref_eqnx_time = datetime.datetime(2021, 3, 20, 9, 37)
    days_diff = (at_time - ref_eqnx_time).total_seconds() / (3600 * 24)  # no. of days from last march equinox
    zero_correction = days_diff * (4 * 60 - 4) * 0.0042
    # correction due to difference between a day (24hrs) and solar day (23hrs, 56mins, 4secs)
    days_diff += zero_correction
    diff_wrt_ref_eq = (days_diff - int(days_diff)) * 360
    diff_wrt_SM = -(ref_eqnx_cord.x + diff_wrt_ref_eq) % 360
    return Coords(diff_wrt_SM, 0)
