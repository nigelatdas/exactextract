#include "spatial_index.h"

#include <algorithm>
#include <functional>
#include <iostream>
#include <list>
#include <memory>
#include <vector>

#include "box.h"
#include "geos_utils.h"

namespace exactextract {
    void SpatialIndex::addFeature(const GEOSGeometry* feature) {
        Box bounds = geos_get_box(m_geos_context, feature);
        // // Get the AABB of the feature
        double minX = bounds.xmin - m_gridOffsetX;
        double minY = bounds.ymin - m_gridOffsetY;
        double maxX = bounds.xmax - m_gridOffsetX;
        double maxY = bounds.ymax - m_gridOffsetY;

        // Calculate the grid indices for the AABB
        int minGridX = static_cast<int>((minX / m_cellWidth));
        int minGridY = static_cast<int>((minY / m_cellHeight));
        int maxGridX = static_cast<int>((maxX / m_cellWidth));
        int maxGridY = static_cast<int>((maxY / m_cellHeight));

        // TODO .. bound check?

        // Add the feature to the corresponding grid cells
        for (int x = minGridX; x <= maxGridX; ++x) {
            for (int y = minGridY; y <= maxGridY; ++y) {
                m_grid[x][y].push_back(feature);
            }
        }
    }
}  // namespace exactextract