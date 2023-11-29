

#ifndef EXACTEXTRACT_SPATIAL_INDEX_H
#define EXACTEXTRACT_SPATIAL_INDEX_H

#include <list>
#include <vector>

#include "geos_utils.h"

namespace exactextract {
    class SpatialIndex {
    public:
        SpatialIndex(GEOSContextHandle_t context, double cellWidth,
                     double cellHeight, int columnCount, int rowCount,
                     double gridOffsetX, double gridOffsetY)
            : m_cellWidth(cellWidth),
              m_cellHeight(cellHeight),
              m_gridOffsetX(gridOffsetX),
              m_gridOffsetY(gridOffsetY),
              m_geos_context(context),
              m_grid(columnCount,
                     std::vector<std::list<const GEOSGeometry*>>(rowCount)) {
        }

        void addFeature(const GEOSGeometry* feature);

        // Function to get features in a specific grid cell
        std::list<const GEOSGeometry*> getFeaturesInCell(int xIndex,
                                                         int yIndex) {
            return m_grid[xIndex][yIndex];
        }

    private:
        double m_cellWidth;
        double m_cellHeight;
        double m_gridOffsetX;
        double m_gridOffsetY;
        GEOSContextHandle_t m_geos_context;
        std::vector<std::vector<std::list<const GEOSGeometry*>>> m_grid;
    };
}  // namespace exactextract

#endif  // EXACTEXTRACT_SPATIAL_INDEX_H