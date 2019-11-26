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

# Blender imports
from mathutils import Vector

# Internal imports
import nmv
import nmv.bbox
import nmv.consts
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.mesh
import nmv.rendering
import nmv.scene
import nmv.skeleton
import nmv.utilities


################################################################################################
# @draw_soma_to_arbors_connectivity
################################################################################################
def draw_soma_to_arbors_connectivity(panel,
                                     scene):
    """Draws the options of the soma to arbors connectivity.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    soma_connection_row = panel.layout.row()
    soma_connection_row.label(text='Soma:')
    soma_connection_row.prop(scene, 'NMV_SomaArborsConnection', expand=True)
    nmv.interface.ui_options.mesh.soma_connection = scene.NMV_SomaArborsConnection


################################################################################################
# @draw_mesh_connectivity_options
################################################################################################
def draw_mesh_connectivity_options(panel,
                                   scene):
    """Draws the mesh connectivity options.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Meshing options reference
    meshing_options = nmv.interface.ui_options.mesh

    # If the soma is connected, then by default, the arbors are connected
    if meshing_options.soma_connection == nmv.enums.Meshing.SomaConnection.DISCONNECTED:

        # Mesh objects connection
        mesh_objects_connection_row = panel.layout.row()
        mesh_objects_connection_row.label(text='Skeleton Objects:')
        mesh_objects_connection_row.prop(scene, 'NMV_MeshObjectsConnection', expand=True)
        meshing_options.neuron_objects_connection = scene.NMV_MeshObjectsConnection

    else:
        meshing_options.neuron_objects_connection = nmv.enums.Meshing.ObjectsConnection.DISCONNECTED


####################################################################################################
# @draw_spines_options
####################################################################################################
def draw_spines_options(panel,
                        scene):
    """Draw the spines options to the layout of the meshing panel.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Meshing options reference
    meshing_options = nmv.interface.ui_options.mesh

    # Spines options
    spine_options_row = panel.layout.row()
    spine_options_row.label(text='Spine Options:', icon='MOD_WAVE')

    # Spines source
    spines_row = panel.layout.row()
    spines_row.label(text='Source:')

    # If you are reading from a BBP circuit, use the locations reported in the circuit, otherwise
    # use random spines
    if scene.NMV_InputSource == nmv.enums.Input.CIRCUIT_GID:
        spines_row.prop(scene, 'NMV_SpinesSourceCircuit', expand=True)
        meshing_options.spines = scene.NMV_SpinesSourceCircuit
    else:
        spines_row.prop(scene, 'NMV_SpinesSourceRandom', expand=True)
        meshing_options.spines = scene.NMV_SpinesSourceRandom

    # If the spines are not ignored
    if not meshing_options.spines == nmv.enums.Meshing.Spines.Source.IGNORE:

        # Spines quality
        spines_quality_row = panel.layout.row()
        spines_quality_row.label(text='Quality:')
        spines_quality_row.prop(scene, 'NMV_SpineMeshQuality', expand=True)
        meshing_options.spines_mesh_quality = scene.NMV_SpineMeshQuality

        # In case of random spines, identify the percentage of randomness
        if meshing_options.spines == nmv.enums.Meshing.Spines.Source.RANDOM:

            # Randomness percentage
            spines_percentage_row = panel.layout.row()
            spines_percentage_row.label(text='Percentage:')
            spines_percentage_row.prop(scene, 'NMV_RandomSpinesPercentage')
            meshing_options.random_spines_percentage = scene.NMV_RandomSpinesPercentage


################################################################################################
# @draw_tessellation_options
################################################################################################
def draw_tessellation_options(panel, 
                              scene):
    """Draws the tessellation options.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Meshing options reference
    meshing_options = nmv.interface.ui_options.mesh

    # Tessellation parameters
    tess_level_row = panel.layout.row()
    tess_level_row.prop(scene, 'NMV_TessellateMesh')
    tess_level_column = tess_level_row.column()
    tess_level_column.prop(scene, 'NMV_MeshTessellationLevel')

    # Disable the tessellation
    if not scene.NMV_TessellateMesh:
        meshing_options.tessellate_mesh = False

        # Use 1.0 to disable the tessellation
        meshing_options.tessellation_level = 1.0
        tess_level_column.enabled = False

    # Activate the tessellation
    else:
        meshing_options.tessellate_mesh = scene.NMV_TessellateMesh
        meshing_options.tessellation_level = scene.NMV_MeshTessellationLevel


################################################################################################
# @draw_piece_wise_meshing_options
################################################################################################
def draw_piece_wise_meshing_options(panel,
                                    scene):
    """Draws the options when the Meta Objects meshing technique is selected.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Components
    components_row = panel.layout.row()
    components_row.label(text='Filling:')
    components_row.prop(scene, 'NMV_MeshingPiecewiseFilling', expand=True)
    nmv.interface.ui_options.mesh.piecewise_filling = scene.NMV_MeshingPiecewiseFilling

    # Which technique to use to reconstruct the soma
    soma_type_row = panel.layout.row()
    soma_type_row.label(text='Soma:')
    soma_type_row.prop(scene, 'NMV_MeshingPiecewiseSoma', expand=True)
    nmv.interface.ui_options.mesh.soma_reconstruction_technique = scene.NMV_MeshingPiecewiseSoma

    # Edges
    mesh_edges_row = panel.layout.row()
    mesh_edges_row.label(text='Edges:')
    mesh_edges_row.prop(scene, 'NMV_MeshSmoothing', expand=True)
    nmv.interface.ui_options.mesh.edges = scene.NMV_MeshSmoothing

    # Surface roughness
    if nmv.interface.ui_options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:
        mesh_surface_row = panel.layout.row()
        mesh_surface_row.label(text='Surface:')
        mesh_surface_row.prop(scene, 'NMV_SurfaceRoughness', expand=True)
        nmv.interface.ui_options.mesh.surface = scene.NMV_SurfaceRoughness
    else:
        nmv.interface.ui_options.mesh.surface = nmv.enums.Meshing.Surface.SMOOTH

    # Connectivity options
    draw_soma_to_arbors_connectivity(panel=panel, scene=scene)

    # Tessellation options
    draw_tessellation_options(panel=panel, scene=scene)

    # Spine options
    draw_spines_options(panel=panel, scene=scene)


################################################################################################
# @draw_color_options
################################################################################################
def draw_color_options(panel,
                       scene):
    """Draw the coloring options.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Get a reference to the layout of the panel
    layout = panel.layout

    # Coloring parameters
    colors_row = layout.row()
    colors_row.label(text='Colors & Materials:', icon='COLOR')

    # Mesh material
    mesh_material_row = layout.row()
    mesh_material_row.prop(scene, 'NMV_MeshMaterial')
    nmv.interface.ui_options.mesh.material = scene.NMV_MeshMaterial

    # Draw the meshing options
    if scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT or \
       scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.UNION or \
       scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.SKINNING:

        # Homogeneous mesh coloring
        homogeneous_color_row = layout.row()
        homogeneous_color_row.prop(scene, 'NMV_MeshHomogeneousColor')

        # If the homogeneous color flag is set
        if scene.NMV_MeshHomogeneousColor:
            neuron_color_row = layout.row()
            neuron_color_row.prop(scene, 'NMV_NeuronMeshColor')

            nmv.interface.ui_options.mesh.soma_color = \
                scene.NMV_NeuronMeshColor
            nmv.interface.ui_options.mesh.axon_color = \
                scene.NMV_NeuronMeshColor
            nmv.interface.ui_options.mesh.basal_dendrites_color = \
                scene.NMV_NeuronMeshColor
            nmv.interface.ui_options.mesh.apical_dendrites_color = \
                scene.NMV_NeuronMeshColor
            nmv.interface.ui_options.mesh.spines_color = \
                scene.NMV_NeuronMeshColor

        # Different colors
        else:
            soma_color_row = layout.row()
            soma_color_row.prop(scene, 'NMV_SomaMeshColor')
            nmv.interface.ui_options.mesh.soma_color = scene.NMV_SomaMeshColor

            axon_color_row = layout.row()
            axon_color_row.prop(scene, 'NMV_AxonMeshColor')
            nmv.interface.ui_options.mesh.axon_color = scene.NMV_AxonMeshColor

            basal_dendrites_color_row = layout.row()
            basal_dendrites_color_row.prop(scene, 'NMV_BasalDendritesMeshColor')
            nmv.interface.ui_options.mesh.basal_dendrites_color = \
                scene.NMV_BasalDendritesMeshColor

            apical_dendrites_color_row = layout.row()
            apical_dendrites_color_row.prop(scene, 'NMV_ApicalDendriteMeshColor')
            nmv.interface.ui_options.mesh.apical_dendrites_color = \
                scene.NMV_ApicalDendriteMeshColor

            # Spines must be there to set a color for them
            if nmv.interface.ui_options.mesh.spines != nmv.enums.Meshing.Spines.Source.IGNORE:
                spines_color_row = layout.row()
                spines_color_row.prop(scene, 'NMV_SpinesMeshColor')
                nmv.interface.ui_options.mesh.spines_color = scene.NMV_SpinesMeshColor

    elif scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.META_OBJECTS:

        neuron_color_row = layout.row()
        neuron_color_row.prop(scene, 'NMV_NeuronMeshColor')

        # Pass options from UI to system
        nmv.interface.ui_options.mesh.soma_color = \
            scene.NMV_NeuronMeshColor
        nmv.interface.ui_options.mesh.axon_color = \
            scene.NMV_NeuronMeshColor
        nmv.interface.ui_options.mesh.basal_dendrites_color = \
            scene.NMV_NeuronMeshColor
        nmv.interface.ui_options.mesh.apical_dendrites_color = \
            scene.NMV_NeuronMeshColor
        nmv.interface.ui_options.mesh.spines_color = \
            scene.NMV_NeuronMeshColor

    # Add nucleus color option if they are not ignored
    if scene.NMV_Nucleus != nmv.enums.Meshing.Nucleus.IGNORE:
        nucleus_color_row = layout.row()
        nucleus_color_row.prop(scene, 'NMV_NucleusMeshColor')

        nmv.interface.ui_options.mesh.nucleus_color = Vector((
            scene.NMV_NucleusMeshColor.r, scene.NMV_NucleusMeshColor.g,
            scene.NMV_NucleusMeshColor.b))


################################################################################################
# @draw_rendering_options
################################################################################################
def draw_rendering_options(panel,
                           scene):
    """Draw the rendering options.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Get a reference to the layout of the panel
    layout = panel.layout

    # Rendering options
    quick_rendering_row = layout.row()
    quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')
    panel.shown_hidden_rows.append(quick_rendering_row)

    # Rendering view
    rendering_view_row = layout.row()
    rendering_view_row.label(text='View:')
    rendering_view_row.prop(scene, 'NMV_MeshRenderingView', expand=True)
    panel.shown_hidden_rows.append(rendering_view_row)

    # Add the close up size option
    if scene.NMV_MeshRenderingView == nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

        # Close up size option
        close_up_size_row = layout.row()
        close_up_size_row.label(text='Close Up Size:')
        close_up_size_row.prop(scene, 'NMV_MeshCloseUpSize')
        close_up_size_row.enabled = True
        panel.shown_hidden_rows.append(close_up_size_row)

        # Frame resolution option (only for the close up mode)
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(scene, 'NMV_MeshFrameResolution')
        frame_resolution_row.enabled = True
        panel.shown_hidden_rows.append(frame_resolution_row)

    # Otherwise, render the Mid and Wide shot modes
    else:

        # Rendering resolution
        rendering_resolution_row = layout.row()
        rendering_resolution_row.label(text='Resolution:')
        rendering_resolution_row.prop(scene, 'NMV_MeshRenderingResolution', expand=True)
        panel.shown_hidden_rows.append(rendering_resolution_row)

        # Add the frame resolution option
        if scene.NMV_MeshRenderingResolution == \
                nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

            # Frame resolution option (only for the close up mode)
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(scene, 'NMV_MeshFrameResolution')
            frame_resolution_row.enabled = True
            panel.shown_hidden_rows.append(frame_resolution_row)

        # Otherwise, add the scale factor option
        else:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(scene, 'NMV_MeshFrameScaleFactor')
            scale_factor_row.enabled = True
            panel.shown_hidden_rows.append(scale_factor_row)

    # Keep the cameras used for the rendering in the scene
    keep_cameras_row = layout.row()
    keep_cameras_row.prop(scene, 'NMV_KeepMeshCameras')
    keep_cameras_row.enabled = False

    # Rendering view
    render_view_row = layout.row()
    render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
    render_view_buttons_row = layout.row(align=True)
    render_view_buttons_row.operator('nmv.render_mesh_front', icon='AXIS_FRONT')
    render_view_buttons_row.operator('nmv.render_mesh_side', icon='AXIS_SIDE')
    render_view_buttons_row.operator('nmv.render_mesh_top', icon='AXIS_TOP')
    render_view_buttons_row.enabled = True
    panel.shown_hidden_rows.append(render_view_buttons_row)

    render_animation_row = layout.row()
    render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
    render_animations_buttons_row = layout.row(align=True)
    render_animations_buttons_row.operator('nmv.render_mesh_360', icon='FORCE_MAGNETIC')
    render_animations_buttons_row.enabled = True
    panel.shown_hidden_rows.append(render_animations_buttons_row)

    # Soma rendering progress bar
    neuron_mesh_rendering_progress_row = layout.row()
    neuron_mesh_rendering_progress_row.prop(scene, 'NMV_NeuronMeshRenderingProgress')
    neuron_mesh_rendering_progress_row.enabled = False
    panel.shown_hidden_rows.append(neuron_mesh_rendering_progress_row)


################################################################################################
# @draw_meshing_options
################################################################################################
def draw_meshing_options(panel,
                         scene):
    """Draw the options of the meshing.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Get a reference to the layout of the panel
    layout = panel.layout

    # Skeleton meshing options
    skeleton_meshing_options_row = layout.row()
    skeleton_meshing_options_row.label(text='Meshing Options:', icon='SURFACE_DATA')

    # Which meshing technique to use
    meshing_method_row = layout.row()
    meshing_method_row.prop(scene, 'NMV_MeshingTechnique', icon='OUTLINER_OB_EMPTY')
    nmv.interface.ui_options.mesh.meshing_technique = scene.NMV_MeshingTechnique

    # Draw the meshing options
    if scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
        draw_piece_wise_meshing_options(panel=panel, scene=scene)
    elif scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.META_OBJECTS:
        draw_meta_objects_meshing_options(panel=panel, scene=scene)
    elif scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.SKINNING:
        draw_skinning_meshing_options(panel=panel, scene=scene)
    elif scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.UNION:
        draw_union_meshing_options(panel=panel, scene=scene)
    else:
        pass


################################################################################################
# @draw_skinning_meshing_options
################################################################################################
def draw_skinning_meshing_options(panel,
                                  scene):
    """Draws the options when the skinning meshing technique is selected.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Surface roughness
    if nmv.interface.ui_options.mesh.edges == nmv.enums.Meshing.Edges.SMOOTH:
        mesh_surface_row = panel.layout.row()
        mesh_surface_row.label(text='Surface:')
        mesh_surface_row.prop(scene, 'NMV_SurfaceRoughness', expand=True)
        nmv.interface.ui_options.mesh.surface = scene.NMV_SurfaceRoughness
    else:
        nmv.interface.ui_options.mesh.surface = nmv.enums.Meshing.Surface.SMOOTH

    # Connectivity options
    draw_soma_to_arbors_connectivity(panel=panel, scene=scene)

    # Tessellation options
    draw_tessellation_options(panel=panel, scene=scene)

    # Spine options
    draw_spines_options(panel=panel, scene=scene)


################################################################################################
# @draw_meta_objects_meshing_options
################################################################################################
def draw_meta_objects_meshing_options(panel,
                                      scene):
    """Draws the options when the meta objects meshing technique is selected.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Tessellation options
    draw_tessellation_options(panel=panel, scene=scene)


################################################################################################
# @draw_union_meshing_options
################################################################################################
def draw_union_meshing_options(panel,
                               scene):
    """Draws the options when the union meshing technique is selected.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Surface roughness
    mesh_surface_row = panel.layout.row()
    mesh_surface_row.label(text='Surface:')
    mesh_surface_row.prop(scene, 'NMV_SurfaceRoughness', expand=True)

    # Pass options from UI to system
    nmv.interface.ui_options.mesh.surface = scene.NMV_SurfaceRoughness

    # Edges
    mesh_edges_row = panel.layout.row()
    mesh_edges_row.label(text='Edges:')
    mesh_edges_row.prop(scene, 'NMV_MeshSmoothing', expand=True)

    # Pass options from UI to system
    nmv.interface.ui_options.mesh.edges = scene.NMV_MeshSmoothing

    # Connectivity options
    draw_soma_to_arbors_connectivity(panel=panel, scene=scene)

    # Tessellation options
    draw_tessellation_options(panel=panel, scene=scene)

    # Spine options
    draw_spines_options(panel=panel, scene=scene)


################################################################################################
# @draw_mesh_reconstruction_button
################################################################################################
def draw_mesh_reconstruction_button(panel,
                                    scene):
    """Draw the mesh reconstruction button.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Get a reference to the layout of the panel
    layout = panel.layout

    # Mesh quick reconstruction options
    quick_reconstruction_row = layout.row()
    quick_reconstruction_row.label(text='Quick Reconstruction:', icon='PARTICLE_POINT')

    # Mesh reconstruction options
    mesh_reconstruction_row = layout.row()
    mesh_reconstruction_row.operator('nmv.reconstruct_neuron_mesh', icon='MESH_DATA')


################################################################################################
# @draw_mesh_export_options
################################################################################################
def draw_mesh_export_options(panel,
                             scene):
    """Draw the mesh export options.

    :param panel:
        Blender UI panel.
    :param scene:
        Blender scene.
    """

    # Get a reference to the layout of the panel
    layout = panel.layout

    # Saving meshes parameters
    save_neuron_mesh_row = layout.row()
    save_neuron_mesh_row.label(text='Export Neuron Mesh:', icon='MESH_UVSPHERE')

    export_format = layout.row()
    export_format.prop(scene, 'NMV_ExportedMeshFormat', icon='GROUP_VERTEX')

    if not scene.NMV_ExportedMeshFormat == nmv.enums.Meshing.ExportFormat.BLEND:
        if scene.NMV_MeshingTechnique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
            export_individual_row = layout.row()
            export_individual_row.prop(scene, 'NMV_ExportIndividuals')

    # Save button
    save_neuron_mesh_buttons_column = layout.column(align=True)
    save_neuron_mesh_buttons_column.operator('nmv.export_neuron_mesh', icon='MESH_DATA')
    save_neuron_mesh_buttons_column.enabled = True
    panel.shown_hidden_rows.append(save_neuron_mesh_buttons_column)