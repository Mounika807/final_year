<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PlanModel extends Model
{
    use HasFactory;

    protected $primaryKey = "plan_id";

    protected $fillable = [
        "plan_id",
        "user_id",
        "plan_title",
        "budget",
        "special_occasion",
        "no_of_people",
        "first_time_visiting",
        "type_of_trip",
        "sort_preference",
        "food_preference",
        'food_cost'
    ];
}
