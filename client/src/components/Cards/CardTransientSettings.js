import React from "react";
import { useState } from "react";

// components

import CardStopStart from "components/Cards/CardStopStart.js";

export default function CardTransientSettings() {
  const [transientInput, setTransInput] = useState({
    // default values
    type: "transientInput",
    start_y: 25,
    end_y: 55,
    nodes: 7,
    presetConfig: "Linear",
  });

  const postResult = (result) => {
    console.log(result);
  };

  const postTransConfig = (inputs) => {
    console.log("Transient Config");

    fetch("http://127.0.0.1:5000/LoadTransConfig", {
      credentials: "same-origin",
      "Content-Type": "application/json",
      method: "POST",
      body: JSON.stringify(inputs),
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.log(error));
  };

  const handleChange = (event) => {
    const { name, type, value } = event.target;

    switch (type) {
      case "Number":
        setTransInput({ ...transientInput, [name]: Number(value) });
        break;
      default:
        setTransInput({ ...transientInput, [name]: value });
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    postResult(transientInput); // TODO: instead of Transient logging, change func to POST
  };

  const handleLoadTransConfig = (event) => {
    event.preventDefault();
    postTransConfig(transientInput); // TODO: instead of Transient logging, change func to POST
  };

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0">
        <div className="rounded-t bg-white mb-0 px-6 py-6">
          <div className="text-center flex justify-between">
            <h6 className="text-blueGray-700 text-xl font-bold">
              Transient Input
            </h6>
          </div>
        </div>
        <div className="flex-auto px-4 lg:px-10"></div>
        <form onSubmit={handleSubmit}>
          <button className="w-full px-4 py-2">
            <CardStopStart
              statTitle="Refresh"
              color="bg-purple-200"
              accent="active:bg-purple-500"
            />
          </button>
        </form>
        <form onSubmit={handleLoadTransConfig}>
          <button className="w-full px-4 py-2">
            <CardStopStart
              statTitle="Load Transient Configuration"
              color="bg-lightBlue-500"
              accent="active:bg-lightBlue-600"
            />
          </button>
          <div className="flex-auto px-4 lg:px-10 py-2"></div>
          <div className="flex flex-wrap">
            <div className="w-full lg:w-6/12 px-4">
              <div className="relative w-full mb-3">
                <label className="block uppercase text-blueGray-600 text-xs font-bold mb-2">
                  Start
                </label>
                <input
                  type="number"
                  className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                  value={transientInput.start_y}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="w-full lg:w-6/12 px-4">
              <div className="relative w-full mb-3">
                <label className="block uppercase text-blueGray-600 text-xs font-bold mb-2">
                  End
                </label>
                <input
                  type="number"
                  className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                  value={transientInput.end_y}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="w-full lg:w-6/12 px-4">
              <div className="relative w-full mb-3">
                <label className="block uppercase text-blueGray-600 text-xs font-bold mb-2">
                  Nodes
                </label>
                <input
                  type="number"
                  className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                  value={transientInput.nodes}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="w-full lg:w-6/12 px-4">
              <div className="relative w-full mb-3">
                <label
                  className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                  for="pulse"
                >
                  Preset Config
                </label>
                <select
                  className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                  value={transientInput.presetConfig}
                  onChange={handleChange}
                >
                  <option value="Linear">Linear</option>
                  <option value="Custom">Custom</option>
                </select>
              </div>
            </div>
          </div>
        </form>
        <hr className="mt-6 border-b-1 border-blueGray-300" />
      </div>
    </>
  );
}
