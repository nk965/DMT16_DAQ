import React from "react";
import Chart from "chart.js";

import { useState, useEffect } from "react";

export default function CardLineChart() {

  const [data, setData] = useState({ labels: [], datasets: [] }); 

  const handleRefreshClick = () => {

    console.log("Hello")

    fetch("http://127.0.0.1:5000/RefreshTransConfig")
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Log the data
      setData({
        labels: data.message.labels,
        datasets: [
          {
            label: "Branch Pipe Valve",
            backgroundColor: "#4c51bf",
            borderColor: "#4c51bf",
            data: data.message.values,
            fill: false,
          },
        ],
      });
    });
};

  useEffect(() => {

    fetch('http://127.0.0.1:5000/RefreshTransConfig')
      .then(response => response.json())
      .then(data => setData({
        labels: data.message.labels,
        datasets: [{
          label: "Branch Pipe Valve",
          backgroundColor: "#4c51bf",
          borderColor: "#4c51bf",
          data: data.message.values,
          fill: false,
        }]
      }));


    var config = {
      type: "line",
      data: {
        labels: [1, 2, 3, 4, 5, 6, 7],
        datasets: [
          {
            label: "Branch Pipe Valve",
            backgroundColor: "#4c51bf",
            borderColor: "#4c51bf",
            data: [25, 30, 35, 40, 45, 50, 55],
            fill: false,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        legend: {
          labels: {
            fontColor: "white",
          },
          align: "end",
          position: "bottom",
        },
        tooltips: {
          mode: "index",
          intersect: false,
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          xAxes: [
            {
              ticks: {
                fontColor: "rgba(255,255,255,.7)",
              },
              display: true,
              scaleLabel: {
                display: false,
                labelString: "Month",
                fontColor: "white",
              },
              gridLines: {
                display: false,
                borderDash: [2],
                borderDashOffset: [2],
                color: "rgba(33, 37, 41, 0.3)",
                zeroLineColor: "rgba(0, 0, 0, 0)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
          yAxes: [
            {
              ticks: {
                fontColor: "rgba(255,255,255,.7)",
              },
              display: true,
              scaleLabel: {
                display: false,
                labelString: "Value",
                fontColor: "white",
              },
              gridLines: {
                borderDash: [3],
                borderDashOffset: [3],
                drawBorder: false,
                color: "rgba(255, 255, 255, 0.15)",
                zeroLineColor: "rgba(33, 37, 41, 0)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
        },
      },
    };
    var ctx = document.getElementById("line-chart").getContext("2d");
    window.myLine = new Chart(ctx, config);
  }, []);
  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-blueGray-700">
        <div className="rounded-t mb-0 px-4 py-3 bg-transparent">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full max-w-full flex-grow flex-1">
              <h6 className="uppercase text-blueGray-100 mb-1 text-xs font-semibold">
                Configure Transient Input
              </h6>
              <h2 className="text-white text-xl font-semibold">Flow Actuator Valve</h2>
            </div>
            <div className="relative w-full max-w-full flex-grow flex-1 text-right">
              <button onClick={handleRefreshClick} className="bg-white text-gray-800 active:bg-gray-100 text-xs font-bold uppercase px-4 py-2 rounded shadow hover:shadow-md transition duration-300 ease-in-out outline-none focus:outline-none mr-2 mb-1">
                Refresh
              </button>
            </div>
          </div>
        </div>
        <div className="p-4 flex-auto">
          {/* Chart */}
          <div className="relative h-350-px">
            <canvas id="line-chart"></canvas>
          </div>
        </div>
      </div>
    </>
  );
}
