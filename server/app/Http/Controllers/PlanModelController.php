<?php

namespace App\Http\Controllers;

use App\Models\PlanModel;
use App\Models\UserDestinations;
use Illuminate\Http\Request;
use GuzzleHttp\Client;

class PlanModelController extends Controller
{

    public function FetchPlans(Request $request)
    {
        $plans = PlanModel::where("user_id", $request->user()->id)->orderBy("plan_id", "DESC")->get();

        return response()->json(["status" => true, "data" => $plans]);
    }

    public function CreatePlan(Request $request)
    {

        $request->validate([
            'plan_title' => ['required', 'string', 'max:255'],
            'budget' => ['nullable', 'string'],
            'special_occasion' => ['nullable', 'string'],
            'no_of_people' => ['nullable', 'integer'],
            'first_time_visiting' => ['nullable', 'boolean'],
            'type_of_trip' => ['nullable', 'string'],
            'sort_preference' => ['nullable', 'string', 'in:most_visited,most_reviewed'],
            'food_preference' => ['nullable', 'string'],
            'food_cost' => ['nullable', 'string']
        ]);

        $plan = new PlanModel([
            "user_id" => $request->user()->id,
            "plan_title" => $request->plan_title,
            "budget" => $request->budget,
            "special_occasion" => $request->special_occasion,
            "no_of_people" => $request->no_of_people,
            "first_time_visiting" => $request->first_time_visiting,
            "type_of_trip" => $request->type_of_trip,
            "sort_preference" => $request->sort_preference,
            "food_preference" => $request->food_preference,
            'food_cost' => $request->food_cost
        ]);

        $plan->save();

        return response()->json(["status" => true, "data" => $plan]);
    }

    public function UpdatePlan(Request $request)
    {


        $request->validate([
            'plan_id' => ['required', 'integer'],
            'plan_title' => ['required', 'string', 'max:255'],
            'budget' => ['nullable', 'string'],
            'special_occasion' => ['nullable', 'string'],
            'no_of_people' => ['nullable', 'integer'],
            'first_time_visiting' => ['nullable', 'boolean'],
            'type_of_trip' => ['nullable', 'string'],
            'sort_preference' => ['nullable', 'string', 'in:most_visited,most_reviewed'],
            'food_preference' => ['nullable', 'string'],
            'food_cost' => ['nullable', 'string']
        ]);

        $plan = PlanModel::where('user_id', $request->user()->id)
            ->where('plan_id', $request->plan_id)
            ->first();

        // If plan exists, update it
        if ($plan) {
            $plan->update([
                "plan_title" => $request->plan_title,
                "budget" => $request->budget,
                "special_occasion" => $request->special_occasion,
                "no_of_people" => $request->no_of_people,
                "first_time_visiting" => $request->first_time_visiting,
                "type_of_trip" => $request->type_of_trip,
                "sort_preference" => $request->sort_preference,
                "food_preference" => $request->food_preference,
                'food_cost' => $request->food_cost
            ]);

            return response()->json(["status" => true, "data" => $plan]);
        } else {
            return response()->json(["status" => false, "message" => "Plan does not exist"], 404);
        }
    }


    public function FetchPlanDestination(Request $request)
    {

        $request->validate([
            'plan_id' => ['required', 'integer'],
        ]);

        $plan = PlanModel::where([["user_id", "=", $request->user()->id], ["plan_id", "=", $request->plan_id]])->first();

        if ($plan === null) {
            return response()->json(["status" => false, "message" => "Plan Do Not Exists"], 404);
        }

        $destinations = UserDestinations::where([["user_id", "=", $request->user()->id], ["plan_id", "=", $request->plan_id]])->get();
        return response()->json(["status" => true, "data" => $destinations]);
    }


    public function CreatePlanDestination(Request $request)
    {

        $request->validate([
            'plan_id' => ['required', 'integer'],
            'destination_name' => ['required', 'string', "max:255"],
            'destination_datetime' => ['date_format:Y-m-d H:i:s', "nullable"],
        ]);

        $plan = PlanModel::where([["user_id", "=", $request->user()->id], ["plan_id", "=", $request->plan_id]])->first();

        if ($plan === null) {
            return response()->json(["status" => false, "message" => "Plan Do Not Exists"], 404);
        }


        $destination = new UserDestinations([
            "user_id" => $request->user()->id,
            "plan_id" => $request->plan_id,
            "destination_name" => $request->destination_name,
            "destination_datetime" => $request->destination_datetime
        ]);

        $destination->save();

        return response()->json(["status" => true, "data" => $destination]);
    }

    public function GemAI(Request $request)
    {

        return response()->json(["status" => true, "message" => "API Moved: Use Gemini Private FastAPI "],404);

        // $city = $request->input('city');
        // $people = $request->input('people');
        // $trip_type = $request->input('trip_type');
        // $first_time_visit = $request->input('first_time_visit');
        // $travel_budget = $request->input('travel_budget');
        // $food_type = $request->input('food_type');
        // $food_budget = $request->input('food_budget');
        // $PRIVATE_SERVER_API_KEY = env('PRIVATE_SERVER_API_KEY');

        // $client = new Client();

        // try {


        //     $requestBody = [
        //         'city' => $city,
        //         'people' => $people,
        //         'trip_type' => $trip_type,
        //         'first_time_visit' => $first_time_visit,
        //         'travel_budget' => $travel_budget,
        //         'food_type' => $food_type,
        //         'food_budget' => $food_budget,
        //         'SECRET_KEY' => $PRIVATE_SERVER_API_KEY,
        //     ];


        //     $response = $client->request('POST', 'http://localhost:3000/private/api/gen', [
        //         'json' => $requestBody,
        //     ]);

        //     return response()->json(json_decode($response->getBody()->getContents()));
        // } catch (\Exception $e) {
        //     // Handle any errors that occur during the request
        //     return response()->json(['error' => $e->getMessage()], 500);
        // }
    }
}
