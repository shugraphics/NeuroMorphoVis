####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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

# System imports
import copy

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.bmeshi
import nmv.shading


####################################################################################################
# @DendrogramBuilder
####################################################################################################
class DendrogramBuilder:
    """Builds and draws the morphology as a series of samples where each sample is represented by
    a sphere.

    NOTE: We use bmeshes to generate the spheres and then link them to the scene all at once.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology.
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # System options
        self.options = copy.deepcopy(options)

        # All the reconstructed objects of the morphology, for example, poly-lines, spheres etc...
        self.morphology_objects = []

        # A list of the colors/materials of the soma
        self.soma_materials = None

        # A list of the colors/materials of the axon
        self.axon_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrite_materials = None

        # A list of the colors/materials of the articulation spheres
        self.articulation_materials = None

        # An aggregate list of all the materials of the skeleton
        self.skeleton_materials = list()

    ################################################################################################
    # @create_single_skeleton_materials_list
    ################################################################################################
    def create_single_skeleton_materials_list(self):
        """Creates a list of all the materials required for coloring the skeleton.

        NOTE: Before drawing the skeleton, create the materials, once and for all, to improve the
        performance since this is way better than creating a new material per section or segment
        or any individual object.
        """
        nmv.logger.info('Creating materials')

        # Create the default material list
        nmv.builders.skeleton.create_skeleton_materials_and_illumination(builder=self)

        # Index: 0 - 1
        self.skeleton_materials.extend(self.soma_materials)

        # Index: 2 - 3
        self.skeleton_materials.extend(self.apical_dendrite_materials)

        # Index: 4 - 5
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Index: 6 - 7
        self.skeleton_materials.extend(self.axon_materials)

    def get_leaves(self, section, leaves):

        if section.is_leaf():
            leaves.append(section)
        for child in section.children:
            self.get_leaves(child, leaves)

    def count_sub_tree_leaves(self,
                              root):
        leafs = list()
        self.get_leaves(root, leafs)
        print(len(leafs))
        return len(leafs)

    def get_leaves_of_arbor(self,
                            root):
        leaves = list()
        self.get_leaves(root, leaves)
        return leaves




    def compute_dendrogram_x_for_parents(self,
                                         node):

        # Get the parent
        if node is None:
            return

        parent = node.parent

        # Parent must not be None
        if parent is not None:

            # Compute X's for all the children
            x = 0

            for child in parent.children:

                # In case one is not computed
                if child.dendrogram_x is None:
                    return
                x += child.dendrogram_x

            x /= len(parent.children)

            # Do it
            parent.dendrogram_x = x

        # Do it for the parent
        self.compute_dendrogram_x_for_parents(parent)

    def print_dendro(self,
                     root):
        print('%d %f %f' % (root.branching_order, root.dendrogram_x, root.dendrogram_y))

        for child in root.children:
            self.print_dendro(child)

    def propagate_y(self,
                    root):

        if root is not None:
            root.dendrogram_y = root.compute_length()

        for child in root.children:
            self.propagate_y(child)


    def plot_path_length(self, section):

        section.length = nmv.skeleton.compute_section_length(section)
        if section.is_root():
            section.path_length = section.length
        else:
            section.path_length = section.parent.path_length + section.length
        print('%d %f' % (section.branching_order, section.path_length))

        for child in section.children:
            self.plot_path_length(child)



    def draw_dendrogram(self,
                        root):
        if root.is_root():
            starting = 0
        else:
            starting = root.parent.path_length
        ending = starting + root.length

        point_1 = Vector((root.dendrogram_x, starting, 0))
        point_2 = Vector((root.dendrogram_x, ending, 0))

        print('%d %f %f' % (root.branching_order, starting, ending))

        nmv.geometry.draw_line(point1=point_1, point2=point_2, thickness=1.0)

        # Draw the horizontal line
        if root.has_children():

            number_children = len(root.children)

            for i in range(number_children - 1) :
                child_1 = root.children[i]
                child_2 = root.children[i + 1]
                hline_point_1 = Vector((child_1.dendrogram_x - 0.5, ending, 0))
                hline_point_2 = Vector((child_2.dendrogram_x + 0.5, ending, 0))
                nmv.geometry.draw_line(point1=hline_point_1, point2=hline_point_2, thickness=1.0)


        for child in root.children:
            self.draw_dendrogram(child)


    # ratio between the left and the right gets the x distance
    def draw_arbor_dendrogram(self,
                              arbor):

        # Compute the total number of leaves of the arbor
        leaves = self.get_leaves_of_arbor(arbor)
        number_leaves = len(leaves)

        # Assuming that the delta is 4
        delta = 15

        # Total distance
        total_width = delta * (number_leaves - 1)

        # Assuming that the leaves will start at 0.0 on the x-axis
        for i, leaf in enumerate(leaves):
            print(leaf.branching_order)
            leaf.dendrogram_x = i * delta

        # Propagate the values upwards in the tree
        for leaf in leaves:
            self.compute_dendrogram_x_for_parents(leaf)

        self.propagate_y(arbor)

        print('-')
        self.plot_path_length(arbor)

        #self.print_dendro(arbor)
        self.draw_dendrogram(arbor)























    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building skeleton using SamplesBuilder')

        nmv.logger.info('Updating Radii')
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Resample the sections of the morphology skeleton
        nmv.builders.skeleton.resample_skeleton_sections(builder=self)

        if self.morphology.apical_dendrite is not None:
            self.draw_arbor_dendrogram(self.morphology.apical_dendrite)

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects

