<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Labeling|Diagrams" labelsEnabled="1" version="3.6.1-Noosa">
  <renderer-v2 type="nullSymbol"/>
  <labeling type="simple">
    <settings>
      <text-style fontCapitals="0" fontSize="8" blendMode="0" fontItalic="0" textColor="0,0,0,255" isExpression="0" fontSizeUnit="Point" fontUnderline="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="Arial" fontWeight="50" textOpacity="1" fieldName="COUNT" fontLetterSpacing="0" previewBkgrdColor="#ffffff" fontStrikeout="0" multilineHeight="1" namedStyle="Normal" fontWordSpacing="0" useSubstitutions="0">
        <text-buffer bufferDraw="1" bufferNoFill="1" bufferOpacity="1" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferSize="0.8" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0" bufferSizeUnits="MM"/>
        <background shapeSizeUnit="MM" shapeOpacity="1" shapeBorderWidth="0" shapeRotationType="0" shapeSVGFile="" shapeSizeX="0" shapeSizeY="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeJoinStyle="64" shapeRadiiY="0" shapeDraw="0" shapeOffsetUnit="MM" shapeFillColor="255,255,255,255" shapeOffsetY="0" shapeType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeRadiiUnit="MM" shapeRadiiX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeOffsetX="0" shapeBorderColor="128,128,128,255"/>
        <shadow shadowUnder="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetUnit="MM" shadowRadius="1.5" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowOffsetDist="1" shadowDraw="0" shadowOpacity="0.7" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowBlendMode="6" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0"/>
        <substitutions/>
      </text-style>
      <text-format multilineAlign="3" autoWrapLength="0" plussign="0" leftDirectionSymbol="&lt;" useMaxLineLengthForAutoWrap="1" rightDirectionSymbol=">" placeDirectionSymbol="0" addDirectionSymbol="0" formatNumbers="0" decimals="3" wrapChar="" reverseDirectionSymbol="0"/>
      <placement rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" centroidInside="0" maxCurvedCharAngleIn="25" distUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" maxCurvedCharAngleOut="-25" priority="5" quadOffset="4" yOffset="0" repeatDistanceUnits="MM" repeatDistance="0" distMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" dist="0" placementFlags="10" preserveRotation="1" centroidWhole="0" xOffset="0" placement="1" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR"/>
      <rendering maxNumLabels="2000" upsidedownLabels="0" obstacle="1" obstacleFactor="1" fontLimitPixelSize="0" displayAll="1" zIndex="0" limitNumLabels="0" drawLabels="1" minFeatureSize="0" labelPerPart="0" obstacleType="0" mergeLines="0" scaleVisibility="0" fontMaxPixelSize="10000" fontMinPixelSize="3" scaleMin="0" scaleMax="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" name="name" type="QString"/>
          <Option name="properties" type="Map">
            <Option name="Show" type="Map">
              <Option value="true" name="active" type="bool"/>
              <Option value="&quot;COUNT&quot; > 1" name="expression" type="QString"/>
              <Option value="3" name="type" type="int"/>
            </Option>
          </Option>
          <Option value="collection" name="type" type="QString"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <LinearlyInterpolatedDiagramRenderer classificationField="COUNT" diagramType="Pie" upperValue="510" lowerValue="0" upperHeight="20" lowerWidth="0" attributeLegend="1" lowerHeight="0" upperWidth="20">
    <DiagramCategory backgroundAlpha="255" opacity="0.708" enabled="1" lineSizeType="MM" minimumSize="0" lineSizeScale="3x:0,0,0,0,0,0" penColor="#000000" minScaleDenominator="0" sizeScale="3x:0,0,0,0,0,0" penWidth="0" sizeType="MM" backgroundColor="#ffffff" diagramOrientation="Up" width="15" rotationOffset="270" barWidth="5" maxScaleDenominator="0" height="15" scaleDependency="Area" scaleBasedVisibility="0" penAlpha="0" labelPlacementMethod="XHeight">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="&quot;COUNT_IN&quot;" label="COUNT_IN" color="#ec5a35"/>
      <attribute field="&quot;COUNT_OUT&quot;" label="COUNT_OUT" color="#1e91d4"/>
    </DiagramCategory>
    <data-defined-size-legend valign="bottom" title="" type="collapsed">
      <symbol clip_to_extent="1" force_rhr="0" alpha="0.625" name="source" type="marker">
        <layer enabled="1" pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="132,132,132,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <text-style align="1" color="0,0,0,255">
        <font weight="50" family="MS Shell Dlg 2" italic="0" size="8"/>
      </text-style>
    </data-defined-size-legend>
  </LinearlyInterpolatedDiagramRenderer>
  <DiagramLayerSettings priority="0" placement="1" zIndex="0" obstacle="0" linePlacementFlags="18" showAll="1" dist="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <layerGeometryType>0</layerGeometryType>
</qgis>
