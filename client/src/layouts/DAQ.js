import React from "react";
import { Switch, Route, Redirect } from "react-router-dom";

// components

import DAQNavbar from "components/Navbars/DAQNavbar.js";
import Sidebar from "components/Sidebar/Sidebar.js";
import Header from "components/Headers/Header.js";
import FooterDAQ from "components/Footers/FooterDAQ.js";

// views

import Dashboard from "views/DAQ/Dashboard.js";
import DataAnalytics from "views/DAQ/DataAnalytics.js";
import Transient from "views/DAQ/Transient.js";

export default function DAQ() {
  return (
    <>
      <Sidebar />
      <div className="relative md:ml-64 bg-blueGray-100">
        <DAQNavbar />
        {/* Header */}
        <Header />
        <div className="px-4 md:px-10 mx-auto w-full -m-24">
          <Switch>
            <Route path="/DAQ/dashboard" exact component={Dashboard} />
            <Route path="/DAQ/DataAnalytics" exact component={DataAnalytics} />
            <Route path="/DAQ/Transient" exact component={Transient} />
            <Redirect from="/DAQ" to="/DAQ/dashboard" />
          </Switch>
          <FooterDAQ />
        </div>
      </div>
    </>
  );
}
