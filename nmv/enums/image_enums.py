####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################


####################################################################################################
# @Image
####################################################################################################
class Image:
    """Image enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Extension
    ################################################################################################
    class Extension:
        """Extension edges
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        # PDF
        PDF = 'PDF'

        # TIFF
        TIFF = 'TIFF'

        # JPEG
        JPEG = 'JPEG'

        # PNG
        PNG = 'PNG'

        # BMP
        BMP = 'BMP'

        # TIFF
        TIFF = 'TIFF'

        # OpenEXR
        OPEN_EXR = 'OPEN_EXR'

