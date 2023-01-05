import React from "react";
import PropTypes from "prop-types";

export default function CardStopStart({
  statTitle,
  color,
  accent
}) {
  return (
    <>
      <div 
      className={
        " relative flex flex-col min-w-0 break-words rounded mb-6 xl:mb-0  shadow-md hover:shadow-lg ease-linear transition-all duration-150 "
        + color + " " + accent
          }
        >
        <div className={"flex-auto p-4"}>
          <div className="flex flex-wrap">
            <div className=" w-full pr-4 max-w-full flex-grow flex-1">
              <span className="font-semibold text-xl text-black">
                {statTitle}
              </span>
            </div>
            <div className="relative w-auto pl-4 flex-initial">
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

CardStopStart.defaultProps = {
  statSubtitle: "Traffic",
  statTitle: "350,897",
  statArrow: "up",
  statPercent: "3.48",
  statPercentColor: "text-emerald-500",
  statDescripiron: "Since last month",
  statIconName: "far fa-chart-bar",
  statIconColor: "bg-red-500",
};

CardStopStart.propTypes = {
  statSubtitle: PropTypes.string,
  statTitle: PropTypes.string,
  statArrow: PropTypes.oneOf(["up", "down"]),
  statPercent: PropTypes.string,
  // can be any of the text color utilities
  // from tailwindcss
  statPercentColor: PropTypes.string,
  statDescripiron: PropTypes.string,
  statIconName: PropTypes.string,
  // can be any of the background color utilities
  // from tailwindcss
  statIconColor: PropTypes.string,
};
