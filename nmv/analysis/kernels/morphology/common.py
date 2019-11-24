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

# Internal imports
import nmv
import nmv.analysis
import nmv.consts


####################################################################################################
# @get_minimum_value_of_results
####################################################################################################
def get_minimum_value_of_results(results):
    """Returns the result of the minimum value for a given list of results.

    :param results:
        A given list of analysis results.
    :return:
        The result with minimum value.
    """

    # Minimum result
    minimum_result = nmv.analysis.ItemAnalysisResult

    # Find the minimum value
    current_minimum_value = nmv.consts.Math.INFINITY

    # Per result
    for result in results:

        # If the radius is less than the minimum
        if result.value < current_minimum_value:

            # Update the current minimum value
            current_minimum_value = result.value

            # Update the final result as well
            minimum_result = result

    # Return the minimum result
    return minimum_result


####################################################################################################
# @get_maximum_value_of_results
####################################################################################################
def get_maximum_value_of_results(results):
    """Returns the result of the maximum value for a given list of results.

    :param results:
        A given list of analysis results.
    :return:
        The result with maximum value.
    """

    # Maximum result
    maximum_result = nmv.analysis.ItemAnalysisResult

    # Find the maximum value
    current_maximum_value = nmv.consts.Math.SMALLEST_VALUE

    # Per result
    for result in results:

        # If the radius is greater than the minimum
        if result.value > current_maximum_value:

            # Update the current maximum value
            current_maximum_value = result.value

            # Update the final result as well
            maximum_result = result

    # Return the maximum result
    return maximum_result


####################################################################################################
# @get_total_value_of_results
####################################################################################################
def get_total_value_of_results(results):
    """Returns the sum (or the aggregated result) of a given list of results.

    :param results:
        A given list of analysis results.
    :return:
        A result with the aggregated results.
    """

    # Total result
    total_result = nmv.analysis.ItemAnalysisResult()

    # Initialize with Zero
    total_result.value = 0

    # Per result
    for i_result in results:

        # Add to the total
        total_result.value += i_result.value

    # Return the total result
    return total_result


####################################################################################################
# @get_morphology_maximum_branching_order_from_analysis_results
####################################################################################################
def get_morphology_maximum_branching_order_from_analysis_results(analysis_result):
    """Computes the maximum branching order of the morphology based on the actual computed
    values from the analysis.

    :param analysis_result:
        The resulting data from a certain analysis procedure.
    :return:
        The maximum branching order of the morphology.
    """

    maximum_branching_order = 0

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        if len(analysis_result.apical_dendrite_result) > maximum_branching_order:
            maximum_branching_order = len(analysis_result.apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            if len(basal_dendrite_result) > maximum_branching_order:
                maximum_branching_order = len(basal_dendrite_result)

    # Axon
    if analysis_result.axon_result is not None:
        if len(analysis_result.axon_result) > maximum_branching_order:
            maximum_branching_order = len(analysis_result.axon_result)

    # Return the maximum branching order
    return maximum_branching_order


####################################################################################################
# @compute_total_distribution_of_morphology
####################################################################################################
def compute_total_distribution_of_morphology(analysis_result):
    """Computes the total result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # Aggregate result of the entire morphology will be computed later
    maximum_branching_order = \
        get_morphology_maximum_branching_order_from_analysis_results(analysis_result)
    analysis_result.morphology_result = list()
    for i in range(maximum_branching_order):
        analysis_result.morphology_result.append([i + 1, 0])

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        for item in analysis_result.apical_dendrite_result:
            analysis_result.morphology_result[item[0] - 1][1] += item[1]

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            for item in basal_dendrite_result:
                analysis_result.morphology_result[item[0] - 1][1] += item[1]

    # Axon
    if analysis_result.axon_result is not None:
        for item in analysis_result.axon_result:
            analysis_result.morphology_result[item[0] - 1][1] += item[1]


####################################################################################################
# @compute_total_analysis_result_of_morphology
####################################################################################################
def compute_total_analysis_result_of_morphology(analysis_result):
    """Computes the total result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # Aggregate result of the entire morphology will be computed later
    analysis_result.morphology_result = nmv.analysis.ItemAnalysisResult

    # Initialize the value to Zero
    analysis_result.morphology_result.value = 0

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        analysis_result.morphology_result.value += analysis_result.apical_dendrite_result.value

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            analysis_result.morphology_result.value += basal_dendrite_result.value

    # Axon
    if analysis_result.axon_result is not None:
        analysis_result.morphology_result.value += analysis_result.axon_result.value


####################################################################################################
# @compute_minimum_analysis_result_of_morphology
####################################################################################################
def compute_minimum_analysis_result_of_morphology(analysis_result):
    """Computes the minimum result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        all_arbors_results.append(analysis_result.apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axon_result is not None:
        all_arbors_results.append(analysis_result.axon_result)

    # Minimum value
    minimum_value = nmv.consts.Math.INFINITY

    # Per result
    for result in all_arbors_results:

        # If the value if less than the minimum value
        if result.value < minimum_value:

            # Update the minimum value
            minimum_value = result.value

            # Update the morphology result
            analysis_result.morphology_result = result


####################################################################################################
# @compute_maximum_analysis_result_of_morphology
####################################################################################################
def compute_maximum_analysis_result_of_morphology(analysis_result):
    """Computes the maximum result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        all_arbors_results.append(analysis_result.apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axon_result is not None:
        all_arbors_results.append(analysis_result.axon_result)

    # Maximum value
    maximum_value = nmv.consts.Math.SMALLEST_VALUE

    # Per result
    for result in all_arbors_results:

        # If the value if greater than the minimum value
        if result.value > maximum_value:

            # Update the maximum value
            maximum_value = result.value

            # Update the morphology result
            analysis_result.morphology_result = result


####################################################################################################
# @compute_average_analysis_result_of_morphology
####################################################################################################
def compute_average_analysis_result_of_morphology(analysis_result):
    """Computes the average result with respect to the entire morphology skeleton from the analysis
    results of the existing arbors.

    NOTE: The morphology result is updated in the given analysis result structure.

    :param analysis_result:
        A structure that contains all the analysis results of the morphology arbors.
    """

    # A list that will contain the results of all the arbors
    all_arbors_results = list()

    # Apical dendrite
    if analysis_result.apical_dendrite_result is not None:
        all_arbors_results.append(analysis_result.apical_dendrite_result)

    # Basal dendrites
    if analysis_result.basal_dendrites_result is not None:
        for basal_dendrite_result in analysis_result.basal_dendrites_result:
            all_arbors_results.append(basal_dendrite_result)

    # Axon
    if analysis_result.axon_result is not None:
        all_arbors_results.append(analysis_result.axon_result)

    # Update the morphology result
    analysis_result.morphology_result = 0
    for result in all_arbors_results:
        analysis_result.morphology_result += result
    analysis_result.morphology_result /= len(all_arbors_results)


####################################################################################################
# @invoke_kernel
####################################################################################################
def invoke_kernel(morphology,
                  kernel,
                  aggregation_function):
    """Invoke the analysis kernel on the morphology and return the analysis result.

    :param morphology:
        A given morphology skeleton to analyze.
    :param kernel:
        Analysis kernel that will be applied on the morphology.
    :param aggregation_function:
        The function that will aggregate the entire morphology analysis result from the
        individual arbors, for example minimum, maximum, average or total.
    :return:
        The analysis results as an @MorphologyAnalysisResult structure.
    """

    # Apply the analysis operation to the morphology
    analysis_result = nmv.analysis.apply_analysis_operation_to_morphology(*[morphology, kernel])

    # Update the aggregate morphology result from the arbors
    aggregation_function(analysis_result)

    # Return the analysis result of the entire morphology
    return analysis_result


####################################################################################################
# @get_analysis_distributions
####################################################################################################
def get_analysis_distributions(morphology,
                               kernel):
    """Invoke the analysis kernel on the morphology and return the distribution in a form of list.

    :param morphology:
        A given morphology skeleton to analyze.
    :param kernel:
        Analysis kernel that will be applied on the morphology.
    :return:
        The analysis distribution as lists. The format of these lists are only known within the
        section function and the morphology function.
    """

    # Apply the analysis operation to the morphology and return the resulting lists
    return nmv.analysis.apply_analysis_operation_to_morphology(*[morphology, kernel])
