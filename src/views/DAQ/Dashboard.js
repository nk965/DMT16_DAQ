import React from "react";

// components

import CardLineChart from "components/Cards/CardLineChart.js";
import CardTransientSettings from "components/Cards/CardTransientSettings.js";

import CardUserConfig from "components/Cards/CardUserConfig.js";

export default function Dashboard() {
  return (
    <>
      <div className="flex flex-wrap">
        <div className="w-full xl:w-8/12 mb-12 xl:mb-0 px-4">
          <CardLineChart />
        </div>
        <div className="w-full xl:w-4/12 px-4">
          <CardTransientSettings />
        </div>
      </div>
      <div className="flex flex-wrap">
        <div className="w-full px-4">
          <CardUserConfig />
        </div>
      </div>
    </>
  );
}
