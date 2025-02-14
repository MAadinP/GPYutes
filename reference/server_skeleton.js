//web application framework
const express = require('express');
//sends requests to the arduino
const axios = require('axios');
//handle file paths
const path = require('path');

const app = express();
//Arduino IP address and port 
const ARDUINO_IP = '192.168.174.60'; 
const ARDUINO_PORT = 80;

//storing the current state 
let currentState = 'OFF';
let currentInfrared = 'N/A';
let currentRadio = 'N/A';
let currentUltrasound = 'N/A';
let currentMagnetic = 'N/A';
//array to store the connected clients for server sent events
let clients = [];

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

//Server sent events 
//Setting up a stream to send data to clients 
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  res.write(`data: ${JSON.stringify({ 
    state: currentState,
    infrared: currentInfrared,
    radio: currentRadio,
    ultrasound: currentUltrasound,
    magentic: currentMagnetic
 })}\n\n`);

  clients.push(res);

  //clients are removed when disconnected
  req.on('close', () => {
    clients = clients.filter(client => client !== res);
  });
});

//sends updates state and sensor data to all connected clients
const broadcastState = () => {
  clients.forEach(client => {
    client.write(`data: ${JSON.stringify({ 
      state: currentState,
      infrared: currentInfrared,
      radio: currentRadio,
      ultrasound: currentUltrasound,
      magnetic: currentMagnetic
    })}\n\n`);
  });
};

//sends commands to the Arduino 
//updates the server's state with response
//sends GET request to Arduino
//updates corresponding state variable 
//broadcasts the new state
const sendCommand = async (command) => {
  try {
    const response = await axios.get(`http://${ARDUINO_IP}:${ARDUINO_PORT}/${command}`);
    if (command === 'infrared'){
      currentInfrared = response.data;
    }
    else if(command === 'radio'){
      currentRadio = response.data;
    }
    else if(command === 'ultrasound'){
      currentUltrasound = response.data;
    }
    else if(command === 'magnetic'){
      currentMagnetic = response.data;
    }
    else{
      currentState = response.data;
    }
    broadcastState();
    return response.data;
  } catch (error) {
    console.error(`Error sending command: ${error}`);
    return 'Error';
  }
};

//Specific commands to the arduino 
//results are returned 
//DIRECTIONS
app.get('/forw', async (req, res) => {
  console.log("FORWARD");
  const result = await sendCommand('forw');
  res.send(result);
});

app.get('/back', async (req, res) => {
  console.log("BACKWARD");
  const result = await sendCommand('back');
  res.send(result);
});

app.get('/stop', async (req, res) => {
  console.log("STOP");
  const result = await sendCommand('stop');
  res.send(result);
});

app.get('/right', async (req, res) => {
  console.log("RIGHT");
  const result = await sendCommand('right');
  res.send(result);
});

app.get('/left', async (req, res) => {
  console.log("LEFT");
  const result = await sendCommand('left');
  res.send(result);
});


//SENSORS
//IFR
app.get('/infrared', async (req, res) => {
  console.log("INFRARED");
  const result = await sendCommand('infrared');
  res.send(result);
});

//Radio
app.get('/radio', async (req, res) => {
  console.log("RADIO");
  const result = await sendCommand('radio');
  res.send(result);
});

//Ultrasound
app.get('/ultrasound', async (req, res) => {
  console.log("ULTRASOUND");
  const result = await sendCommand('ultrasound');
  res.send(result);
});

//Magnetic
app.get('/magnetic', async (req, res) => {
  console.log("MAGNETIC");
  const result = await sendCommand('magnetic');
  res.send(result);
});


//Server connection via ports 
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Node.js server listening on port ${PORT}`);
});

