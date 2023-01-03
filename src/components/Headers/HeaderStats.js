import React from "react";

// components

import CardStats from "components/Cards/CardStats.js";

export default function HeaderStats() {
  return (
    <>
      {/* Header */}
      <div className="md:pt-32 pb-32 pt-12">
        <div className="px-4 md:px-10 mx-auto w-full">
          <div>
            {/* Card stats */}
            <div className="flex flex-wrap">
              <div className="w-full lg:w-6/12 xl:w-6/12 px-4">
                <CardStats
                  //statSubtitle="TRAFFIC"
                  statTitle="Master Stop"
                  color="bg-red-500"
                  //statArrow="up"
                  // statPercent="3.48"
                  //statPercentColor="text-emerald-500"
                  //statDescripiron="Since last month"
                  //statIconName="far fa-chart-bar"
                  //statIconColor="bg-red-500"
                />
              </div>
              <div className="w-full lg:w-6/12 xl:w-6/12 px-4">
                <CardStats
                  //statSubtitle="PERFORMANCE"
                  statTitle="Start Experiment"
                  color="bg-emerald-500"
                  //statArrow="up"
                  //statPercent="12"
                  //statPercentColor="text-emerald-500"
                  //statDescripiron="Since last month"
                  //statIconName="fas fa-percent"
                  //statIconColor="bg-lightBlue-500"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
