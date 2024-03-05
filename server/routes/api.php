<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PlanModelController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/



Route::middleware(["auth:sanctum"])->group(function () {

    Route::get("/fetch/user/profile", function (Request $request) {
        return $request->user();
    });

    Route::get("/fetch/plans", [PlanModelController::class, "FetchPlans"]);
    Route::get("/fetch/plan/destinations", [PlanModelController::class, "FetchPlanDestination"]);

    Route::post("/create/plan", [PlanModelController::class, "CreatePlan"]);
    Route::post("/update/plan", [PlanModelController::class, "UpdatePlan"]);
    Route::post("/create/plan/destination", [PlanModelController::class, "CreatePlanDestination"]);

    Route::post("/gen",[PlanModelController::class,"GemAI"]);
});
