// Copyright (c) 2023 ISciences, LLC.
// All rights reserved.
//
// This software is licensed under the Apache License, Version 2.0 (the "License").
// You may not use this file except in compliance with the License. You may
// obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "coverage_processor.h"
#include "coverage_operation.h"
#include "raster_area.h"

namespace exactextract {

void
CoverageProcessor::process()
{
    if (m_operations.empty()) {
        return;
    }

    if (m_operations.size() > 1) {
        throw std::runtime_error("Unexpected operation in CoverageProcessor.");
    }

    if (dynamic_cast<CoverageOperation*>(m_operations.front().get()) == nullptr) {
        throw std::runtime_error("Only CoverageOperation can be handled by CoverageProcessor.");
    }


    CoverageOperation& op = static_cast<CoverageOperation&>(*m_operations.front());
    m_output.add_operation(op);

    const auto& opts = op.options();

    auto grid = common_grid(m_operations.begin(), m_operations.end());

    while (m_shp.next()) {
        std::string name{ m_shp.feature_field(m_shp.id_field()) };

        progress(name);

        auto geom = geos_ptr(m_geos_context, m_shp.feature_geometry(m_geos_context));
        auto feature_bbox = geos_get_box(m_geos_context, geom.get());

        // Crop grid to portion overlapping feature
        auto cropped_grid = grid.crop(feature_bbox);

        for (const auto& subgrid : subdivide(cropped_grid, m_max_cells_in_memory)) {
            auto coverage_fractions = raster_cell_intersection(subgrid, m_geos_context, geom.get());

            RasterSource* values = opts.include_values ? op.values : nullptr;
            RasterSource* weights = opts.include_weights ? op.weights : nullptr;

            std::unique_ptr<AbstractRaster<double>> areas;
            if (opts.area_method == CoverageOperation::AreaMethod::CARTESIAN) {
                areas = std::make_unique<CartesianAreaRaster<double>>(coverage_fractions.grid());
            } else if (opts.area_method == CoverageOperation::AreaMethod::SPHERICAL) {
                areas = std::make_unique<SphericalAreaRaster<double>>(coverage_fractions.grid());
            }

            for (const auto& loc : RasterCoverageIteration<double, double>(coverage_fractions, values, weights, grid, areas.get())) {
                op.save_coverage(loc);
                m_output.write(name);
            }

            progress();
        }
    }
}

}