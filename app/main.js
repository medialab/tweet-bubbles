import React, { useCallback, useState } from "react";
import { render } from "react-dom";
import "./style.css";
import "bulma/css/bulma.css";
import { FaGithub, FaTwitter } from "react-icons/fa";
import * as d3 from "d3";
import SvgAlpha from "/home/jean/Bureau/code/tweet-bubbles/app/mysvg.js";
import Test from "./test1.js";
import { parse } from "papaparse";
import { useDropzone } from "react-dropzone";
import { ResponsiveSwarmPlot } from "@nivo/swarmplot";
import traitement_donnees from "./traitement_donne.js";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { renderToString } from "react-dom/server";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";


const svgUrl = "/home/jean/Bureau/code/test.svg";
/*console.log(container);*/
const styles = {
  height: "500px",
};

const routes = [
  {
    path : "/mysvg",
    component : getsvg
  }
]

let data = [
  {
    id: "0.0",
    group: "group A",
    price: 109,
    volume: 20,
  },
  {
    id: "0.1",
    group: "group C",
    price: 227,
    volume: 6,
  },
  {
    id: "0.2",
    group: "group A",
    price: 404,
    volume: 14,
  },
  {
    id: "0.3",
    group: "group A",
    price: 490,
    volume: 9,
  },
  {
    id: "0.4",
    group: "group B",
    price: 60,
    volume: 14,
  },
  {
    id: "0.5",
    group: "group C",
    price: 289,
    volume: 14,
  },
  {
    id: "0.6",
    group: "group C",
    price: 382,
    volume: 12,
  },
  {
    id: "0.7",
    group: "group C",
    price: 320,
    volume: 5,
  },
  {
    id: "0.8",
    group: "group A",
    price: 457,
    volume: 15,
  },
  {
    id: "0.9",
    group: "group C",
    price: 24,
    volume: 11,
  },
  {
    id: "0.10",
    group: "group C",
    price: 187,
    volume: 18,
  },
  {
    id: "0.11",
    group: "group B",
    price: 305,
    volume: 11,
  },
  {
    id: "0.12",
    group: "group C",
    price: 138,
    volume: 6,
  },
  {
    id: "0.13",
    group: "group B",
    price: 24,
    volume: 11,
  },
  {
    id: "0.14",
    group: "group B",
    price: 214,
    volume: 8,
  },
  {
    id: "0.15",
    group: "group A",
    price: 5,
    volume: 8,
  },
  {
    id: "0.16",
    group: "group B",
    price: 76,
    volume: 11,
  },
  {
    id: "0.17",
    group: "group C",
    price: 104,
    volume: 10,
  },
  {
    id: "0.18",
    group: "group B",
    price: 291,
    volume: 11,
  },
  {
    id: "0.19",
    group: "group A",
    price: 281,
    volume: 15,
  },
  {
    id: "0.20",
    group: "group C",
    price: 224,
    volume: 18,
  },
  {
    id: "0.21",
    group: "group B",
    price: 178,
    volume: 5,
  },
  {
    id: "0.22",
    group: "group B",
    price: 237,
    volume: 17,
  },
  {
    id: "0.23",
    group: "group B",
    price: 359,
    volume: 17,
  },
  {
    id: "0.24",
    group: "group A",
    price: 302,
    volume: 12,
  },
  {
    id: "0.25",
    group: "group A",
    price: 392,
    volume: 7,
  },
  {
    id: "0.26",
    group: "group C",
    price: 261,
    volume: 4,
  },
  {
    id: "0.27",
    group: "group A",
    price: 198,
    volume: 10,
  },
  {
    id: "0.28",
    group: "group A",
    price: 424,
    volume: 13,
  },
  {
    id: "0.29",
    group: "group A",
    price: 123,
    volume: 5,
  },
  {
    id: "0.30",
    group: "group A",
    price: 395,
    volume: 5,
  },
  {
    id: "0.31",
    group: "group A",
    price: 475,
    volume: 9,
  },
  {
    id: "0.32",
    group: "group C",
    price: 65,
    volume: 9,
  },
  {
    id: "0.33",
    group: "group B",
    price: 222,
    volume: 13,
  },
  {
    id: "0.34",
    group: "group B",
    price: 118,
    volume: 5,
  },
  {
    id: "0.35",
    group: "group B",
    price: 422,
    volume: 8,
  },
  {
    id: "0.36",
    group: "group A",
    price: 39,
    volume: 10,
  },
  {
    id: "0.37",
    group: "group A",
    price: 366,
    volume: 16,
  },
];

/* This is the Main function (TOP) */
const container = document.getElementById("app");

const MyResponsiveSwarmPlot = ({ array1, min, max, langue }) => (
  <ResponsiveSwarmPlot
    data={array1}
    groups={[langue]}
    value="time"
    valueFormat="$.2f"
    valueScale={{ type: "linear", min: min, max: max, reverse: false }}
    size={{ key: "volume", values: [4, 20], sizes: [6, 20] }}
    forceStrength={4}
    simulationIterations={100}
    borderColor={{
      from: "color",
      modifiers: [
        ["darker", "0"],
        ["opacity", 0.5],
      ],
    }}
    margin={{ top: 80, right: 100, bottom: 80, left: 100 }}
    enableGridY={false}
    enableGridX={false}
    enable={false}
    axisTop={null}
    /*axisTop={{
      orient: "top",
      tickSize: 10,
      tickPadding: 5,
      tickRotation: 0,
      legend: "groups = langue",
      legendPosition: "middle",
      legendOffset: -46,
    }}*/
    axisRight={{
      orient: "right",
      tickSize: 10,
      tickPadding: 5,
      tickRotation: 0,
      legend: "time",
      legendPosition: "middle",
      legendOffset: 76,
    }}
    /*axisBottom={{
      orient: "bottom",
      tickSize: 10,
      tickPadding: 5,
      tickRotation: 0,
      legend: "groups",
      legendPosition: "middle",
      legendOffset: 46,
    }}*/
    axisBottom={null}
    axisLeft={{
      orient: "left",
      tickSize: 10,
      tickPadding: 5,
      tickRotation: 0,
      legend: "time",
      legendPosition: "middle",
      legendOffset: -76,
    }}
    motionStiffness={50}
    motionDamping={10}
  />
);

function MyDropzone({ onDrope, tmin, tmax, tlangue }) {
  let mesdonnees_i = [];
  let mesdonnees_f = [];
  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file) => {
      const reader = new FileReader();
      reader.onabort = () => console.log("file reading was aborted");
      reader.onerror = () => console.log("file reading has failed");
      reader.onload = () => {
        parse(file, {
          headers: true,
          complete: function (results) {
            /*onDrope(results.data)*/
            mesdonnees_i = results.data;
            mesdonnees_f = traitement_donnees(mesdonnees_i);
            onDrope(mesdonnees_f);
            /* getting the max and min of time */
            let min = Math.pow(10, 1000);
            let max = -Math.pow(10, 1000);
            let set1 = [];
            mesdonnees_f.forEach((elmnt) => {
              if (elmnt.time < min) {
                min = elmnt.time;
              } else if (elmnt.time > max) {
                max = elmnt.time;
              }
              if (set1.includes(elmnt.group)) {
                console.log("ok");
              } else {
                set1.push(elmnt.group);
              }
            });
            /* getting languages */
            tmin(min);
            tmax(max);
            tlangue(set1);
            /*tlangue(set1)*/
          },
        });

        const binaryStr = reader.result;

        // Do whatever you want with the file contents
        /*console.log("ok");
        mesdonnees_f = traitement_donnees(mesdonnees_i);
        
        console.log("ok");
        setTimeout(() => {
          console.log(mesdonnees_f);
        }, 10);*/
      };
      reader.readAsText(file);
    });
    /* multithreading à gérer ici ? */
  }, []);
  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      <p className="has-text-centered  mt-4 is-6 mgh-medium">
        Upload your file right here
      </p>
    </div>
  );
}

export function getsvg({prop1, prop2, prop3, prop4}){
  return renderToString(<MyResponsiveSwarmPlot
    array1={prop1}
    min={prop2}
    max={prop3}
    langue={prop4}>
    </MyResponsiveSwarmPlot>
    )
}

function Application() {
  const [array1, setarray1] = useState([]);
  const [min, setmin] = useState([]);
  const [max, setmax] = useState([]);
  const [langue, setlangue] = useState([]);
  /*console.log(array1.length)*/
  console.log(array1);
  console.log(data);
  return (
    <>
      <div class="columns is-gapless is-multiline">
        <div class="column is-12">
          <h1 className="title has-text-centered size-1" id="titre">
            Tweet Bubbles
          </h1>
        </div>
        <div class="column is-12">
          <nav className="navbar is-dark" id="menu">
            <div className="container">
              <div className="navbar-brand">
                <a className="navbar-item brand-text" href="../index.html">
                  Bulma Admin
                </a>
                <div className="navbar-burger burger" data-target="navMenu">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
              <div id="navMenu" className="navbar-menu">
                <Router>
                <div className="navbar-start">
                  <a className="navbar-item" href="admin.html">
                    Show csv file
                  </a>
                  <a className="navbar-item" href="admin.html">
                    Change csv file
                  </a>
                  <Route path="/getsvg" component={getsvg(array1, min, max, langue)}></Route>
                  <a className="navbar-item" href="admin.html">
                    Export to SVG
                  </a>
                </div>
                </Router>
              </div>
            </div>
          </nav>
        </div>
      </div>
      <div className="container">
        <div className="columns">
          <div className="column is-4 ">
            <div className="container has-text-centered">
              <h2 className="title is-6 mt-4">
                What is this app made for and how to use it
              </h2>
              <p>
                This app takes a csv tweets file in input and returns a
                swarmplot visualisation of those tweets. The vertical represents
                the time (the upper the tweet is the newer it is)
              </p>
            </div>
            <div className="box mt-6">
              <h3>Contacts and ressources</h3>
              <a href="https://github.com/medialab/tweet-bubbles">
                <FaGithub /> https://github.com/medialab/tweet-bubbles
              </a>
              <br />
              <a href="https://nivo.rocks/swarmplot">
                Nivo swarmplot : https://nivo.rocks/swarmplot
              </a>
            </div>
          </div>
          <div className="column is-8">
            <MyDropzone
              onDrope={setarray1}
              tmin={setmin}
              tmax={setmax}
              tlangue={setlangue}
            >
            </MyDropzone>
            <div style={styles}>
              <MyResponsiveSwarmPlot
                array1={array1}
                min={min}
                max={max}
                langue={langue}
              ></MyResponsiveSwarmPlot>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
/*array1.forEach(element => console.log(element));*/

render(<Application />, container);
