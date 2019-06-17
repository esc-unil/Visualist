<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Labeling" labelsEnabled="0" version="3.6.1-Noosa">
  <renderer-v2 forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="0" type="line">
        <layer enabled="1" pass="0" class="GeometryGenerator" locked="0">
          <prop k="SymbolType" v="Line"/>
          <prop k="geometryModifier" v="difference(&#xd;&#xa;   difference(&#xd;&#xa;      make_line(&#xd;&#xa;         start_point($geometry),&#xd;&#xa;         centroid(&#xd;&#xa;            offset_curve(&#xd;&#xa;               $geometry, &#xd;&#xa;               length($geometry)/-7.0&#xd;&#xa;            )&#xd;&#xa;         ),&#xd;&#xa;     end_point($geometry)&#xd;&#xa;      ),&#xd;&#xa;      buffer(start_point($geometry), 0.01)&#xd;&#xa;   ),&#xd;&#xa;   buffer(end_point( $geometry), 0.01)&#xd;&#xa;)"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@0@0" type="line">
            <layer enabled="1" pass="0" class="ArrowLine" locked="0">
              <prop k="arrow_start_width" v="1"/>
              <prop k="arrow_start_width_unit" v="MM"/>
              <prop k="arrow_start_width_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="arrow_type" v="0"/>
              <prop k="arrow_width" v="1"/>
              <prop k="arrow_width_unit" v="MM"/>
              <prop k="arrow_width_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="head_length" v="1.5"/>
              <prop k="head_length_unit" v="MM"/>
              <prop k="head_length_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="head_thickness" v="1.5"/>
              <prop k="head_thickness_unit" v="MM"/>
              <prop k="head_thickness_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="head_type" v="0"/>
              <prop k="is_curved" v="1"/>
              <prop k="is_repeated" v="1"/>
              <prop k="offset" v="0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="offset_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="ring_filter" v="0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="arrowHeadLength" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="COUNT" name="field" type="QString"/>
                      <Option name="transformer" type="Map">
                        <Option name="d" type="Map">
                          <Option value="1" name="exponent" type="double"/>
                          <Option value="10" name="maxOutput" type="double"/>
                          <Option value="17" name="maxValue" type="double"/>
                          <Option value="1" name="minOutput" type="double"/>
                          <Option value="1" name="minValue" type="double"/>
                          <Option value="0" name="nullOutput" type="double"/>
                        </Option>
                        <Option value="0" name="t" type="int"/>
                      </Option>
                      <Option value="2" name="type" type="int"/>
                    </Option>
                    <Option name="arrowHeadThickness" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="COUNT" name="field" type="QString"/>
                      <Option name="transformer" type="Map">
                        <Option name="d" type="Map">
                          <Option value="1" name="exponent" type="double"/>
                          <Option value="10" name="maxOutput" type="double"/>
                          <Option value="17" name="maxValue" type="double"/>
                          <Option value="1" name="minOutput" type="double"/>
                          <Option value="1" name="minValue" type="double"/>
                          <Option value="0" name="nullOutput" type="double"/>
                        </Option>
                        <Option value="0" name="t" type="int"/>
                      </Option>
                      <Option value="2" name="type" type="int"/>
                    </Option>
                    <Option name="arrowStartWidth" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="COUNT" name="field" type="QString"/>
                      <Option name="transformer" type="Map">
                        <Option name="d" type="Map">
                          <Option value="0.57" name="exponent" type="double"/>
                          <Option value="10" name="maxSize" type="double"/>
                          <Option value="17" name="maxValue" type="double"/>
                          <Option value="1" name="minSize" type="double"/>
                          <Option value="1" name="minValue" type="double"/>
                          <Option value="0" name="nullSize" type="double"/>
                          <Option value="3" name="scaleType" type="int"/>
                        </Option>
                        <Option value="1" name="t" type="int"/>
                      </Option>
                      <Option value="2" name="type" type="int"/>
                    </Option>
                    <Option name="arrowWidth" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="COUNT" name="field" type="QString"/>
                      <Option name="transformer" type="Map">
                        <Option name="d" type="Map">
                          <Option value="0.57" name="exponent" type="double"/>
                          <Option value="10" name="maxSize" type="double"/>
                          <Option value="17" name="maxValue" type="double"/>
                          <Option value="1" name="minSize" type="double"/>
                          <Option value="1" name="minValue" type="double"/>
                          <Option value="0" name="nullSize" type="double"/>
                          <Option value="3" name="scaleType" type="int"/>
                        </Option>
                        <Option value="1" name="t" type="int"/>
                      </Option>
                      <Option value="2" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
              <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@@0@0@0" type="fill">
                <layer enabled="1" pass="0" class="SimpleFill" locked="0">
                  <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="color" v="159,159,159,255"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="247,247,247,255"/>
                  <prop k="outline_style" v="no"/>
                  <prop k="outline_width" v="0.26"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="style" v="solid"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option value="" name="name" type="QString"/>
                      <Option name="properties" type="Map">
                        <Option name="fillColor" type="Map">
                          <Option value="false" name="active" type="bool"/>
                          <Option value="1" name="type" type="int"/>
                          <Option value="" name="val" type="QString"/>
                        </Option>
                        <Option name="outlineWidth" type="Map">
                          <Option value="false" name="active" type="bool"/>
                          <Option value="1" name="type" type="int"/>
                          <Option value="" name="val" type="QString"/>
                        </Option>
                      </Option>
                      <Option value="collection" name="type" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style fontCapitals="0" fontSize="10" blendMode="0" fontItalic="0" textColor="0,0,0,255" isExpression="0" fontSizeUnit="Point" fontUnderline="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="MS Shell Dlg 2" fontWeight="50" textOpacity="1" fieldName="COUNT" fontLetterSpacing="0" previewBkgrdColor="#ffffff" fontStrikeout="0" multilineHeight="1" namedStyle="Normal" fontWordSpacing="0" useSubstitutions="0">
        <text-buffer bufferDraw="0" bufferNoFill="1" bufferOpacity="1" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferSize="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0" bufferSizeUnits="MM"/>
        <background shapeSizeUnit="MM" shapeOpacity="1" shapeBorderWidth="0" shapeRotationType="0" shapeSVGFile="" shapeSizeX="0" shapeSizeY="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeType="0" shapeJoinStyle="64" shapeRadiiY="0" shapeDraw="0" shapeOffsetUnit="MM" shapeFillColor="255,255,255,255" shapeOffsetY="0" shapeType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeRadiiUnit="MM" shapeRadiiX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeOffsetX="0" shapeBorderColor="128,128,128,255"/>
        <shadow shadowUnder="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetUnit="MM" shadowRadius="1.5" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowOffsetDist="1" shadowDraw="0" shadowOpacity="0.7" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowBlendMode="6" shadowRadiusUnit="MM" shadowRadiusAlphaOnly="0"/>
        <substitutions/>
      </text-style>
      <text-format multilineAlign="4294967295" autoWrapLength="0" plussign="0" leftDirectionSymbol="&lt;" useMaxLineLengthForAutoWrap="1" rightDirectionSymbol=">" placeDirectionSymbol="0" addDirectionSymbol="0" formatNumbers="0" decimals="3" wrapChar="" reverseDirectionSymbol="0"/>
      <placement rotationAngle="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" centroidInside="0" maxCurvedCharAngleIn="25" distUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" maxCurvedCharAngleOut="-25" priority="5" quadOffset="4" yOffset="0" repeatDistanceUnits="MM" repeatDistance="0" distMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" dist="0" placementFlags="1" preserveRotation="1" centroidWhole="0" xOffset="0" placement="2" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR"/>
      <rendering maxNumLabels="2000" upsidedownLabels="0" obstacle="1" obstacleFactor="1" fontLimitPixelSize="0" displayAll="0" zIndex="0" limitNumLabels="0" drawLabels="1" minFeatureSize="0" labelPerPart="0" obstacleType="0" mergeLines="0" scaleVisibility="0" fontMaxPixelSize="10000" fontMinPixelSize="3" scaleMin="0" scaleMax="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" name="name" type="QString"/>
          <Option name="properties"/>
          <Option value="collection" name="type" type="QString"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>6</featureBlendMode>
  <layerGeometryType>1</layerGeometryType>
</qgis>
