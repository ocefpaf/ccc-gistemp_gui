#!/usr/bin/env python
# $URL$
# $Rev$
#
# parse_parameters.py
#
# Filipe Fernandes, 2011-08-08

import ConfigParser


class Dict2Struc(object):
    """ Open variables from a dictionary in a structure-like form."""
    def __init__(self, adict):
        for k in adict.keys():
            self.__dict__[k] = adict[k]

    def __repr__(self):
        return "Dict2Struc(%r)" % self.__dict__


class ParseConfig(object):
    """Parse ini config file with ccc-gistemp options."""
    def __init__(self, inifile='parameters.ini'):
        self.inifile = inifile
        self.config = ConfigParser.SafeConfigParser()
        # Make option names case sensitive.
        self.config.optionxform = str
        self.config.read(self.inifile)

        self._default = dict(data_sources="ghcn ushcn hohenpeissenberg scar",
                             augment_metadata='',
                             work_file_format="v2",
                             USHCN_meta='',
                             rural_designator="global_light",
                             USHCN_convert_id=True,
                             retain_contiguous_US=True,
                             USHCN_offset_start_year=1980,
                             USHCN_offset_max_months=10,
                             station_combine_min_overlap=4,
                             station_combine_bucket_radius=10,
                             station_combine_min_mid_years=5,
                             station_drop_minimum_months=20,
                             max_rural_brightness=10,
                             urban_adjustment_min_years=20,
                             urban_adjustment_min_rural_stations=3,
                             urban_adjustment_min_leg=5,
                             urban_adjustment_short_leg=7,
                             rural_station_min_overlap=20,
                             gridding_min_overlap=20,
                             subbox_min_valid=240,
                             subbox_land_range=100,
                             box_min_overlap=20,
                             zone_annual_min_months=6,
                             urban_adjustment_steep_leg=0.1,
                             urban_adjustment_leg_difference=0.05,
                             urban_adjustment_reverse_gradient=0.02,
                             urban_adjustment_full_radius=1000.0,
                             gridding_radius=1200.0,
                             sea_surface_cutoff_temp=-1.77,
                             gridding_reference_period=(1951, 1980),
                             subbox_reference_period=(1961, 1990),
                             box_reference_period=(1951, 1980),
                             urban_adjustment_proportion_good=2.0 / 3.0
                             )

    def config2dict(self):
        """ Update default options with those from the ini file. Return a
        variable parameters.<option> compatible with ccc-gistemp code.
        """

        parameters = self._default

        # Update default dict.
        # NOTE: Could use eval() for all and avoid all elifs. Also, that
        # would allow for meaningful section names.
        for section in self.config.sections():
            for opt in self.config.options(section):
                if section == "strings":
                    parameters[opt] = self.config.get(section, opt)
                elif section == "bools":
                    parameters[opt] = self.config.getboolean(section, opt)
                elif section == "ints":
                    parameters[opt] = self.config.getint(section, opt)
                elif section == "floats":
                    parameters[opt] = self.config.getfloat(section, opt)
                elif section == "special":
                    parameters[opt] = eval(self.config.get(section, opt))

        self.parameters = parameters

        return Dict2Struc(self.parameters)


def parameters():
    params = ParseConfig()
    return params.config2dict()

if __name__ == '__main__':
    import pprint
    pprint.pprint(parameters().__dict__)
