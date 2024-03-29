# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Visualist
                                 A QGIS plugin
 Plugin for Crime Analysts
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-04-15
        copyright            : (C) 2019 by Quentin Rossy
        email                : quentin.rossy@unil.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Quentin Rossy'
__date__ = '2019-04-15'
__copyright__ = '(C) 2019 by Quentin Rossy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os, math

import plotly as plt
import plotly.graph_objs as go
from plotly import tools

from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView
from qgis.PyQt.QtWidgets import (QDialog,
                        QWidget,
                        QVBoxLayout,
                        QLabel)

from qgis.utils import iface
from qgis.core import (QgsApplication,
                       QgsFeatureRequest,
                       QgsFeature,
                       QgsDistanceArea,
                       QgsProject,
                       QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterField,
                       QgsProcessingOutputNumber,
                       QgsProcessingParameterExtent,
                       QgsSpatialIndex,
                       QgsExpression)

from .visualist_alg import VisualistAlgorithm

class WebDialog(QDialog):

    def __init__(self, parent=None, title='WebDialog'):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.html_file = None
        layout = QVBoxLayout()
        layout.setMargin(0)
        layout.setSpacing(6)
        self.WebV = QWebView()
        layout.addWidget(self.WebV)
        self.setLayout(layout)

    def setHTML(self, file_path):
        self.html_file = file_path
        self.WebV.load(QUrl.fromLocalFile(self.html_file))


class DistanceAnalysis(VisualistAlgorithm):

    INPUT = 'INPUT'
    OUTPUT_HTML_FILE = 'OUTPUT_HTML_FILE'
    SPLIT = 'SPLIT'
    EVENT_ID = 'EVENT_ID'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'distanceanalysis'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              self.tr('Points'), [QgsProcessing.TypeVectorPoint]))

        self.addParameter(QgsProcessingParameterField(self.SPLIT,
                                            self.tr('Field to split layer'),
                                            type=QgsProcessingParameterField.String,
                                            parentLayerParameterName=self.INPUT,
                                            allowMultiple=False, defaultValue=None, optional=True))
        self.addParameter(QgsProcessingParameterField(self.EVENT_ID,
                                    self.tr('Field that contains event\'s ID'),
                                    type=QgsProcessingParameterField.Any,
                                    parentLayerParameterName=self.INPUT,
                                    allowMultiple=False, defaultValue=None, optional=True))

        self.addParameter(QgsProcessingParameterFileDestination(self.OUTPUT_HTML_FILE, self.tr('Distance analysis'), self.tr('HTML files (*.html)'), None, True))

    def postProcessAlgorithm(self, context, feedback):
        """
        PostProcessing Tasks to load html
        """
        dial = WebDialog(iface.mainWindow(), self.displayName())
        dial.setHTML(self.path)
        dial.show()

        return self.output

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        field_split = self.parameterAsString(parameters, self.SPLIT, context)
        if field_split:
            field_split_index = source.fields().lookupField(field_split)
        field_event = self.parameterAsString(parameters, self.EVENT_ID, context)
        if field_event:
            field_event_index = source.fields().lookupField(field_event)

        output_file = self.parameterAsFileOutput(parameters, self.OUTPUT_HTML_FILE, context)
        self.path = output_file

        spatialIndex = QgsSpatialIndex(source, feedback)

        uniqueValues = source.uniqueValues(field_split_index)
        total = 100.0 / len(uniqueValues) if uniqueValues else 1


        distArea = QgsDistanceArea()
        distArea.setSourceCrs(source.sourceCrs(), context.transformContext())
        distArea.setEllipsoid(context.project().ellipsoid())

        for current, i in enumerate(uniqueValues):
            if feedback.isCanceled():
                break
            filter = '{} = {}'.format(QgsExpression.quotedColumnRef(field_split), QgsExpression.quotedValue(i))
            req = QgsFeatureRequest().setFilterExpression(filter).setSubsetOfAttributes([field_event_index])
            features = source.getFeatures(req)
            for current, inFeat in enumerate(features):
                if feedback.isCanceled():
                    break
                inGeom = inFeat.geometry()
                inID = str(inFeat[field_event])
                featList = spatialIndex.nearestNeighbor(inGeom.asPoint(), 1)

        self.output = {self.OUTPUT_HTML_FILE: output_file}
        return self.output
