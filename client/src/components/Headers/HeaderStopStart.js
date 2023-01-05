import React from "react";

// components

import CardStopStart from "components/Cards/CardStopStart.js";

export default function HeaderStopStart() {
  return (
    <>
      {/* Header */}
      <div className="md:pt-32 pb-32 pt-12">
        <div className="px-4 md:px-10 mx-auto w-full">
          <div>
            {/* Card stats */}
            <div className="flex flex-wrap">
              <button className="w-full lg:w-6/12 xl:w-6/12 px-4">
                <CardStopStart
                  statTitle="Master Stop"
                  color="bg-red-500"
                  accent="active:bg-red-600"
                />
              </button>
              <button className="w-full lg:w-6/12 xl:w-6/12 px-4">
                <CardStopStart
                  statTitle="Start Experiment"
                  color="bg-emerald-500"
                  accent="active:bg-emerald-600"
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
