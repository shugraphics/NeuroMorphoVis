"""
@ create_layer_targets.py:
    Creates targets based on layer
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# System imports
import os, sys, subprocess


# NeuroRender imports
import neuron
# imports
import argparse
import random
import bbp
import brain
import morphology_utils

import core.utilities


################################################################################
# @parse_command_line_arguments
################################################################################
def parse_command_line_arguments():
    """Parse the input command line arguments and return a list of them.

    :return:
        A list with all the parsed arguments.
    """

    # Add all the options.
    parser = argparse.ArgumentParser()

    help = 'BBP circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=help)

    help = 'Cell target, default [mc2_Column]'
    parser.add_argument('--target',
                        action='store', default='mc2_Column', dest='target', help=help)

    help = 'Percentage of the target, default 100%'
    parser.add_argument('--percent',
                        action='store', default=100.0, dest='percent', help=help)

    help = 'Number of tags, default 1'
    parser.add_argument('--ntags',
                        action='store', default=1, dest='number_tags', help=help)

    help = 'The output path'
    parser.add_argument('--output',
                        action='store', default='.', dest='output', help=help)

    # parse the arguments, and return a list of them.
    return parser.parse_args()


################################################################################
# @create_targets
################################################################################
def create_targets(circuit_config,
                   target,
                   percent,
                   output,
                   number_tags):
    """Create the speficied targets.

    :param circuit_config:
        Circuit configuration.
    :param target:
        Input target.
    :param percent:
        Percentage.
    :param output:
        Output path.
    :param number_tags:
        The number of tags.
    :return:
        A Neuron list of all the cells created for the specified target.
    """

    # Use the BBP circuit configuration to open a bbp experiment
    experiment = bbp.Experiment()
    experiment.open(circuit_config)

    # Circuit
    micro_circuit = experiment.microcircuit()

    # Cell target
    cell_target = experiment.cell_target(target)

    # Load neurons only, since it will take forever to load the morphologies
    print('Loading the circuit from the BBPSDK')
    load_flags = bbp.Loading_Flags
    micro_circuit.load(cell_target, load_flags.NEURONS)

    # Get the BBP data
    neurons = micro_circuit.neurons()

    # Load the circuit from Brain
    print('Loading the circuit from Brain')
    circuit = brain.Circuit(circuit_config)

    # Get all the gids of the target
    gids = circuit.gids(target)

    # Load the morphologies with brain (faster than BBPSDK)
    circuit.load_morphologies(gids, circuit.Coordinates.local)
    uris = circuit.morphology_uris(gids)[0]
    brain.neuron.Morphology(uris)
    morphologies = circuit.load_morphologies(gids, circuit.Coordinates.local)

    # A list that will keep the data of all the neurons from the target
    target_data = list()

    # Filtering
    print('Filtering circuit')
    for i, gid, neuron in zip(range(len(gids) + 1), gids, neurons):

        # Position
        position = neuron.position()

        # Layer
        layer = neuron.layer()

        # Mean radius
        mean_radius = morphologies[i].soma().mean_radius()

        # Minimum and maximum radii
        min_radius, max_radius = core.utilities.get_minimum_and_maximum_radii(
            morphologies[i].soma().profile_points())

        # Morphology type
        morphology_type = neuron.morphology_type().name()

        # Morphology label
        morphology_label = neuron.morphology_label()

        # Column
        column = neuron.column()

        neuron = core.Neuron(gid=,mtype=,mlabel=,layer=,position=,orientation=)

        # Compose the neuron data
        neuron_data = '%s %s %s %s %s %s %s %s %s %s %s %s' % \
                      (str(gid),
                       str(random.randint(1, number_tags)),
                       str(position.x()),
                       str(position.y()),
                       str(position.z()),
                       str(min_radius),
                       str(mean_radius),
                       str(max_radius),
                       str(morphology_type),
                       str(morphology_label),
                       str(column),
                       str(layer))

        # add the neuron data to the list
        target_data.append(neuron)

    # Sample the target randomly
    filtered_target_data = random.sample(set(target_data),
        int((len(target_data) * percent / 100.0)))

    # Write the NeuroRender file
    core.write_neurorender_config(filtered_target_data)










    for i in range(1, ntags + 1):
        voxelization_target_output = \
            open("%s/Tag%d_%s-%dp.list" %
                 (output, i, target,int(percent)), 'w')
        default_target_output = open("%s/Tag%d_%s-%dp.target" %
                                     (output, i, target, int(percent)), 'w')
        default_target_output.write(
            "Target Cell Layer%d_%s-%dp \n" % (i, target, int(percent)))
        default_target_output.write("{\n")
        gids_string = ''
        for data in all_layers_data:
            if i == data.split(' ')[1]:
                gids_string += "a%d " % int(data.split(' ')[0])
                voxelization_target_output.write("%s\n" % data)
        default_target_output.write(gids_string)
        default_target_output.write("\n}\n")
        voxelization_target_output.close()
        default_target_output.close()
    voxelization_target_output = open("%s/Random_%s-%dp.list" %
                                      (output, target, int(percent)), 'w')

    default_target_output = open(
        "%s/Random_%s-%dp.target" % (output, target, int(percent)), 'w')
    default_target_output.write(
        "Target Cell Random_%s-%dp \n" % (target, int(percent)))
    default_target_output.write("{\n")
    gids_string = ''
    for data in all_layers_data:
        gids_string += "a%d " % int(data.split(' ')[0])
        voxelization_target_output.write("%s\n" % data)
    default_target_output.write(gids_string)
    default_target_output.write("\n}\n")
    voxelization_target_output.close()
    default_target_output.close()


################################################################################
# @run
################################################################################
def run():
    """Run the script.
    """

    # parse the arguments
    argument_list = parse_command_line_arguments()

    # create targets
    create_targets(argument_list.circuit_config,
                   argument_list.target,
                   float(argument_list.percent),
                   argument_list.output,
                   int(argument_list.number_tags))


################################################################################
# @__main__
################################################################################
if __name__ == "__main__":
    run()