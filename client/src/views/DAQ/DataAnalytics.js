import React from "react";

// components

import CardTransientSettings from "components/Cards/CardTransientSettings.js";

export default function DataAnalytics() {
  return (
    <>
      <div className="flex flex-wrap">
        <div className="w-full px-4">
          <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
            <CardTransientSettings />
          </div>
        </div>
      </div>
    </>
  );
}
