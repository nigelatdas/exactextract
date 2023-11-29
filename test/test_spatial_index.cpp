#include "catch.hpp"
#include "spatial_index.h"

using namespace exactextract;

TEST_CASE("SpacialIndex") {
    GEOSContextHandle_t context = initGEOS_r(nullptr, nullptr);

    SpatialIndex si{context, 1, 1, 20, 20, 0, 0};

    auto poly1 =
        GEOSGeom_read_r(context, "POLYGON ((3 2, 7 2, 7 9, 3 9, 3 2))");
    auto poly2 =
        GEOSGeom_read_r(context, "POLYGON ((5 5, 8.5 5, 8.5 7.5, 5 7.5, 5 5))");

    si.addFeature(poly1.get());
    si.addFeature(poly2.get());

    CHECK(si.getFeaturesInCell(0, 0) == std::list<const GEOSGeometry*>{});
    CHECK(si.getFeaturesInCell(10, 10) == std::list<const GEOSGeometry*>{});

    CHECK(si.getFeaturesInCell(3, 3) ==
          std::list<const GEOSGeometry*>{poly1.get()});
    CHECK(si.getFeaturesInCell(7, 9) ==
          std::list<const GEOSGeometry*>{poly1.get()});

    CHECK(si.getFeaturesInCell(6, 5) ==
          std::list<const GEOSGeometry*>{poly1.get(), poly2.get()});

    finishGEOS_r(context);
}
