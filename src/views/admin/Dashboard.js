import React from "react";

// components

import CardLineChart from "components/Cards/CardLineChart.js";
import TransientSettings from "components/Cards/TransientSettings.js";

import CardSettings from "components/Cards/CardSettings.js";

export default function Dashboard() {
  return (
    <>
      <div className="flex flex-wrap">
        <div className="w-full xl:w-8/12 mb-12 xl:mb-0 px-4">
          <CardLineChart />
        </div>
        <div className="w-full xl:w-4/12 px-4">
          <TransientSettings />
        </div>
      </div>
      <div className="flex flex-wrap">
        <div className="w-full px-4">
          <CardSettings />
        </div>
      </div>
    </>
  );
}
