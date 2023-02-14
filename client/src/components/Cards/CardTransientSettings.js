import React from "react";
import { useState } from "react";
// components

export default function CardTransientSettings() {

  const [transientInput, setTransInput] = useState({
    // default values
    start_y: 25, 
    end_y: 55,
    nodes: 7,
    presetConfig: "Linear",
    trans_time: 15 
  });

  const postResult = (result) => {
    console.log(result);
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

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0">
        <div className="rounded-t bg-white mb-0 px-6 py-6">
          <div className="text-center flex justify-between">
            <h6 className="text-blueGray-700 text-xl font-bold">Transient Input</h6>
          </div>
        </div>
        <div className="flex-auto px-4 lg:px-10 py-10">
        <form onSubmit={handleSubmit}>
        <div className="w-full px-4">
          <button className="py-3 px-4 placeholder-blueGray-300 bg-lightBlue-500 text-white active:bg-lightBlue-600 rounded text-xl font-bold shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"> Refresh </button>
        </div>
            <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
            </h6>
            <div className="flex flex-wrap">
              <div className="w-full lg:w-6/12 px-4">
                <div className="relative w-full mb-3">
                  <label
                    className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                    
                  >
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
                  <label
                    className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                    
                  >
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
                  <label
                    className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                    
                  >
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
                  <select className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                  value={transientInput.presetConfig}
                  onChange={handleChange}>
                    <option value="Linear">Linear</option>
                    <option value="Custom">Custom</option>
                  </select>
                </div>
              </div>
              <div className="w-full lg:w-6/12 px-4">
                <div className="relative w-full mb-3">
                  <label
                    className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                    
                  >
                    Time
                  </label>
                  <input
                    type="number"
                    className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                    value={transientInput.trans_time}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>
            </form>
            <hr className="mt-6 border-b-1 border-blueGray-300" />
          <h6 className="text-blueGray-700 text-sm font-bold">*Notes</h6>
            <h6 className="text-blueGray-700 text-xs">After input has been configured, click the refresh button. Time refers to the length of transient condition (different to experiment time)</h6>
        </div>
      </div>
    </>
  );
}
