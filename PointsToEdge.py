# -*- coding: utf-8 -*-

"""
***************************************************************************
    PointToEdge was created from:

    PointsToPaths.py
    ---------------------
    Date                 : April 2014
    Copyright            : (C) 2014 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy modified by Quentin Rossy'
__date__ = 'April 2014'
__copyright__ = '(C) 2014, Alexander Bruy & (C) 2019, Quentin Rossy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from datetime import datetime
from qgis.PyQt.QtCore import QVariant, QDateTime
from qgis.PyQt.QtGui import QColor
from qgis.core import (QgsFeature,
                       QgsFeatureSink,
                       QgsFields,
                       QgsField,
                       QgsGeometry,
                       QgsDistanceArea,
                       QgsPointXY,
                       QgsLineString,
                       QgsWkbTypes,
                       QgsFeatureRequest,
                       QgsProcessingException,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       QgsProcessingFeatureSource,
                       QgsProcessing,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFolderDestination,
                       QgsMessageLog,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingUtils)

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from .visualist_alg import VisualistAlgorithm
from .utils import renderers

#Convenient function to debug
NAME = "Visualist"
log = lambda m: QgsMessageLog.logMessage(m, NAME)

class PointsToEdge(VisualistAlgorithm):

    INPUT = 'INPUT'
    GROUP_FIELD = 'GROUP_FIELD'
    ORDER_FIELD = 'ORDER_FIELD'
    FIELDS = 'FIELDS'
    DATE_FORMAT = 'DATE_FORMAT'
    OUTPUT_LINE = 'OUTPUT_LINE'
    OUTPUT_POINT = 'OUTPUT_POINT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'pointstoedge'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              self.tr('Input point layer'), [QgsProcessing.TypeVectorPoint]))
        self.addParameter(QgsProcessingParameterField(self.GROUP_FIELD,
                                                      self.tr('Group field'), parentLayerParameterName=self.INPUT))
        self.addParameter(QgsProcessingParameterField(self.ORDER_FIELD,
                                                      self.tr('Order field'), parentLayerParameterName=self.INPUT))
        self.addParameter(QgsProcessingParameterString(self.DATE_FORMAT,
                                                       self.tr('Order date format (i.e. %Y-%m-%dT%H:%M:%S.%f)'), optional=True))
        self.addParameter(QgsProcessingParameterField(self.FIELDS,
                                                      self.tr('Fields to include'),
                                                      parentLayerParameterName=self.INPUT,
                                                      allowMultiple=True, optional=True))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT_LINE,
                                                        self.tr('Edge Map'),
                                                        QgsProcessing.TypeVectorLine))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT_POINT,
                                                        self.tr('End points Map'),
                                                        QgsProcessing.TypeVectorPoint))

    def addFields(self, source, fields, prefix, field_names, order_field_def=None):
        if order_field_def is not None:
            order_field = QgsField(order_field_def)
            order_field.setName(prefix)
            fields.append(order_field)
        self.field_indices = []
        for field_name in field_names:
            field_index = source.fields().lookupField(field_name)
            if field_index < 0:
                feedback.reportError(self.tr('Invalid field name {}').format(field_name))
                continue
            field = source.fields()[field_index]
            name = field.displayName()
            field.setName("{0}_{1}".format(prefix,name))
            fields.append(field)
            self.field_indices.append(field_index)

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        source = self.parameterAsSource(parameters, self.INPUT, context)
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        group_field_name = self.parameterAsString(parameters, self.GROUP_FIELD, context)
        order_field_name = self.parameterAsString(parameters, self.ORDER_FIELD, context)
        date_format = self.parameterAsString(parameters, self.DATE_FORMAT, context)
        group_field_index = source.fields().lookupField(group_field_name)
        order_field_index = source.fields().lookupField(order_field_name)
        field_names = self.parameterAsFields(parameters, self.FIELDS, context)

        if group_field_index >= 0:
            group_field_def = source.fields().at(group_field_index)
        else:
            group_field_def = None
        order_field_def = source.fields().at(order_field_index)

        #Create output for lines
        fields = QgsFields()
        self.addFields(source, fields, 'start_order', field_names, order_field_def)
        self.addFields(source, fields, 'end_order', field_names, order_field_def)
        fields.append(QgsField('COUNT', QVariant.LongLong))

        output_wkb = QgsWkbTypes.LineString
        if QgsWkbTypes.hasM(source.wkbType()):
            output_wkb = QgsWkbTypes.addM(output_wkb)
        if QgsWkbTypes.hasZ(source.wkbType()):
            output_wkb = QgsWkbTypes.addZ(output_wkb)

        (self.sink, self.dest_id) = self.parameterAsSink(parameters, self.OUTPUT_LINE, context,
                                                fields, output_wkb, source.sourceCrs())
        if self.sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT_LINE))

        #Create output for Points
        fields_point = QgsFields()
        fields_point.append(QgsField("fid", QVariant.Int, "int", 9, 0))
        self.addFields(source, fields_point, 'end_order', field_names)
        fields_point.append(QgsField("COUNT", QVariant.LongLong))
        fields_point.append(QgsField("COUNT_IN", QVariant.LongLong))
        fields_point.append(QgsField("COUNT_OUT", QVariant.LongLong))

        (self.sink_point, self.dest_id_point) = self.parameterAsSink(parameters, self.OUTPUT_POINT, context,
                                               fields_point, source.wkbType(), source.sourceCrs(), QgsFeatureSink.RegeneratePrimaryKey)
        if self.sink_point is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT_POINT))

        #Compute the lines
        points = dict()
        features = source.getFeatures(QgsFeatureRequest(), QgsProcessingFeatureSource.FlagSkipGeometryValidityChecks)
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        for current, f in enumerate(features):
            if feedback.isCanceled(): return {}

            if not f.hasGeometry(): continue

            point = f.geometry().asPoint()
            if group_field_index >= 0:
                group = f[group_field_index]
            else:
                group = 1
            order = f[order_field_index]
            if date_format != '':
                if isinstance(order, QDateTime):
                    pass
                else:
                    try:
                        order = datetime.strptime(str(order), date_format)
                    except ValueError as ve:
                        feedback.reportError(self.tr('Invalid format {}').format(ve))
                        return {}
            data = [order, point]
            for indice in self.field_indices:
                data.append(f[indice])
            if group in points:
                points[group].append(data)
            else:
                points[group] = [data]

            feedback.setProgress(int(current * total))
        feedback.setCurrentStep(1)

        #Create the features
        current = 0
        total = 100.0 / len(points) if points else 1
        edge_ids = {}
        end_points = {}
        self.point_id = 0
        for group, vertices in points.items():
            if feedback.isCanceled(): return {}
            feedback.setProgress(int(current * total))
            # log("attrs: {}".format(vertices))
            vertices.sort(key=lambda x: (x[0] is None, x[0]))
            for i in range(len(vertices)-1):
                if feedback.isCanceled(): return {}
                start_id = vertices[i][1].asWkt()
                end_id = vertices[i+1][1].asWkt()
                edge_id = start_id+"-"+end_id

                if edge_id in edge_ids:
                    f = edge_ids[edge_id]
                    count_index = 2*(len(self.field_indices)+1)
                    count = f.attribute(count_index)+1
                    f.setAttribute(count_index,count)
                else:
                    f = QgsFeature()
                    attrs = []
                    attrs.append(vertices[i][0])               #Add Order begin
                    for j in range(len(self.field_indices)):        #Add Attrs for begin
                        attrs.append(vertices[i][j+2])         # +2 ignore order and point
                    attrs.append(vertices[i+1][0])             #Add Order end
                    for j in range(0, len(self.field_indices)):     #Add Attrs for end
                        attrs.append(vertices[i+1][j+2])       # +2 ignore order and point
                    attrs.append(1)  #Count = 1
                    f.setAttributes(attrs)
                    line = [vertices[i][1], vertices[i+1][1]]
                    geom = QgsGeometry()
                    f.setGeometry(QgsGeometry(geom.fromPolylineXY(line)))
                    edge_ids[edge_id] = f

                self.updatePoints(start_id, end_points, vertices[i], 'start')
                self.updatePoints(end_id, end_points, vertices[i+1], 'end')

                current += 1
                feedback.setProgress(int(current * total))
        for id in edge_ids:
            if feedback.isCanceled(): return {}
            self.sink.addFeature(edge_ids[id], QgsFeatureSink.FastInsert)
        for id in end_points:
            if feedback.isCanceled(): return {}
            self.sink_point.addFeature(end_points[id], QgsFeatureSink.FastInsert)

        return {self.OUTPUT_LINE: self.dest_id}

    def updatePoints(self, id, end_points, vertice, type):
        if id in end_points:
            f_point = end_points[id]
            count_index = (len(self.field_indices)+1)
            count = f_point.attribute(count_index)+1
            f_point.setAttribute(count_index,count)
            if type == 'start':
                count_index = (len(self.field_indices)+3)
                count = f_point.attribute(count_index)+1
                f_point.setAttribute(count_index,count)
            else:
                count_index = (len(self.field_indices)+2)
                count = f_point.attribute(count_index)+1
                f_point.setAttribute(count_index,count)
        else:
            f_point = QgsFeature()
            attrs_point = [self.point_id]
            for j in range(0, len(self.field_indices)):
                attrs_point.append(vertice[j+2])
            if type == 'start':
                attrs_point += [1,0,1]
            else:
                attrs_point += [1,1,0]
            f_point.setAttributes(attrs_point)
            geom = QgsGeometry()
            f_point.setGeometry(geom.fromPointXY(vertice[1]))
            end_points[id] = f_point
            self.point_id += 1

    def postProcessAlgorithm(self, context, feedback):
        """
        PostProcessing Tasks to define the Symbology
        """
        output = QgsProcessingUtils.mapLayerFromString(self.dest_id_point, context)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "utils/styles/EdgesPoints.qml")
        feedback.pushInfo('Load symbology from file: {})'.format(path))
        output.loadNamedStyle(path)
        output.triggerRepaint()

        output = QgsProcessingUtils.mapLayerFromString(self.dest_id, context)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "utils/styles/Edges.qml")
        feedback.pushInfo('Load symbology from file: {})'.format(path))
        output.loadNamedStyle(path)
        output.triggerRepaint()
        return {self.OUTPUT_LINE: self.dest_id}
