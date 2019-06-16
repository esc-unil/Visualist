# -*- coding: utf-8 -*-

"""
***************************************************************************
    PointToFlow was created from:

    edgebundlingProviderPlugin.py
    ---------------------
    Date                 : January 2018
    Copyright            : (C) 2018 by Anita Graser
    Email                : anitagraser@gmx.at
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Anita Graser modified by Quentin Rossy'
__date__ = 'January 2018'
__copyright__ = '(C) 2018, Anita Graser & (C) 2019, Quentin Rossy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os, processing
from tempfile import gettempdir

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon

from qgis.core import (QgsField,
                       QgsFeature,
                       QgsFeatureSink,
                       QgsFeatureRequest,
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterDefinition,
                       QgsMessageLog,
                       QgsProcessingUtils
                      )

from .edgebundlingUtils import Edge, EdgeCluster
from .visualist_alg import VisualistAlgorithm
from .utils import renderers

pluginPath = os.path.dirname(__file__)

#Convenient function to debug
NAME = "Visualist"
log = lambda m: QgsMessageLog.logMessage(m, NAME)

class EdgesToFlow(VisualistAlgorithm):

    INPUT = 'INPUT'
    CLUSTER_FIELD = 'CLUSTER_FIELD'
    WEIGHT_FIELD = 'WEIGHT_FIELD'
    INITIAL_STEP_SIZE = 'INITIAL_STEP_SIZE'
    MAX_DISTANCE = 'MAX_DISTANCE'
    COMPATIBILITY = 'COMPATIBILITY'
    CYCLES = 'CYCLES'
    ITERATIONS = 'ITERATIONS'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return "flowmap"

    def postProcessAlgorithm(self, context, feedback):
        """
        PostProcessing Tasks to define the Symbology
        """
        output = QgsProcessingUtils.mapLayerFromString(self.dest_id, context)
        if self.doRenderer:
            r = renderers.MapRender(output)
            r.prop('OVERLAP_COUNT', type=renderers.LINE)

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "utils/styles/Flow.qml")
        feedback.pushInfo('Load symbology from file: {})'.format(path))
        output.loadNamedStyle(path)
        output.triggerRepaint()
        return {self.OUTPUT: self.dest_id}

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT,
            self.tr("Input layer"),
            [QgsProcessing.TypeVectorLine]))


        self.addParameter(QgsProcessingParameterField(
            self.CLUSTER_FIELD,
            self.tr("Cluster field"),
            type=QgsProcessingParameterField.Any,
            parentLayerParameterName=self.INPUT,
            allowMultiple=False, defaultValue=None, optional=True))

        self.addParameter(QgsProcessingParameterField(
            self.WEIGHT_FIELD,
            self.tr("Weight field"),
            type=QgsProcessingParameterField.Any,
            parentLayerParameterName=self.INPUT,
            allowMultiple=False, defaultValue=None, optional=True))

        init_step_size = QgsProcessingParameterNumber(
            self.INITIAL_STEP_SIZE,
            self.tr("Initial step size (try 0.001 for GPS data or 100 for projected data)"),
            QgsProcessingParameterNumber.Double,
            0.001)
        init_step_size.setFlags(init_step_size.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(init_step_size)

        compatibility = QgsProcessingParameterNumber(
            self.COMPATIBILITY,
            self.tr("Compatibility (a low value increases the grouping of paths)"),
            QgsProcessingParameterNumber.Double,
            0.6)
        compatibility.setFlags(compatibility.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(compatibility)

        cycles = QgsProcessingParameterNumber(
            self.CYCLES,
            self.tr("Cycles (increases the number of line breaks)"),
            QgsProcessingParameterNumber.Integer,
            6)
        cycles.setFlags(cycles.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(cycles)

        iterations = QgsProcessingParameterNumber(
            self.ITERATIONS,
            self.tr("Iterations (of the force-directed layout)"),
            QgsProcessingParameterNumber.Integer,
            90)
        iterations.setFlags(iterations.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(iterations)

        max_dist = QgsProcessingParameterNumber(
            self.MAX_DISTANCE,
            self.tr("Maximum distance to merge overlapping segments"),
            type=QgsProcessingParameterNumber.Double,
            optional=True) #defaultValue=0.005,
        max_dist.setFlags(max_dist.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(max_dist)

        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT,
            self.tr("Flow Map"),
            QgsProcessing.TypeVectorLine))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        outputs = {}
        self.doRenderer = False
        # Fix geometries
        alg_params = {
            'INPUT': parameters[self.INPUT],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        if feedback.isCanceled():
            return {}

        # Explode lines
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExplodeLines'] = processing.run('native:explodelines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        if feedback.isCanceled():
            return {}

        # Remove null geometries
        alg_params = {
            'INPUT': outputs['ExplodeLines']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RemoveNullGeometries'] = processing.run('native:removenullgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        weight_field = self.parameterAsString(parameters, self.WEIGHT_FIELD, context)
        cluster_field = self.parameterAsString(parameters, self.CLUSTER_FIELD, context)
        initial_step_size = self.parameterAsDouble(parameters, self.INITIAL_STEP_SIZE, context)
        max_distance = self.parameterAsDouble(parameters, self.MAX_DISTANCE, context)
        compatibility = self.parameterAsDouble(parameters, self.COMPATIBILITY, context)
        cycles = self.parameterAsInt(parameters, self.CYCLES, context)
        iterations = self.parameterAsInt(parameters, self.ITERATIONS, context)
        source = self.parameterAsSource(outputs['RemoveNullGeometries'], 'OUTPUT', context)

        # Create edge list
        features = source.getFeatures(QgsFeatureRequest())
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        edges = []
        for current, feat in enumerate(features):
            if feedback.isCanceled(): break
            edges.append(Edge(feat))

        # Create clusters
        fields = source.fields()
        clusters = []
        if cluster_field != '':
            # Arrange edges in clusters according to cluster-id
            labels = []
            for edge in edges:
                if feedback.isCanceled(): return {}
                labels.append(edge[cluster_field])
            feedback.pushDebugInfo(cluster_field)
            for l in range(0, max(labels) + 1):
                if feedback.isCanceled(): return {}
                clusters.append(list())
            for i, label in enumerate(labels):
                if feedback.isCanceled(): return {}
                if label >= 0:
                    clusters[label].append(edges[i])
                else:
                    clusters.append([edges[i]])
            for i, cluster in enumerate(clusters):
                if feedback.isCanceled(): return {}
                clusters[i] = EdgeCluster(cluster, initial_step_size, iterations,
                                    cycles, compatibility)
        else:
            # If clustering should not be used, create only one big cluster containing all edges
            clusters = [EdgeCluster(edges, initial_step_size, iterations,
                                    cycles, compatibility)]
        fields.append(QgsField('CLUSTER', QVariant.Int))
        cluster_index = fields.lookupField('CLUSTER')
        if max_distance > 0:
            self.doRenderer = True
            fields.append(QgsField('PATH', QVariant.Int))
            fields.append(QgsField('OVERLAP_COUNT', QVariant.Int))
            overlap_index = fields.lookupField('OVERLAP_COUNT')

        (sink, self.dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                     fields, source.wkbType(), source.sourceCrs())

        # Do edge-bundling (separately for all clusters)
        if max_distance == 0:
            feedback.setProgressText(self.tr('Compute Flow without merging lines'))
            for c, cl in enumerate(clusters):
                if feedback.isCanceled(): return {}
                if cl.E > 1:
                    cl.force_directed_eb(feedback)
            for id, cl in enumerate(clusters):
                if feedback.isCanceled(): return {}
                for e, edge in enumerate(cl.edges):
                    feat = QgsFeature()
                    feat.setGeometry(edge.geometry())
                    attr = edge.attributes()
                    attr.append(id)
                    feat.setAttributes(attr)
                    sink.addFeature(feat, QgsFeatureSink.FastInsert)
        else:
            feedback.setProgressText(self.tr('Compute Flow and try to merge lines'))
            for c, cl in enumerate(clusters):
                if feedback.isCanceled(): return {}
                if cl.E > 1:
                    cl.force_directed_eb(feedback)
                    cl.create_segments(feedback)
                    feedback.setCurrentStep(2)
                    cl.collapse_lines(max_distance, feedback)
            fid = 0
            for id, cl in enumerate(clusters):
                if feedback.isCanceled(): return {}
                for e, edge in enumerate(cl.edges):
                    segments = cl.get_segments(edge)
                    for key, segment in segments.items():
                        feat = QgsFeature()
                        feat.setGeometry(segment.geometry())
                        attr = edge.attributes()
                        path_id = attr[0]
                        attr[0] = fid
                        attr.append(id)
                        attr.append(path_id)
                        attr.append(int(segment.get_agg_weight())) #Overlap count
                        feat.setAttributes(attr)
                        sink.addFeature(feat, QgsFeatureSink.FastInsert)
                        fid += 1

        return {self.OUTPUT: self.dest_id}
