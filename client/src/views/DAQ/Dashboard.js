import React from "react";
import { useState } from "react";

// components

import CardStopStart from "components/Cards/CardStopStart.js";

export default function Dashboard() {
  const [userInput, setUserInput] = useState({
    // default values
    syrLen: 150,
    syrDia: 30,
    dyeSpeed: 8,
    enPulse: "True",
    testDelay: 60,
    lenExperiment: 250,
    PIVfreq: 300,
    Datafreq: 5,
  });

  const postResult = (result) => {
    console.log(result);
  };

  const handleChange = (event) => {
    const { name, type, value } = event.target;

    switch (type) {
      case "Number":
        setUserInput({ ...userInput, [name]: Number(value) });
        break;
      default:
        setUserInput({ ...userInput, [name]: value });
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    postResult(userInput); // TODO: instead of Transient logging, change func to POST
  };

  return (
    <>
      <button className="w-full px-4 py-2">
        <CardStopStart
          statTitle="Master Stop"
          color="bg-red-500"
          accent="active:bg-red-600"
        />
      </button>
      <form onSubmit={handleSubmit}>
        <button className="w-full px-4 py-4">
          <CardStopStart
            statTitle="Start Experiment"
            color="bg-emerald-500"
            accent="active:bg-emerald-600"
          />
        </button>
        <div className="flex flex-wrap">
          <div className="w-full px-4">
            <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0">
              <div className="rounded-t bg-white mb-0 px-6 py-6">
                <div className="text-center flex justify-between">
                  <h6 className="text-blueGray-700 text-xl font-bold">
                    User Configuration
                  </h6>
                  <button
                    className="bg-lightBlue-500 text-white active:bg-lightBlue-600 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
                    type="button"
                  >
                    Docs
                  </button>
                </div>
              </div>
              <div className="flex-auto px-4 lg:px-10 py-10 pt-0">
                <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                  Dye Injection Characteristics
                </h6>
                <div className="flex flex-wrap">
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Syringe Length (mm)
                      </label>
                      <input
                        type="number"
                        name="syrLen"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.syrLen}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Syringe Diameter (mm)
                      </label>
                      <input
                        type="number"
                        name="syrDia"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.syrDia}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Dye Injection Speed (mm/s)
                      </label>
                      <input
                        type="number"
                        name="dyeSpeed"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.dyeSpeed}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase font-bold mb-2 text-xs"
                        for="pulse"
                        htmlFor="grid-password"
                      >
                        Enable Pulse Mode?
                      </label>
                      <select
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        name="enPulse"
                        value={userInput.enPulse}
                        onChange={handleChange}
                      >
                        <option value={"True"}>Yes</option>
                        <option value={"False"}>No</option>
                      </select>
                    </div>
                  </div>
                </div>
                <hr className="mt-6 border-b-1 border-blueGray-300" />

                <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                  Timings
                </h6>
                <div className="flex flex-wrap">
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Testbed Stablising Delay (s)
                      </label>
                      <input
                        type="number"
                        name="testDelay"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.testDelay}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Length of Experiment (s)
                      </label>
                      <input
                        type="text"
                        name="lenExperiment"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.lenExperiment}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </div>
                <hr className="mt-6 border-b-1 border-blueGray-300" />
                <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                  Sample Frequencies
                </h6>
                <div className="flex flex-wrap">
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Datalogger Frequency (Hz)
                      </label>
                      <input
                        type="number"
                        name="Datafreq"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.Datafreq}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Particle Image Velocimetry (KHz)
                      </label>
                      <input
                        type="text"
                        name="PIVfreq"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.PIVfreq}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </div>
                <hr className="mt-6 border-b-1 border-blueGray-300" />
              </div>
            </div>
          </div>
        </div>
      </form>
    </>
  );
}
