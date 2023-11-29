// // Copyright (c) 2019 ISciences, LLC.
// // All rights reserved.
// //
// // This software is licensed under the Apache License, Version 2.0 (the
// // "License"). You may not use this file except in compliance with the
// License.
// // You may obtain a copy of the License at
// // http://www.apache.org/licenses/LICENSE-2.0.
// //
// // Unless required by applicable law or agreed to in writing, software
// // distributed under the License is distributed on an "AS IS" BASIS,
// // WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// // See the License for the specific language governing permissions and
// // limitations under the License.

// #ifndef EXACTEXTRACT_FIXED_WINDOW_RASTER_SEQUENTIAL_PROCESSOR_H
// #define EXACTEXTRACT_FIXED_WINDOW_RASTER_SEQUENTIAL_PROCESSOR_H

// // #include <memory>

// // #include "geos_utils.h"
// #include "feature_source.h"
// #include "processor.h"
// #include "spatial_index.h"

// namespace exactextract {

//     /**
//      * @brief The FixedWindowRasterSequentialProcessor class iterates over
//      * chunks of the raster, fetching features that intersect each chunk and
//      * incrementally updating their statistics. It requires that all features
//      * and their associated statistics remain in memory at all times. It may
//      be
//      * efficient for rasters that from which random rectangles cannot be
//      * efficiently read.
//      */
//     class FixedWindowRasterSequentialProcessor : public Processor {
//     public:
//         using Processor::Processor;

//         FixedWindowRasterSequentialProcessor(
//             FeatureSource& ds, OutputWriter& out,
//             std::vector<std::unique_ptr<Operation>> ops)
//             : Processor(ds, out, ops) {
//             // m_spindex = std::make_unique<exactextract::SpatialIndex>(
//             //     m_geos_context, 1, 1, 20, 20, 0, 0);
//         }

//         void read_features();
//         void populate_index();

//         void process() override;

//     private:
//         using Feature = std::pair<std::string, geom_ptr_r>;

//         std::vector<Feature> m_features;
//         tree_ptr_r m_feature_tree{
//             geos_ptr(m_geos_context, GEOSSTRtree_create_r(m_geos_context,
//             10))};
//         std::unique_ptr<exactextract::SpatialIndex> m_spindex;
//     };

// }  // namespace exactextract

// #endif  // EXACTEXTRACT_RASTER_SEQUENTIAL_PROCESSOR_H
