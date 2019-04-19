<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="1" styleCategories="Symbology|Labeling" version="3.6.1-Noosa">
  <renderer-v2 enableorderby="0" symbollevels="1" forceraster="0" type="RuleRenderer">
    <rules key="{e5ae5d24-84dd-47df-9746-8fefd2907637}">
      <rule key="{e5cc762b-1cb8-452a-9f3b-82ced8a3cc87}" symbol="0" filter=" &quot;line_id&quot; > 0" label=" Linked to a line"/>
      <rule key="{0810b632-0d7a-4bc1-a020-8fb461477608}" symbol="1" filter="ELSE" label="Not linked to a line"/>
    </rules>
    <symbols>
      <symbol alpha="0.7" clip_to_extent="1" type="marker" name="0" force_rhr="0">
        <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
          <prop v="0" k="angle"/>
          <prop v="72,157,91,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="no" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="coalesce(2*scale_exp(NUMPOINTS, 1, 27, 1, 10, 0.5), 0)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="1" force_rhr="0">
        <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
          <prop v="0" k="angle"/>
          <prop v="179,7,7,162" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="no" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style fontCapitals="0" fontItalic="0" fontSizeUnit="Point" previewBkgrdColor="#ffffff" fontFamily="Arial" fontSize="8" fontWordSpacing="0" fontUnderline="0" textColor="0,0,0,255" fontWeight="50" multilineHeight="1" fontStrikeout="0" isExpression="0" fontLetterSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" blendMode="0" fieldName="NUMPOINTS" textOpacity="1" namedStyle="Normal" useSubstitutions="0">
        <text-buffer bufferSize="0.8" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="1" bufferDraw="1" bufferSizeUnits="MM" bufferBlendMode="0" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferOpacity="1"/>
        <background shapeBorderWidthUnit="MM" shapeSizeX="0" shapeBlendMode="0" shapeSizeY="0" shapeSizeType="0" shapeRadiiUnit="MM" shapeSVGFile="" shapeBorderColor="128,128,128,255" shapeOpacity="1" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeOffsetY="0" shapeType="0" shapeRotation="0" shapeRadiiY="0" shapeDraw="0" shapeBorderWidth="0" shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeSizeUnit="MM" shapeRotationType="0" shapeOffsetUnit="MM"/>
        <shadow shadowBlendMode="6" shadowOffsetGlobal="1" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowRadius="1.5" shadowColor="0,0,0,255" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowDraw="0" shadowRadiusUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowOpacity="0.7" shadowScale="100" shadowUnder="0"/>
        <substitutions/>
      </text-style>
      <text-format useMaxLineLengthForAutoWrap="1" leftDirectionSymbol="&lt;" formatNumbers="0" plussign="0" autoWrapLength="0" addDirectionSymbol="0" wrapChar="" rightDirectionSymbol=">" decimals="3" multilineAlign="3" placeDirectionSymbol="0" reverseDirectionSymbol="0"/>
      <placement distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" offsetType="0" centroidInside="0" quadOffset="4" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" xOffset="0" offsetUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistance="0" repeatDistanceUnits="MM" rotationAngle="0" placementFlags="10" dist="0" maxCurvedCharAngleIn="25" priority="5" centroidWhole="0" distUnits="MM" yOffset="0" placement="1" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" preserveRotation="1" maxCurvedCharAngleOut="-25"/>
      <rendering displayAll="0" obstacle="1" drawLabels="1" obstacleFactor="1" limitNumLabels="0" upsidedownLabels="0" scaleMin="0" scaleMax="0" mergeLines="0" maxNumLabels="2000" minFeatureSize="0" fontLimitPixelSize="0" fontMinPixelSize="3" obstacleType="0" fontMaxPixelSize="10000" zIndex="0" scaleVisibility="0" labelPerPart="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option type="Map" name="properties">
            <Option type="Map" name="Show">
              <Option value="true" type="bool" name="active"/>
              <Option value="&quot;NUMPOINTS&quot; > 1" type="QString" name="expression"/>
              <Option value="3" type="int" name="type"/>
            </Option>
          </Option>
          <Option value="collection" type="QString" name="type"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerGeometryType>0</layerGeometryType>
</qgis>
