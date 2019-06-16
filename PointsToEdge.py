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
                       QgsMessageLog)

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from .visualist_alg import VisualistAlgorithm

#Convenient function to debug
NAME = "Visualist"
log = lambda m: QgsMessageLog.logMessage(m, NAME)

class PointsToEdge(VisualistAlgorithm):

    INPUT = 'INPUT'
    GROUP_FIELD = 'GROUP_FIELD'
    ORDER_FIELD = 'ORDER_FIELD'
    FIELDS = 'FIELDS'
    DATE_FORMAT = 'DATE_FORMAT'
    OUTPUT = 'OUTPUT'
    OUTPUT_TEXT_DIR = 'OUTPUT_TEXT_DIR'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'pointstoedge'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              self.tr('Input point layer'), [QgsProcessing.TypeVectorPoint]))
        self.addParameter(QgsProcessingParameterField(self.GROUP_FIELD,
                                                      self.tr('Group field'), parentLayerParameterName=self.INPUT, optional=True))
        self.addParameter(QgsProcessingParameterField(self.ORDER_FIELD,
                                                      self.tr('Order field'), parentLayerParameterName=self.INPUT))
        self.addParameter(QgsProcessingParameterString(self.DATE_FORMAT,
                                                       self.tr('Order date format (i.e. %Y-%m-%dT%H:%M:%S.%f)'), optional=True))
        self.addParameter(QgsProcessingParameterField(self.FIELDS,
                                                      self.tr('Fields to include (leave empty to use all fields)'),
                                                      parentLayerParameterName=self.INPUT,
                                                      allowMultiple=True, optional=True))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Edges'), QgsProcessing.TypeVectorLine))


    def addFields(self, source, fields, prefix, field_names, order_field_def):
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

    def processAlgorithm(self, parameters, context, feedback):
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

        fields = QgsFields()
        self.addFields(source, fields, 'start_order', field_names, order_field_def)
        self.addFields(source, fields, 'end_order', field_names, order_field_def)
        fields.append(QgsField('COUNT', QVariant.LongLong))

        output_wkb = QgsWkbTypes.LineString
        if QgsWkbTypes.hasM(source.wkbType()):
            output_wkb = QgsWkbTypes.addM(output_wkb)
        if QgsWkbTypes.hasZ(source.wkbType()):
            output_wkb = QgsWkbTypes.addZ(output_wkb)

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                               fields, output_wkb, source.sourceCrs())
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        points = dict()
        features = source.getFeatures(QgsFeatureRequest(), QgsProcessingFeatureSource.FlagSkipGeometryValidityChecks)
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        for current, f in enumerate(features):
            if feedback.isCanceled():
                return {}

            if not f.hasGeometry():
                continue

            point = f.geometry().constGet().clone()
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

        feedback.setProgress(0)
        current = 0
        total = 100.0 / len(points) if points else 1
        edge_ids = {}
        for group, vertices in points.items():
            if feedback.isCanceled():
                break
            # log("attrs: {}".format(vertices))
            vertices.sort(key=lambda x: (x[0] is None, x[0]))
            for i in range(len(vertices)-1):
                edge_id = vertices[i][1].asWkt()+"-"+vertices[i+1][1].asWkt()
                if edge_id in edge_ids:
                    f = edge_ids[edge_id]
                    count_index = 2*(len(self.field_indices)+1)
                    count = f.attribute(count_index)+1
                    f.setAttribute(count_index,count)
                else:
                    f = QgsFeature()
                    attributes = []
                    attributes.append(vertices[i][0])               #Add Order begin
                    for j in range(len(self.field_indices)):        #Add Attrs for begin
                        attributes.append(vertices[i][j+2])         # +2 ignore order and point
                    attributes.append(vertices[i+1][0])             #Add Order end
                    for j in range(0, len(self.field_indices)):     #Add Attrs for end
                        attributes.append(vertices[i+1][j+2])       # +2 ignore order and point
                    attributes.append(1)                            #Count = 1
                    f.setAttributes(attributes)
                    line = [vertices[i][1], vertices[i+1][1]]
                    f.setGeometry(QgsGeometry(QgsLineString(line)))
                    edge_ids[edge_id] = f
                current += 1
                feedback.setProgress(int(current * total))
        for id in edge_ids:
            sink.addFeature(edge_ids[id], QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}
