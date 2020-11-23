import { FaChevronCircleDown } from "react-icons/fa";

function traitement_donnees(data) {
  let mesdonnees_f = [];
  let tweetsO1 = {};
  let tweetsO2 = {};
  let rtO1 = [];
  let c = 0;
  let headr;
  let time_part = new Object();
  data.forEach((element) => {
    if (c === 0) {
      headr = element;
      c++;
    }
    if (!(element[45] === "")) {
      /* element.retweeted_id */
      rtO1.push(element);
    } else {
      tweetsO1[element[0]] = element;
      tweetsO2[element[0]] = parseInt(element[34]);
    }
  });

  /* why rt01 contains only the headers ??? */
  rtO1.forEach((element) => {
    let key = element[45];
    if (!(key === "retweeted_id" || key === undefined)) {
      if (!(tweetsO1[element[45]] === undefined)) {
        if (!(element[24] == tweetsO1[element[45]][24])) {
          tweetsO2[key] += parseInt(element[34]);
        }
        /*if (!(element[24] == tweetsO1[element[45]][24])) {
        tweetsO2[key] += parseInt(element[34]);*/
      }
    }
  });
  let cid = 0.1;
  /*Darkness, this is fempty*/

  /* Here we must deal with node sizes -> 10 sizes so deal with element2*/
  let min_size = Math.pow(10, 1000);
  let max_size = -Math.pow(10, 1000);
  for (const element in tweetsO2){
    if(tweetsO2[element]>max_size){
      max_size = tweetsO2[element];
    }
    else if(tweetsO2[element]<min_size){
      min_size=tweetsO2[element];
    }
  }

  min_size = Math.log(min_size);
  console.log(min_size)
  max_size = Math.log(max_size);
  console.log(max_size)
  let t = (max_size - min_size)/10
  console.log(t)
  let tweetsO3 = {};
  for(let pas = min_size; pas < max_size; pas = pas + t){

  }
  /* ---- */ 

  for (const element in tweetsO1) {
    let cir = {};
    cir.id = String(parseFloat(element)); /* "" + elt */
    cir.group = tweetsO1[element][14];
    cir.time = parseInt(Math.sqrt(tweetsO1[element][1]));
    cir.volume = parseInt(Math.log(tweetsO2[element]));
    mesdonnees_f.push(cir);
  }

  return mesdonnees_f;
}

export default traitement_donnees;
/*
let maxi_time = -Math.pow(10, 1000);
  let mini_time = Math.pow(10, 1000);
  let n  = 0;

  setTimeout(() => {
  for (const element in tweetsO1){
    n++ ;
    if (parseFloat(tweetsO1[element][1]) > maxi_time){
    maxi_time = parseFloat(tweetsO1[element][1]) ;
    }
    if (parseFloat(tweetsO1[element][1])< mini_time){
    mini_time = parseFloat(tweetsO1[element][1]);
    }

  }
  
  let pace = (maxi_time - mini_time)/n *0.9;
  let t = mini_time - 0.1*pace;
  console.log(maxi_time);
  console.log(t);
  let time_partitions= new Object;
  let Y = 4000

  while (t < maxi_time){
      time_partitions[t] = [Y,0]
      Y -= 10
      t += pace
  }

  time_partitions[(t-pace)+0.01*pace] = [Y,0];
  let Z = 4000;
 
  let a = 0;
  let d = new Object;
  let test = 0;
  for (const element in tweetsO1){
    let tem = parseFloat(tweetsO1[element][1])
    for (const elementbis in time_partitions){
      if(tem > elementbis && tem < elementbis + pace){
        continue
      }
      d[elementbis] = 1 ;
  }
}

  for(const elementb in time_partitions){
    console.log(elementb)
    if (elementb in d){
      console.log(elementb)
      time_part[elementb] = Z
      Z-=15
    }
  }*/
