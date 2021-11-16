#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#-----------------------------------------------------------
#
# Custom renderer functions for maps
#
# Copyright (C) 2013  Quentin Rossy
#
#-----------------------------------------------------------


import os, math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *

#Convenient function to debug
log = lambda m: QgsMessageLog.logMessage(m, "Visualist")

POINT = 'point'
LINE = 'line'

class MapRender(object):

    def __init__(self, layer):
        self.l = layer
        self.prov = self.l.dataProvider()

    def cat(self, cntField, groups, colors, name, labelField=None, type=POINT, color=Qt.black, trans=0.7):
        labelField = cntField if labelField is None else labelField

        l = []
        for group in groups:
            color = colors[group]
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.Line) if type == LINE else QgsSymbol.defaultSymbol(QgsWkbTypes.Point)
            symbol.setColor(color)
            symbol.setOpacity(trans)
            self.setDataDefinedSize(symbol, cntField)
            if type == POINT:
                sl = symbol.symbolLayer(0)
                sl.setBorderColor(Qt.white)
            l.append(QgsRendererCategory(group, symbol, group))
        myRenderer = QgsCategorizedSymbolRenderer(name, l)

        self.l.setRenderer(myRenderer)
        self.setLabels(labelField)
        return myRenderer

    def setDataDefinedSize(self, symbol, field, type):
        min = None
        max = 0
        for feature in self.l.getFeatures():
            val = feature[field]
            if min is None:
                min = val
                max = val
            elif val < min:
                min = val
            elif val > max:
                max = val
        if type == LINE:
            strExp = "coalesce(0.5*scale_linear("+field+", "+str(min)+", "+str(max)+", 1, 10), 0)"
            prop = QgsProperty().fromExpression(strExp)
            symbol.setDataDefinedWidth(prop)
        else:
            if min == 0:
                minScale = 0
                maxScale = 20
            else:
                maxScale = 20.0
                minScale = (maxScale*math.sqrt(min))/math.sqrt(max)
                if minScale < 1:
                    minScale = 1
                    maxScale = math.sqrt(max)/math.sqrt(min)
            # strExp = "coalesce(scale_linear(sqrt("+field+"), "+str(math.sqrt(min))+", "+str(math.sqrt(max))+", "+str(minScale)+", "+str(maxScale)+"), 0)"
            strExp = "coalesce(scale_exp("+field+", "+str(min)+", "+str(max)+", "+str(minScale)+", "+str(maxScale)+", 0.5), 0)"
            prop = QgsProperty().fromExpression(strExp)
            symbol.setDataDefinedSize(prop)
        # prop.setField(field)


    def prop(self, cntField, labelField=None, type=POINT, color=Qt.black, trans=0.7):
        labelField = cntField if labelField is None else labelField
        s = QgsSymbol.defaultSymbol(1) if type == LINE else QgsSymbol.defaultSymbol(0)
        myRenderer = QgsSingleSymbolRenderer(s)
        self.setDataDefinedSize(s, cntField, type)
        myRenderer.symbol().setColor(color)
        myRenderer.symbol().setOpacity(trans)
        # if type == POINT:
        #     l = s.symbolLayer(0)
        #     l.setColor(Qt.white)
        # myRenderer.setScaleMethod(QgsSymbol.ScaleArea) #QgsSymbol.ScaleArea
        self.l.setRenderer(myRenderer)
        self.setLabels(labelField)
        return myRenderer

    def choropleth(self, cntField, classes=7, labelField=None, mode=QgsGraduatedSymbolRenderer.Jenks):
        labelField = cntField if labelField is None else labelField

        props = {}
        props["outline_color"] ="255,255,255,255"
        props["outline_style"] ="solid"
        props["outline_width"] ="0.26"
        props["outline_width_unit"] ="MM"

        renderer = QgsGraduatedSymbolRenderer()
        renderer.setSourceSymbol(QgsFillSymbol.createSimple(props))
        renderer.setClassAttribute(cntField)
        renderer.setClassificationMethod(QgsClassificationJenks())
        renderer.setSourceColorRamp(QgsGradientColorRamp(QColor(230,230,230), QColor(50,50,50)))
        renderer.setGraduatedMethod(QgsGraduatedSymbolRenderer.GraduatedColor)
        renderer.updateClasses(self.l, classes)

        self.setLabels(labelField, filter=0)
        self.l.setRenderer(renderer)

        return renderer

    def nnclusters(self, cntField, classes=7, labelField=None, mode=QgsGraduatedSymbolRenderer.Jenks):
        labelField = cntField if labelField is None else labelField

        props = {}
        props["outline_color"] ="0,0,0,0"
        props["outline_style"] ="solid"
        props["outline_width"] ="2"
        props["outline_width_unit"] ="MM"

        renderer = QgsGraduatedSymbolRenderer()
        renderer.setSourceSymbol(QgsFillSymbol.createSimple(props))
        renderer.setClassAttribute(cntField)
        renderer.setClassificationMethod(QgsClassificationJenks())
        renderer.setSourceColorRamp(QgsGradientColorRamp(QColor(230,230,230), QColor(50,50,50)))
        renderer.setGraduatedMethod(QgsGraduatedSymbolRenderer.GraduatedColor)
        renderer.updateClasses(self.l, classes)

        self.setLabels(labelField, filter=0)
        self.l.setRenderer(myRenderer)
        return myRenderer

    def choropleth2(self, cntField, labelField=None):
        labelField = cntField if labelField is None else labelField
        fieldIndex = self.l.fields().indexFromName(cntField)
        minimum = self.prov.minimumValue( fieldIndex )
        maximum = self.prov.maximumValue( fieldIndex )
        if str(minimum) == "NULL" or str(maximum) == "NULL":
            (minimum, maximum) = (0, 0)
#            log(str(minimum)+" "+str(maximum))
        numberOfClasses=7
        myRangeList = []
        delta = ( maximum - minimum ) / numberOfClasses
        for i in range(0,numberOfClasses):
            myMin = minimum + delta * i
            myMax = minimum + delta * ( i + 1 )
            # if i != 0: myMin += 1
            if i == numberOfClasses-1:
                myMax = maximum
            elif delta > 10: myMax -= 1
            myLabel = "%.0f - %.0f" % (myMin,myMax)
            s = 200
            myColour = QColor(s-s*i/numberOfClasses, s-s*i/numberOfClasses, s-s*i/numberOfClasses)
            mySymbol = QgsSymbol.defaultSymbol(QgsWkbTypes.MultiPolygon)
            mySymbol.setColor(myColour)
            l = mySymbol.symbolLayer(0)
            l.setBorderColor(Qt.white)
            mySymbol.setOpacity(1)
            myRange1 = QgsRendererRange(myMin,myMax,mySymbol,myLabel)
            myRangeList.append(myRange1)
        myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
        myRenderer.setMode(QgsGraduatedSymbolRenderer.Jenks)
        myRenderer.setClassAttribute(cntField)
        self.setLabels(labelField)
        self.l.setRenderer(myRenderer)
        return myRenderer

    def zscore(self, cntField):
        fieldIndex = self.l.fields().indexFromName(cntField)
        minimum = self.prov.minimumValue( fieldIndex )
        maximum = self.prov.maximumValue( fieldIndex )
        if not minimum < -2.576:
            minimum = -2.576
        if not maximum > 2.576:
            maximum = 2.576
        zstep = [minimum, -2.576, -1.960, -1.645, -0.674, 0, 0,
                  0.674, 1.645, 1.960, 2.576, maximum]
        colors=[QColor(103,0,31),
                QColor(178,24,43),
                QColor(214,96,77),
                QColor(244,165,130),
                QColor(253,219,199),
                QColor(247,247,247),
                QColor(209,229,240),
                QColor(146,197,222),
                QColor(67,147,195),
                QColor(33,102,172),
                QColor(5,48,97)]
        myRangeList = []
        for i in range(len(colors)):
            myMin = zstep[i]
            myMax = zstep[i+1]
            myLabel = "%.3f - %.3f" % (myMin,myMax)
            mySymbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
            mySymbol.setColor(colors[len(colors)-i-1])
            myRange1 = QgsRendererRange(myMin,myMax,mySymbol,myLabel)
            myRangeList.append(myRange1)
        myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
        myRenderer.setClassificationMethod(QgsClassificationEqualInterval())
        myRenderer.setClassAttribute(cntField)
        self.l.setRenderer(myRenderer)
        return myRenderer

    def setLabels(self, field, filter=1):
        Labelqml = "<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>"\
            "<qgis labelsEnabled=\"1\" version=\"3.4.6-Madeira\" styleCategories=\"Labeling\">"\
            "  <labeling type=\"simple\">"\
            "    <settings>"\
            "      <text-style fontSize=\"8\" fontWeight=\"50\" textColor=\"0,0,0,255\" blendMode=\"0\" fontLetterSpacing=\"0\" fontUnderline=\"0\" previewBkgrdColor=\"#ffffff\" fontWordSpacing=\"0\" isExpression=\"0\" useSubstitutions=\"0\" fontFamily=\"Arial\" fontStrikeout=\"0\" multilineHeight=\"1\" fontSizeMapUnitScale=\"3x:0,0,0,0,0,0\" fontItalic=\"0\" fontCapitals=\"0\" namedStyle=\"Normal\" textOpacity=\"1\" fontSizeUnit=\"Point\" fieldName=\""+field+"\">"\
            "        <text-buffer bufferColor=\"255,255,255,255\" bufferSize=\"0.8\" bufferOpacity=\"1\" bufferDraw=\"1\" bufferJoinStyle=\"128\" bufferSizeUnits=\"MM\" bufferSizeMapUnitScale=\"3x:0,0,0,0,0,0\" bufferBlendMode=\"0\" bufferNoFill=\"1\"/>"\
            "        <background shapeRadiiY=\"0\" shapeBorderWidthUnit=\"MM\" shapeSizeUnit=\"MM\" shapeRadiiMapUnitScale=\"3x:0,0,0,0,0,0\" shapeOffsetMapUnitScale=\"3x:0,0,0,0,0,0\" shapeSVGFile=\"\" shapeBorderWidth=\"0\" shapeRotationType=\"0\" shapeFillColor=\"255,255,255,255\" shapeOffsetUnit=\"MM\" shapeOpacity=\"1\" shapeType=\"0\" shapeSizeX=\"0\" shapeJoinStyle=\"64\" shapeBorderColor=\"128,128,128,255\" shapeSizeMapUnitScale=\"3x:0,0,0,0,0,0\" shapeDraw=\"0\" shapeSizeType=\"0\" shapeBorderWidthMapUnitScale=\"3x:0,0,0,0,0,0\" shapeRotation=\"0\" shapeBlendMode=\"0\" shapeRadiiX=\"0\" shapeSizeY=\"0\" shapeOffsetY=\"0\" shapeOffsetX=\"0\" shapeRadiiUnit=\"MM\"/>"\
            "        <shadow shadowScale=\"100\" shadowRadiusAlphaOnly=\"0\" shadowBlendMode=\"6\" shadowRadiusUnit=\"MM\" shadowUnder=\"0\" shadowOffsetMapUnitScale=\"3x:0,0,0,0,0,0\" shadowOffsetAngle=\"135\" shadowRadiusMapUnitScale=\"3x:0,0,0,0,0,0\" shadowRadius=\"1.5\" shadowOffsetDist=\"1\" shadowOpacity=\"0.7\" shadowColor=\"0,0,0,255\" shadowDraw=\"0\" shadowOffsetUnit=\"MM\" shadowOffsetGlobal=\"1\"/>"\
            "        <substitutions/>"\
            "      </text-style>"\
            "      <text-format autoWrapLength=\"0\" addDirectionSymbol=\"0\" useMaxLineLengthForAutoWrap=\"1\" leftDirectionSymbol=\"&lt;\" plussign=\"0\" decimals=\"3\" multilineAlign=\"3\" placeDirectionSymbol=\"0\" wrapChar=\"\" formatNumbers=\"0\" rightDirectionSymbol=\">\" reverseDirectionSymbol=\"0\"/>"\
            "      <placement dist=\"0\" labelOffsetMapUnitScale=\"3x:0,0,0,0,0,0\" maxCurvedCharAngleOut=\"-25\" placementFlags=\"10\" priority=\"5\" repeatDistance=\"0\" centroidWhole=\"0\" distMapUnitScale=\"3x:0,0,0,0,0,0\" placement=\"1\" offsetType=\"0\" xOffset=\"0\" predefinedPositionOrder=\"TR,TL,BR,BL,R,L,TSR,BSR\" rotationAngle=\"0\" offsetUnits=\"MM\" centroidInside=\"0\" repeatDistanceUnits=\"MM\" quadOffset=\"4\" preserveRotation=\"1\" yOffset=\"0\" repeatDistanceMapUnitScale=\"3x:0,0,0,0,0,0\" fitInPolygonOnly=\"0\" distUnits=\"MM\" maxCurvedCharAngleIn=\"25\"/>"\
            "      <rendering limitNumLabels=\"0\" fontMaxPixelSize=\"10000\" mergeLines=\"0\" scaleMin=\"0\" scaleMax=\"0\" obstacleFactor=\"1\" drawLabels=\"1\" obstacle=\"1\" fontMinPixelSize=\"3\" maxNumLabels=\"2000\" displayAll=\"0\" obstacleType=\"0\" fontLimitPixelSize=\"0\" upsidedownLabels=\"0\" minFeatureSize=\"0\" labelPerPart=\"0\" zIndex=\"0\" scaleVisibility=\"0\"/>"\
            "      <dd_properties>"\
            "        <Option type=\"Map\">"\
            "          <Option type=\"QString\" value=\"\" name=\"name\"/>"\
            "          <Option type=\"Map\" name=\"properties\">"\
            "            <Option type=\"Map\" name=\"Show\">"\
            "              <Option type=\"bool\" value=\"true\" name=\"active\"/>"\
            "              <Option type=\"QString\" value=\"&quot;"+field+"&quot; > "+str(filter)+"\" name=\"expression\"/>"\
            "              <Option type=\"int\" value=\"3\" name=\"type\"/>"\
            "            </Option>"\
            "          </Option>"\
            "          <Option type=\"QString\" value=\"collection\" name=\"type\"/>"\
            "        </Option>"\
            "      </dd_properties>"\
            "    </settings>"\
            "  </labeling>"\
            "</qgis>"

        path = os.path.join(os.path.abspath( os.path.dirname( __file__)), "styles/labels.qml")
        file = open(path, 'w')
        file.writelines(Labelqml)
        file.close()
        self.l.loadNamedStyle(path)
        self.l.triggerRepaint()

        # layer_settings  = QgsPalLayerSettings()
        # text_format = QgsTextFormat()
        #
        # text_format.setFont(QFont("Arial", 8))
        # text_format.setSize(8)
        #
        # buffer_settings = QgsTextBufferSettings()
        # buffer_settings.setEnabled(True)
        # buffer_settings.setSize(0.80)
        # buffer_settings.setColor(QColor("white"))
        #
        # text_format.setBuffer(buffer_settings)
        # layer_settings.setFormat(text_format)
        #
        # layer_settings.fieldName = field
        # layer_settings.placement = 1
        # layer_settings.enabled = True
        #
        # layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
        #
        # self.l.setLabelsEnabled(True)
        # self.l.setLabeling(layer_settings)
        # self.l.triggerRepaint()
