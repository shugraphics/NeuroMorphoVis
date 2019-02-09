"""bmesh_face_ops.py:
    A set of utilities and operators for handling faces of bmesh objects.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import math

# Blender imports
import bmesh
from mathutils import Vector, Matrix

# Internal modules
#import intersection

import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.geometry


####################################################################################################
# @get_vertex_from_index
####################################################################################################
def get_vertex_from_index(bmesh_object,
                          vertex_index):
    """Gets a vertex of a bmesh object from its index.

    :param bmesh_object:
        A given bmesh object.
    :param vertex_index:
        The index of the vertex we need to get.
    :return:
        A reference to the vertex.
    """

    # Update the bmesh vertices
    bmesh_object.verts.ensure_lookup_table()

    # Get the vertex from its index
    vertex = bmesh_object.verts[vertex_index]

    # Return a reference to the vertex
    return vertex


####################################################################################################
# @extrude_vertex_towards_point
####################################################################################################
def extrude_vertex_towards_point(bmesh_object,
                                 index,
                                 point):
    """Extrude a vertex of a bmesh object to a given point in space.

    :param bmesh_object:
        A given bmesh object.
    :param index:
        The index of the vertex that will be extruded.
    :param point:
        A point in three-dimensional space.
    :return:
    """

    # Get a reference to the vertex
    vertex = get_vertex_from_index(bmesh_object, index)

    # Extrude the vertex (sort of via duplication)
    extruded_vertex = bmesh.ops.extrude_vert_indiv(bmesh_object, verts=[vertex])
    extruded_vertex = extruded_vertex['verts'][0]

    # Note that the extruded vertex is located at the same position of the original one
    # So we should update the coordinate of the extruded vertex to the given point
    extruded_vertex.co = point

    # Return a reference to the extruded vertex
    return extruded_vertex
