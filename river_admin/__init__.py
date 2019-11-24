from river_admin.site import Site


class RiverAdmin(object):
    icon = None
    name = None
    list_displays = None

    def get_list_displays(self):
        return self.list_displays


site = Site()
