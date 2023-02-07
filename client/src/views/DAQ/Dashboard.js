import React from "react";
//import { useState } from 'react';

// components

import CardLineChart from "components/Cards/CardLineChart.js";
import CardTransientSettings from "components/Cards/CardTransientSettings.js";

import CardStopStart from "components/Cards/CardStopStart.js";

import CardUserConfig from "components/Cards/CardUserConfig.js";

export default function Dashboard() {

  //const [userConfig] = useState([]);

  const postResult = (result) => {
    console.log(result);
  }

  return (
    <>
        <button className="w-full lg:w-6/12 xl:w-6/12 px-4 py-4">
          <CardStopStart
            statTitle="Master Stop"
            color="bg-red-500"
            accent="active:bg-red-600"
          />
        </button>
        <button className="w-full lg:w-6/12 xl:w-6/12 px-4 py-4">
          <CardStopStart
            statTitle="Start Experiment"
            color="bg-emerald-500"
            accent="active:bg-emerald-600"
          />
        </button>
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
          <CardUserConfig postResult = {postResult}/>
        </div>
      </div>
    </>
  );
}
