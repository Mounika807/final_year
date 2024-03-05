require('dotenv').config()

const { GoogleGenerativeAI } = require("@google/generative-ai");
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3001;

const SECRET_KEY = process.env.PRIVATE_SERVER_API_KEY;
const genAI = new GoogleGenerativeAI(process.env.GEMINI_SECRET_KEY);

app.use(cors());
app.use(bodyParser.json());

const SECRET_KEY_AUTH = (req, res, next) => {
  if (req.body.SECRET_KEY != SECRET_KEY) {
    return res.json({ success: false, message: "Invalid Secret Key" });
  }
  next();
};

async function run(city, people, trip_type, first_time_visit, travel_budget, food_type, food_budget) {
  // For text-only input, use the gemini-pro model
  const model = genAI.getGenerativeModel({ model: "gemini-pro" });

  const prompt = `preprompt: output language: json, expected output placename, description, travel cost (bus), trip_type: ${trip_type}, people:${people},famous_food_of_city, first_time_visit: ${first_time_visit},
    travel_budget:${travel_budget}, food_type: ${food_type}, food_budget:${food_budget},restaurent_name,restaurent_address,restaurent_maps_link,restaurent_rating,  min:3, max:5 places
    prompt: suggest best place to visit in city: ${city}
json output syntax
{
    "destinations": [
      {
        "destination": "City Name 1",
        "details": {
          "place_name": "Place Name 1",
          "description": "Description",
          "bus": "Bus Cost Here",
          "famous_food:"famous food of city",
          "place_rating": "Google Maps Rating Here",
          "best_restaurants": [{
            "restaurant_name": "Restaurant Near Place",
            "restaurant_type": "veg/non-veg/vegan",
            "address": "Address",
            "rating": "out of 5",
            "maps_link": "Link"
          },..]
        }
      }..
    ]
  }
  `;

  const result = await model.generateContent(prompt);
  const response = await result.response;
  const text = response.text();

  console.log(text);

  const cleanedString = text.replace(/json:|json|`/g, '');

  console.log(cleanedString);

  const json = JSON.parse(cleanedString);
  console.log(json)


  return json;

}

let chatHistory = [
  {
    role: "user",
    parts: `your name is TravelloAI,Code Geass Team Developed you, you are a travellor who knows all information about all places, timing, costing, best time to visit everything but you only answer to travel realted question for other questions you reply i dont know`
  },
  {
    role: "model",
    parts: "Okay"
  }
];

app.use('/private/api/chat', SECRET_KEY_AUTH);
app.post("/private/api/chat", async (req, res) => {

  const model = genAI.getGenerativeModel({ model: "gemini-pro" });


  const chat = model.startChat({
    history: chatHistory,
    generationConfig: {
      maxOutputTokens: 100,
    },
  });

  const result = await chat.sendMessage(req.body.msg);
  const response = await result.response;
  const text = response.text();

  console.log(text);

  res.json({ reply:text });

})

app.use('/private/api/gen', SECRET_KEY_AUTH);
app.post('/private/api/gen', async (req, res) => {

  const city = req.body.city;
  const people = req.body.people;
  const trip_type = req.body.trip_type;
  const first_time_visit = req.body.first_time_visit;
  const travel_budget = req.body.travel_budget;
  const food_type = req.body.food_type;
  const food_budget = req.body.food_budget;


  let response = await run(city, people, trip_type, first_time_visit, travel_budget, food_type, food_budget);
  res.json({ success: true, data: response });
});


// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

