# -*- coding: utf-8 -*-

"""
***************************************************************************
    PointsInPolygon.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant


from qgis.core import (QgsApplication,
                       QgsGeometry,
                       QgsFeatureSink,
                       QgsFeatureRequest,
                       QgsFeature,
                       QgsField,
                       QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterString,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingUtils,
                       QgsSpatialIndex)

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm

from .utils import renderers

class PointsInPolygon(QgisAlgorithm):
    dest_id = None  # Save a reference to the output layer id

    POLYGONS = 'POLYGONS'
    POINTS = 'POINTS'
    OUTPUT = 'OUTPUT'
    FIELD = 'FIELD'
    WEIGHT = 'WEIGHT'
    MULTIPLIER = 'MULTIPLIER'

    def icon(self):
        iconName = 'choropleth.png'
        return QIcon(":/plugins/visualist/icons/" + iconName)

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'Cartography'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.POLYGONS,
                                                              self.tr('Polygons'), [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterFeatureSource(self.POINTS,
                                                              self.tr('Points'), [QgsProcessing.TypeVectorPoint]))
        self.addParameter(QgsProcessingParameterField(self.WEIGHT,
                                                      self.tr('Weight field'), parentLayerParameterName=self.POLYGONS,
                                                      optional=True))
        self.addParameter(QgsProcessingParameterNumber(self.MULTIPLIER,
                                                      self.tr('Multiplier (default is %)'),
                                                      optional=True,
                                                      defaultValue=100))
        self.addParameter(QgsProcessingParameterString(self.FIELD,
                                                       self.tr('Count field name'), defaultValue='NUMPOINTS'))
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Choropleth Map'), QgsProcessing.TypeVectorPolygon))

    def name(self):
        return 'countpointsinpolygon'

    def displayName(self):
        return self.tr('Choropleth Map')

    def postProcessAlgorithm(self, context, feedback):
        """
        PostProcessing Tasks to define the Symbology
        """
        output = QgsProcessingUtils.mapLayerFromString(self.dest_id, context)
        r = renderers.MapRender(output)
        r.choropleth(self.field_name)

        return {self.OUTPUT: self.dest_id}

    def processAlgorithm(self, parameters, context, feedback):
        poly_source = self.parameterAsSource(parameters, self.POLYGONS, context)
        if poly_source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.POLYGONS))

        point_source = self.parameterAsSource(parameters, self.POINTS, context)
        if point_source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.POINTS))

        weight_field = self.parameterAsString(parameters, self.WEIGHT, context)
        weight_field_index = -1
        if weight_field:
            weight_field_index = poly_source.fields().lookupField(weight_field)

        multiplier = self.parameterAsDouble(parameters, self.MULTIPLIER, context)

        field_name = self.parameterAsString(parameters, self.FIELD, context)
        self.field_name = field_name

        fields = poly_source.fields()
        if fields.lookupField(field_name) < 0:
            fields.append(QgsField(field_name, QVariant.LongLong))
            if weight_field:
                fields.append(QgsField(field_name+'_WEIGHTED', QVariant.LongLong))
        field_index = fields.lookupField(field_name)

        (sink, self.dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                               fields, poly_source.wkbType(), poly_source.sourceCrs(), QgsFeatureSink.RegeneratePrimaryKey)
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        features = poly_source.getFeatures()
        total = 100.0 / poly_source.featureCount() if poly_source.featureCount() else 0
        for current, polygon_feature in enumerate(features):
            if feedback.isCanceled():
                break

            count = 0
            output_feature = QgsFeature()
            if polygon_feature.hasGeometry():
                geom = polygon_feature.geometry()
                engine = QgsGeometry.createGeometryEngine(geom.constGet())
                engine.prepareGeometry()
                count = 0
                request = QgsFeatureRequest().setFilterRect(geom.boundingBox()).setDestinationCrs(poly_source.sourceCrs(), context.transformContext())
                for point_feature in point_source.getFeatures(request):
                    if feedback.isCanceled():
                        break
                    if engine.contains(point_feature.geometry().constGet()):
                        count += 1
                output_feature.setGeometry(geom)
            attrs = polygon_feature.attributes()
            attrs.append(count)
            if weight_field_index >= 0:
                weight = polygon_feature[weight_field_index]
                if weight == None or weight == 0:
                    weighted_count = 0
                    feedback.pushInfo('Error with feature {} : no value for weight field'.format(polygon_feature.id()))
                else:
                    weighted_count = (count*multiplier)/float(weight)
                    attrs.append(weighted_count)
            output_feature.setAttributes(attrs)
            sink.addFeature(output_feature, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(current * total))

        return {self.OUTPUT: self.dest_id}