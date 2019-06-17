# -*- coding: utf-8 -*-

"""
***************************************************************************
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

__author__ = 'Anita Graser'
__date__ = 'January 2018'
__copyright__ = '(C) 2018, Anita Graser'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import math
import numpy as np
from datetime import datetime

from qgis.core import QgsFeature, QgsPoint, QgsVector, QgsGeometry, QgsField, QgsSpatialIndex

import processing

from qgis.core import QgsMessageLog, QgsProcessingFeedback
from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig

#Convenient function to debug
NAME = "Visualist"
log = lambda m: QgsMessageLog.logMessage(m, NAME)

idc = 0.6666667  # For decreasing iterations
sdc = 0.5  # For decreasing the step-size
K = 0.1
eps = 0.000001

def forcecalcx(x, y, d) :
    if abs(x) > eps and abs(y) > eps :
        x *= 1.0 / d
    else :
        x = 0.0
    return x

def forcecalcy(x, y, d) :
    if abs(x) > eps and abs(y) > eps :
        y *= 1.0 / d
    else :
        y = 0.0
    return y

# ------------------------------------ EDGE ------------------------------------ #

class Edge(QgsFeature):
    def __init__(self, feature, weight_index=None):
        super(Edge,self).__init__(feature)
        if weight_index is not None:
            self.weight = float(self.attributes()[weight_index]) #self[weight_field]
        else:
            self.weight = 1
        self.agg_weight = self.weight

    def increase_weight(self,value=1):
        self.agg_weight += value

    def get_weight(self):
        return self.weight

    def get_agg_weight(self):
        return self.agg_weight

# ------------------------------------ MISC ------------------------------------ #

class MiscUtils:

    @staticmethod
    def project_point_on_line(pt, line):
        """ Projects point onto line, needed for compatibility computation """
        v0 = line.vertexAt(0)
        v1 = line.vertexAt(1)
        length = max(line.length(), 10**(-6))
        r = ((v0.y() - pt.y()) * (v0.y() - v1.y()) -
             (v0.x() - pt.x()) * (v1.x() - v0.x())) / (length**2)
        return QgsPoint(v0.x() + r * (v1.x() - v0.x()), v0.y() + r * (v1.y() - v0.y()))


# ------------------------------------ EDGE-CLUSTER  ------------------------------------ #

class EdgeCluster():

    def __init__(self, edges, initial_step_size, iterations, cycles, compatibility):
        self.S = initial_step_size  # Weighting factor (needs to be cached, because will be decreased in every cycle)
        self.I = iterations         # Number of iterations per cycle (needs to be cached, because will be decreased in every cycle)
        self.edges = edges          # Edges to bundle in this cluster
        self.edge_lengths = []      # Array to cache edge lenghts
        self.E = len(edges)         # Number of edges
        self.EP = 2                 # Current number of edge points
        self.SP = 0                 # Current number of subdivision points
        self.compatibility = compatibility
        self.cycles = cycles
        self.compatibility_matrix = np.zeros(shape=(self.E,self.E)) # Compatibility matrix
        self.direction_matrix = np.zeros(shape=(self.E,self.E))     # Encodes direction of edge pairs
        self.N = (2**cycles ) + 1                                   # Maximum number of points per edge
        self.epm_x = np.zeros(shape=(self.E,self.N))                # Bundles edges (x-values)
        self.epm_y = np.zeros(shape=(self.E,self.N))                # Bundles edges (y-values)

        self.segments = {} # dict of Edges containing {id_seg: seg}
        self.allSegments = {} # {id_seg: [seg as Edge, MainEdge id]}

    def get_size(self):
        return len(self.edges)

    def get_segments(self, edge):
        return self.segments[edge.id()]

    def create_segments(self, weight_index, feedback):
        self.index = QgsSpatialIndex()
        seg_id = 0
        for i, edge in enumerate(self.edges):
            if feedback.isCanceled(): return
            feedback.setProgress(100.0*(i+1)/len(self.edges))
            geom = edge.geometry()
            attrs = edge.attributes()
            polyline = geom.asPolyline()
            segments = {}
            for j in range(0,len(polyline)-1):
                feat = QgsFeature()
                feat.setId(seg_id)
                seg_id += 1
                g = QgsGeometry.fromPolylineXY([polyline[j],polyline[j+1]])
                feat.setGeometry(g)
                feat.setAttributes(attrs+[j]) #Add the rank of the segment
                segEdge = Edge(feat, weight_index)
                self.allSegments[segEdge.id()] = [segEdge, edge.id()]
                self.index.addFeature(segEdge)
                segments[segEdge.id()] = segEdge
            self.segments[edge.id()] = segments

    def collapse_lines(self, max_distance, feedback):
        for i, edge1 in enumerate(self.edges):
            feedback.setProgress(100.0*(i+1)/len(self.edges))
            if feedback.isCanceled(): return
            segments1 = self.get_segments(edge1)
            for key1, segment1 in segments1.items():
                geom1 = segment1.geometry()
                # get other edges in the vicinty
                tolerance = min(max_distance,geom1.length()/2)
                ids = self.index.intersects(geom1.buffer(tolerance,4).boundingBox())
                # feedback.setProgressText("{0} matching segments with tolerance of {1}".format(len(ids), tolerance))
                keys2pop = []
                for id in ids:
                    edge2_id = self.allSegments[id][1]
                    if edge2_id == edge1.id(): continue
                    segment2 = self.allSegments[id][0]
                    geom2 = segment2.geometry()
                    d0 = geom1.vertexAt(0).distance(geom2.vertexAt(0))
                    d1 = geom1.vertexAt(1).distance(geom2.vertexAt(1))
                    if d0 <= (tolerance/2) and d1 <= (tolerance/2):
                        segment1.increase_weight(segment2.get_weight())
                        keys2pop.append(id)
                    d0 = geom1.vertexAt(0).distance(geom2.vertexAt(1))
                    d1 = geom1.vertexAt(1).distance(geom2.vertexAt(0))
                    if d0 <= (tolerance/2) and d1 <= (tolerance/2):
                        segment1.increase_weight(segment2.get_weight())
                        keys2pop.append(id)
                for id in keys2pop:
                    self.index.deleteFeature(self.allSegments[id][0])
                    self.segments[self.allSegments[id][1]].pop(id)
                    self.allSegments.pop(id)


    def compute_compatibilty_matrix(self, feedback):
        """
        Compatibility is stored in a matrix (rows = edges, columns = edges).
        Every coordinate in the matrix tells whether the two edges (r,c)/(c,r)
        are compatible, or not. The diagonal is always zero, and the other fields
        are filled with either -1 (not compatible) or 1 (compatible).
        The matrix is symmetric.
        """
        feedback.setProgressText("Compute compatibility matrix")
        edges_as_geom = []
        edges_as_vect = []
        for e_idx, edge in enumerate(self.edges):
            if feedback.isCanceled(): return
            geom = edge.geometry()
            edges_as_geom.append(geom)
            edges_as_vect.append(QgsVector(geom.vertexAt(1).x() - geom.vertexAt(0).x(),
                                           geom.vertexAt(1).y() - geom.vertexAt(0).y()))
            self.edge_lengths.append(edges_as_vect[e_idx].length())

        progress = 0
        for i in range(self.E-1):
            if feedback.isCanceled(): return
            feedback.setProgress(100.0*(i+1)/(self.E-1))
            for j in range(i+1, self.E):
                if feedback.isCanceled(): return
                # Parameters
                lavg = (self.edge_lengths[i] + self.edge_lengths[j]) / 2.0
                dot = edges_as_vect[i].normalized() * edges_as_vect[j].normalized()

                # Angle compatibility
                angle_comp = abs(dot)

                # Scale compatibility
                scale_comp = 2.0 / (lavg / min(self.edge_lengths[i],
                                    self.edge_lengths[j]) + max(self.edge_lengths[i],
                                    self.edge_lengths[j]) / lavg)

                # Position compatibility
                i0 = edges_as_geom[i].vertexAt(0)
                i1 = edges_as_geom[i].vertexAt(1)
                j0 = edges_as_geom[j].vertexAt(0)
                j1 = edges_as_geom[j].vertexAt(1)
                e1_mid = QgsPoint((i0.x() + i1.x()) / 2.0, (i0.y() + i1.y()) / 2.0)
                e2_mid = QgsPoint((j0.x() + j1.x()) / 2.0, (j0.y() + j1.y()) / 2.0)
                diff = QgsVector(e2_mid.x() - e1_mid.x(), e2_mid.y() - e1_mid.y())
                pos_comp = lavg / (lavg + diff.length())

                # Visibility compatibility
                mid_E1 = edges_as_geom[i].centroid()
                mid_E2 = edges_as_geom[j].centroid()
                #dist = mid_E1.distance(mid_E2)
                I0 = MiscUtils.project_point_on_line(j0, edges_as_geom[i])
                I1 = MiscUtils.project_point_on_line(j1, edges_as_geom[i])
                mid_I = QgsGeometry.fromPolyline([I0, I1]).centroid()
                dist_I = I0.distance(I1)
                if dist_I == 0.0:
                    visibility1 = 0.0
                else:
                    visibility1 = max(0, 1 - ((2 * mid_E1.distance(mid_I)) / dist_I))
                J0 = MiscUtils.project_point_on_line(i0, edges_as_geom[j])
                J1 = MiscUtils.project_point_on_line(i1, edges_as_geom[j])
                mid_J = QgsGeometry.fromPolyline([J0, J1]).centroid()
                dist_J = J0.distance(J1)
                if dist_J == 0.0:
                    visibility2 = 0.0
                else:
                    visibility2 = max(0, 1 - ((2 * mid_E2.distance(mid_J)) / dist_J))
                visibility_comp = min(visibility1, visibility2)

                # Compatibility score
                comp_score = angle_comp * scale_comp * pos_comp * visibility_comp

                # Fill values into the matrix (1 = yes, -1 = no) and use matrix symmetry (i/j = j/i)
                if comp_score >= self.compatibility:
                    self.compatibility_matrix[i, j] = 1
                    self.compatibility_matrix[j, i] = 1
                else:
                    self.compatibility_matrix[i, j] = -1
                    self.compatibility_matrix[j, i] = -1

                # Store direction
                distStart1 = j0.distance(i0)
                distStart2 = j1.distance(i0)
                if distStart1 > distStart2:
                    self.direction_matrix[i, j] = -1
                    self.direction_matrix[j, i] = -1
                else:
                    self.direction_matrix[i, j] = 1
                    self.direction_matrix[j, i] = 1


    def force_directed_eb(self, feedback):
        """ Force-directed edge bundling """
        if feedback.isCanceled(): return
        # Create compatibility matrix
        self.compute_compatibilty_matrix(feedback)
        feedback.setCurrentStep(2)
        if feedback.isCanceled(): return

        for e_idx, edge in enumerate(self.edges):
            vertices = edge.geometry().asPolyline()
            self.epm_x[e_idx, 0] = vertices[0].x()
            self.epm_y[e_idx, 0] = vertices[0].y()
            self.epm_x[e_idx, self.N-1] = vertices[1].x()
            self.epm_y[e_idx, self.N-1] = vertices[1].y()

        # For each cycle
        feedback.setProgressText('Compute force-directed layout')
        for c in range(self.cycles):
            if feedback.isCanceled(): return
            # New number of subdivision points
            current_num = self.EP
            currentindeces = []
            for i in range(current_num):
                idx = int((float(i) / float(current_num - 1)) * float(self.N - 1))
                currentindeces.append(idx)
            self.SP += 2 ** c
            self.EP = self.SP + 2
            edgeindeces = []
            newindeces = []
            for i in range(self.EP):
                idx = int((float(i) / float(self.EP - 1)) * float(self.N - 1))
                edgeindeces.append(idx)
                if idx not in currentindeces:
                    newindeces.append(idx)
            pointindeces = edgeindeces[1:self.EP-1]

            # Calculate position of new points
            for idx in newindeces:
                if feedback.isCanceled(): return
                i = int((float(idx) / float(self.N - 1)) * float(self.EP - 1))
                left = i - 1
                leftidx = int((float(left) / float(self.EP - 1)) * float(self.N - 1))
                right = i + 1
                rightidx = int((float(right) / float(self.EP - 1)) * float(self.N - 1))
                self.epm_x[:, idx] = ( self.epm_x[:, leftidx] + self.epm_x[:, rightidx] ) / 2.0
                self.epm_y[:, idx] = ( self.epm_y[:, leftidx] + self.epm_y[:, rightidx] ) / 2.0

            # Needed for spring forces
            KP0 = np.zeros(shape=(self.E,1))
            KP0[:,0] = np.asarray(self.edge_lengths)
            KP = K / (KP0 * (self.EP - 1))

            # For all iterations (number decreased in every cycle)
            for iteration in range(self.I):
                if feedback.isCanceled(): return
                if (iteration+1) % 5 == 0:
                    feedback.pushCommandInfo("Cycle {0} and Iteration {1}".format(c+1, iteration+1))
                    feedback.setProgress(100.0*(iteration+1)/self.I)
                # Spring forces
                middlepoints_x = self.epm_x[:, pointindeces]
                middlepoints_y = self.epm_y[:, pointindeces]
                neighbours_left_x = self.epm_x[:, edgeindeces[0:self.EP-2]]
                neighbours_left_y = self.epm_y[:, edgeindeces[0:self.EP-2]]
                neighbours_right_x = self.epm_x[:, edgeindeces[2:self.EP]]
                neighbours_right_y = self.epm_y[:, edgeindeces[2:self.EP]]
                springforces_x = (neighbours_left_x - middlepoints_x + neighbours_right_x - middlepoints_x) * KP
                springforces_y = (neighbours_left_y - middlepoints_y + neighbours_right_y - middlepoints_y) * KP

                # Electrostatic forces
                electrostaticforces_x = np.zeros(shape=(self.E, self.SP))
                electrostaticforces_y = np.zeros(shape=(self.E, self.SP))
                # Loop through all edges
                for e_idx, edge in enumerate(self.edges):
                    if feedback.isCanceled(): return
                    # Loop through compatible edges
                    comp_list = np.where(self.compatibility_matrix[:,e_idx] > 0)
                    for other_idx in np.nditer(comp_list, ['zerosize_ok']):
                        if feedback.isCanceled(): return
                        otherindeces = pointindeces[:]
                        if self.direction_matrix[e_idx,other_idx] < 0:
                            otherindeces.reverse()
                        # Distance between points
                        subtr_x = self.epm_x[other_idx, otherindeces] - self.epm_x[e_idx, pointindeces]
                        subtr_y = self.epm_y[other_idx, otherindeces] - self.epm_y[e_idx, pointindeces]
                        distance = np.sqrt( np.add( np.multiply(subtr_x, subtr_x), np.multiply(subtr_y, subtr_y)))
                        flocal_x = map(forcecalcx, subtr_x, subtr_y, distance)
                        flocal_y = map(forcecalcy, subtr_x, subtr_y, distance)
                        # Sum of forces
                        electrostaticforces_x[e_idx, :] += np.array(list(flocal_x))
                        electrostaticforces_y[e_idx, :] += np.array(list(flocal_y))

                # Compute total forces
                force_x = (springforces_x + electrostaticforces_x) * self.S
                force_y = (springforces_y + electrostaticforces_y) * self.S

                # Compute new point positions
                self.epm_x[:, pointindeces] += force_x
                self.epm_y[:, pointindeces] += force_y

            # Adjustments for next cycle
            self.S = self.S * sdc              # Decrease weighting factor
            self.I = int(round(self.I * idc))  # Decrease iterations

        feedback.setProgressText("Ongoing final calculations")
        for e_idx in range(self.E):
            if feedback.isCanceled(): return
            # Create a new polyline out of the line array
            line = map(lambda p,q: QgsPoint(p,q), self.epm_x[e_idx], self.epm_y[e_idx])
            self.edges[e_idx].setGeometry(QgsGeometry.fromPolyline(line))
