import React from "react";

// components

import CardLineChart from "components/Cards/CardLineChart.js";
import CardTransientSettings from "components/Cards/CardTransientSettings.js";

export default function Transient() {
  return (
    <>
      <div className="flex flex-wrap">
        <div className="w-full xl:mb-0 px-4 py-2">
          <CardLineChart />
        </div>
        <div className="w-full px-4">
          <CardTransientSettings />
        </div>
      </div>
    </>
  );
}
