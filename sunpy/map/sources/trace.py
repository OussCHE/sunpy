"""TRACE Map subclass definitions"""
#pylint: disable=W0221,W0222,E1101,E1121

__author__ = "Jack Ireland"
__email__ = "jack.ireland@nasa.gov"

from sunpy.map import GenericMap
from sunpy.cm import cm

from matplotlib import colors

__all__ = ['TRACEMap']

class TRACEMap(GenericMap):
    """TRACE Image Map definition
References
----------
For a description of TRACE headers see:
http://trace.lmsal.com/Project/Instrument/cal/
For a description of the TRACE mission, TRACE analysis guide (SSWIDL),
and all things TRACE (images, movies, galleries, science results), please
see:
http://trace.lmsal.com/
Note that this map definition is currently only being tested on JPEG2000
files. TRACE FITS data is stored in a more complex format. Typically
TRACE data is stored in hourly "tri" files that store all the data taken
by TRACE in the hour indicated by the filename. Those files must first be
understood and parsed to obtain the science data. The ability to do this
is not yet in SunPy, but is available in SSWIDL. Please refer to the links
above concerning how to read "tri" files in SSWIDL.
"""

    def __init__(self, data, header, **kwargs):

        GenericMap.__init__(self, data, header, **kwargs)

        # It needs to be verified that these must actually be set and are not
        # already in the header.
        self.meta['detector'] = "TRACE"
        self.meta['obsrvtry'] = "TRACE"
        self._nickname = self.detector
        # Colour maps
        self.plot_settings['cmap'] = cm.get_cmap('trace' + self.measurement)

    @classmethod
    def is_datasource_for(cls, data, header, **kwargs):
        """Determines if header corresponds to an TRACE image"""
        return header.get('instrume') == 'TRACE'

    def _get_mpl_normalizer(self):
        """Returns a Normalize object to be used with TRACE data"""
        mean = self.mean()
        std = self.std()

        vmin = 1
        vmax = min(self.max(), mean + 5 * std)

        return colors.LogNorm(vmin, vmax)
