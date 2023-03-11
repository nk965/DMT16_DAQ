import React from "react";
import { useState } from "react";

// components

import CardStopStart from "components/Cards/CardStopStart.js";

export default function Dashboard() {
  const [userInput, setUserInput] = useState({
    // default values
    DAQ_port: "COM7",
    TB_port: "COM8",
    vol_inject: 30,
    syrDia: 30,
    inject_time: 15,
    enPulse: "True",
    stabilising_delay: 60,
    lenExperiment: 20,
    PIVfreq: 20,
    Datafreq: 200,
    dutyCycle: 0.3,
    cyclePeriod: 0.5,
    trans_time: 12,
    branch_temp: 60,
  });

  const postUserConfig = (inputs) => {
    fetch("http://127.0.0.1:5000/LoadUserConfig", {
      credentials: "same-origin",
      "Content-Type": "application/json",
      method: "POST",
      body: JSON.stringify(inputs),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          alert(data.message);
        }
        console.log(data);
      })
      .catch((error) => console.log(error));
  };

  const postStart = () => {
    fetch("http://127.0.0.1:5000/StartExperiment", {
      credentials: "same-origin",
      "Content-Type": "application/json",
      method: "POST",
      body: JSON.stringify({ Status: "Start" }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          alert(JSON.stringify(data.message, null, 2));
        }
        console.log(data);
      })
      .catch((error) => console.log(error));
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

  const getPorts = () => {
    console.log("Test")

    fetch("http://127.0.0.1:5000/FindPorts")
      .then((response) => response.json())
      .then((data) => {
        alert(JSON.stringify(data, null, 2));
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const handleLoadUserConfig = (event) => {
    event.preventDefault();
    postUserConfig(userInput);
  };

  const handleStartExperiment = (event) => {
    event.preventDefault();
    postStart();
  };

  const handlePortRequest = (event) => {
    event.preventDefault();
    getPorts();
  };

  return (
    <>
      <form onSubmit={handleStartExperiment}>
        <button className="w-full px-4 py-2">
          <CardStopStart
            statTitle="Start Experiment"
            color="bg-emerald-500"
            accent="active:bg-emerald-600"
          />
        </button>
      </form>
      <form onSubmit={handlePortRequest}>
        <button className="w-full px-4 py-2">
          <CardStopStart
            statTitle="Find Serial Ports"
            color="bg-lightBlue-400"
            accent="active:bg-LightBlue-600"
          />
        </button>
      </form>
      <form onSubmit={handleLoadUserConfig}>
        <button className="w-full px-4 py-4">
          <CardStopStart
            statTitle="Load User Configuration"
            color="bg-lightBlue-400"
            accent="active:bg-lightBlue-600"
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
                </div>
              </div>
              <div className="flex-auto px-4 lg:px-10 py-10 pt-0">
                <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                  Serial Communication Ports
                </h6>
                <div className="flex flex-wrap">
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        DAQ Port (e.g., COM7 or /dev/tty.*)
                      </label>
                      <input
                        type="text"
                        name="DAQ_port"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.DAQ_port}
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
                        TB Port (e.g., COM8 or /dev/tty.*)
                      </label>
                      <input
                        type="text"
                        name="TB_port"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.TB_port}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </div>
                <hr className="mt-6 border-b-1 border-blueGray-300" />
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
                        Volume of Dye Injected (ml)
                      </label>
                      <input
                        type="number"
                        name="vol_inject"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.vol_inject}
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
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Duty Cycle (%)
                      </label>
                      <input
                        type="text"
                        name="dutyCycle"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.dutyCycle}
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
                        Period of Duty Cycle (s)
                      </label>
                      <input
                        type="number"
                        name="cyclePeriod"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.cyclePeriod}
                        onChange={handleChange}
                      />
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
                        Testbed Stabilising Delay (s)
                      </label>
                      <input
                        type="number"
                        name="stabilising_delay"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.stabilising_delay}
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
                        Logger Recording Length (s)
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
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Time of Dye Injection (s)
                      </label>
                      <input
                        type="number"
                        name="inject_time"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.inject_time}
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
                        Transient Experiment Duration (s)
                      </label>
                      <input
                        type="text"
                        name="trans_time"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.trans_time}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </div>
                <h6 className="text-blueGray-700 text-sm font-bold">*Notes</h6>
                <h6 className="text-blueGray-700 text-xs">
                  Transient Experiment Duration &lt; Time of Dye Injection &lt;
                  Logger Recording Length
                </h6>
                <hr className="mt-6 border-b-1 border-blueGray-300" />
                <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                  Sampling Frequencies
                </h6>
                <div className="flex flex-wrap">
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Datalogger Time Interval (ms)
                      </label>
                      <select
                        type="number"
                        name="Datafreq"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.Datafreq}
                        onChange={handleChange}
                      >
                        <option type="number" value={100}>
                          100
                        </option>
                        <option type="number" value={200}>
                          200
                        </option>
                        <option type="number" value={300}>
                          300
                        </option>
                        <option type="number" value={400}>
                          400
                        </option>
                        <option type="number" value={500}>
                          500
                        </option>
                        <option type="number" value={600}>
                          600
                        </option>
                        <option type="number" value={700}>
                          700
                        </option>
                        <option type="number" value={800}>
                          800
                        </option>
                        <option type="number" value={900}>
                          900
                        </option>
                        <option type="number" value={1000}>
                          1000
                        </option>
                        <option type="number" value={1100}>
                          1100
                        </option>
                        <option type="number" value={1200}>
                          1200
                        </option>
                        <option type="number" value={1300}>
                          1300
                        </option>
                        <option type="number" value={1400}>
                          1400
                        </option>
                        <option type="number" value={1500}>
                          1500
                        </option>
                        <option type="number" value={1600}>
                          1600
                        </option>
                      </select>
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
                        type="number"
                        name="PIVfreq"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.PIVfreq}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </div>
                <hr className="mt-6 border-b-1 border-blueGray-300" />
                <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
                  Testbed Configuration (future application)
                </h6>
                <div className="flex flex-wrap">
                  <div className="w-full lg:w-6/12 px-4">
                    <div className="relative w-full mb-3">
                      <label
                        className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                        htmlFor="grid-password"
                      >
                        Branch Pipe Temperature (Celsius)
                      </label>
                      <input
                        type="number"
                        name="branch_temp"
                        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={userInput.branch_temp}
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
