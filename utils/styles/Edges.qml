<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingTol="1" version="3.6.1-Noosa" styleCategories="AllStyleCategories" minScale="1e+08" readOnly="0" simplifyDrawingHints="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" maxScale="0" simplifyLocal="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="line" clip_to_extent="1" alpha="1">
        <layer enabled="1" pass="0" class="GeometryGenerator" locked="0">
          <prop v="Line" k="SymbolType"/>
          <prop v="difference(&#xd;&#xa;   difference(&#xd;&#xa;      make_line(&#xd;&#xa;         start_point($geometry),&#xd;&#xa;         centroid(&#xd;&#xa;            offset_curve(&#xd;&#xa;               $geometry, &#xd;&#xa;               length($geometry)/-5.0&#xd;&#xa;            )&#xd;&#xa;         ),&#xd;&#xa;     end_point($geometry)&#xd;&#xa;      ),&#xd;&#xa;      buffer(start_point($geometry), 0.01)&#xd;&#xa;   ),&#xd;&#xa;   buffer(end_point( $geometry), 0.01)&#xd;&#xa;)" k="geometryModifier"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@0" force_rhr="0" type="line" clip_to_extent="1" alpha="1">
            <layer enabled="1" pass="0" class="ArrowLine" locked="0">
              <prop v="1" k="arrow_start_width"/>
              <prop v="MM" k="arrow_start_width_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="arrow_start_width_unit_scale"/>
              <prop v="0" k="arrow_type"/>
              <prop v="1" k="arrow_width"/>
              <prop v="MM" k="arrow_width_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="arrow_width_unit_scale"/>
              <prop v="1.5" k="head_length"/>
              <prop v="MM" k="head_length_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="head_length_unit_scale"/>
              <prop v="1.5" k="head_thickness"/>
              <prop v="MM" k="head_thickness_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="head_thickness_unit_scale"/>
              <prop v="0" k="head_type"/>
              <prop v="1" k="is_curved"/>
              <prop v="1" k="is_repeated"/>
              <prop v="0" k="offset"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
              <prop v="0" k="ring_filter"/>
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
              <symbol name="@@0@0@0" force_rhr="0" type="fill" clip_to_extent="1" alpha="1">
                <layer enabled="1" pass="0" class="SimpleFill" locked="0">
                  <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
                  <prop v="159,159,159,255" k="color"/>
                  <prop v="bevel" k="joinstyle"/>
                  <prop v="0,0" k="offset"/>
                  <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
                  <prop v="MM" k="offset_unit"/>
                  <prop v="247,247,247,255" k="outline_color"/>
                  <prop v="no" k="outline_style"/>
                  <prop v="0.26" k="outline_width"/>
                  <prop v="MM" k="outline_width_unit"/>
                  <prop v="solid" k="style"/>
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
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>"start_Loc ID"</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>6</featureBlendMode>
  <layerOpacity>0.708</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory backgroundAlpha="255" scaleDependency="Area" minimumSize="0" backgroundColor="#ffffff" penWidth="0" height="15" enabled="0" barWidth="5" lineSizeType="MM" rotationOffset="270" opacity="1" maxScaleDenominator="1e+08" diagramOrientation="Up" penAlpha="255" scaleBasedVisibility="0" sizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" minScaleDenominator="0" penColor="#000000" width="15" sizeScale="3x:0,0,0,0,0,0">
      <fontProperties style="" description="MS Shell Dlg 2,6.6,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="2" priority="0" zIndex="0" dist="0" linePlacementFlags="18" obstacle="0" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="start">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="start_Loc ID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="start_City">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="start_Country">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="end">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="end_Loc ID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="end_City">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="end_Country">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="COUNT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" name="" index="0"/>
    <alias field="start" name="" index="1"/>
    <alias field="start_Loc ID" name="" index="2"/>
    <alias field="start_City" name="" index="3"/>
    <alias field="start_Country" name="" index="4"/>
    <alias field="end" name="" index="5"/>
    <alias field="end_Loc ID" name="" index="6"/>
    <alias field="end_City" name="" index="7"/>
    <alias field="end_Country" name="" index="8"/>
    <alias field="COUNT" name="" index="9"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="start" applyOnUpdate="0" expression=""/>
    <default field="start_Loc ID" applyOnUpdate="0" expression=""/>
    <default field="start_City" applyOnUpdate="0" expression=""/>
    <default field="start_Country" applyOnUpdate="0" expression=""/>
    <default field="end" applyOnUpdate="0" expression=""/>
    <default field="end_Loc ID" applyOnUpdate="0" expression=""/>
    <default field="end_City" applyOnUpdate="0" expression=""/>
    <default field="end_Country" applyOnUpdate="0" expression=""/>
    <default field="COUNT" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="fid" notnull_strength="1" constraints="3" unique_strength="1" exp_strength="0"/>
    <constraint field="start" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="start_Loc ID" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="start_City" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="start_Country" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="end" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="end_Loc ID" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="end_City" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="end_Country" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
    <constraint field="COUNT" notnull_strength="0" constraints="0" unique_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" exp="" desc=""/>
    <constraint field="start" exp="" desc=""/>
    <constraint field="start_Loc ID" exp="" desc=""/>
    <constraint field="start_City" exp="" desc=""/>
    <constraint field="start_Country" exp="" desc=""/>
    <constraint field="end" exp="" desc=""/>
    <constraint field="end_Loc ID" exp="" desc=""/>
    <constraint field="end_City" exp="" desc=""/>
    <constraint field="end_Country" exp="" desc=""/>
    <constraint field="COUNT" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="1" actionWidgetStyle="dropDown" sortExpression="&quot;COUNT&quot;">
    <columns>
      <column name="start" type="field" hidden="0" width="-1"/>
      <column name="start_Loc ID" type="field" hidden="0" width="-1"/>
      <column name="start_City" type="field" hidden="0" width="-1"/>
      <column name="start_Country" type="field" hidden="0" width="-1"/>
      <column name="end" type="field" hidden="0" width="-1"/>
      <column name="end_Loc ID" type="field" hidden="0" width="-1"/>
      <column name="end_City" type="field" hidden="0" width="-1"/>
      <column name="end_Country" type="field" hidden="0" width="-1"/>
      <column name="COUNT" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
      <column name="fid" type="field" hidden="0" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="COUNT" editable="1"/>
    <field name="end" editable="1"/>
    <field name="end_City" editable="1"/>
    <field name="end_Country" editable="1"/>
    <field name="end_Loc ID" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="start" editable="1"/>
    <field name="start_City" editable="1"/>
    <field name="start_Country" editable="1"/>
    <field name="start_Loc ID" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="COUNT" labelOnTop="0"/>
    <field name="end" labelOnTop="0"/>
    <field name="end_City" labelOnTop="0"/>
    <field name="end_Country" labelOnTop="0"/>
    <field name="end_Loc ID" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="start" labelOnTop="0"/>
    <field name="start_City" labelOnTop="0"/>
    <field name="start_Country" labelOnTop="0"/>
    <field name="start_Loc ID" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>start_Loc ID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
