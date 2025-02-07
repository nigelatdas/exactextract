// Copyright (c) 2018 ISciences, LLC.
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

#ifndef EXACTEXTRACT_GDAL_DATASET_WRAPPER_H
#define EXACTEXTRACT_GDAL_DATASET_WRAPPER_H

#include "feature_source.h"
#include "gdal_feature.h"

#include <gdal.h>
#include <geos_c.h>
#include <string>

namespace exactextract {

    class Feature;

    class GDALDatasetWrapper : public FeatureSource {
    public:
        GDALDatasetWrapper(const std::string &filename, const std::string & layer, std::string id_field);

        const Feature& feature() const override;

        bool next() override;

        const std::string& id_field() const override { return m_id_field; }

        void copy_field(const std::string & field_name, OGRLayerH to) const;

        ~GDALDatasetWrapper() override;

    private:
        GDALDatasetH m_dataset;
        OGRLayerH m_layer;
        std::string m_id_field;
        GDALFeature m_feature;
    };

}

#endif //EXACTEXTRACT_GDAL_DATASET_WRAPPER_H
